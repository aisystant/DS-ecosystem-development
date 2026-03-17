---
type: architecture-proposal
title: "Knowledge Gateway + BYOB — архитектура доступа к знаниям"
status: draft
created: 2026-03-17
parent: WP-73
related_adr: ADR-018
for: architect
---

# Knowledge Gateway + BYOB: предложение для обсуждения с архитектором

> **Контекст:** ADR-018 (MCP Hub) описывает единую точку доступа к MCP-серверам. Это предложение уточняет модель данных для пользовательских MCP — как хранить знания пользователя и как объединять платформенные + пользовательские источники в один endpoint.

<details open>
<summary><b>1. Проблема</b></summary>

Сейчас knowledge-mcp — монолит: 11 источников (4 платформенных Pack + SPF/FPF + DS + guides + личные) в одной Neon DB. Проблемы:

1. **Пользователь не может подключить свой Pack.** У каждого пользователя IWE будут собственные Pack-репо (их предметные области). Текущий knowledge-mcp — это наш сервер, пользователь не может добавить туда свои источники.

2. **Смешаны контуры.** Платформенные знания (ZP, FPF, SPF, PACK-digital-platform) и личные знания (DS-Knowledge-Index-Tseren, aist-bot-docs) — в одной базе. Нет изоляции.

3. **Масштаб.** При 100 пользователях × 1000 docs = 100K записей в одном Neon. Платформа платит за хранение чужих данных.

4. **Доверие.** Pack пользователя = конфиденциальное доменное знание (его бизнес). Хранение на нашем сервере = trust barrier.

5. **GDPR.** Если храним данные пользователей — мы data processor со всеми обязательствами.

</details>
<details open>
<summary><b>2. Предлагаемое решение: BYOB (Bring Your Own Backend)</b></summary>

**Принцип:** платформа даёт код и L2-знания. Данные пользователя — на **его** ресурсах. Пользователь не думает, какой MCP спрашивать — один endpoint, за кулисами fan-out по источникам.

### 2.1. Два контура

| Контур | Что индексирует | Где живёт | Кто владеет |
|---|---|---|---|
| **L2 Platform** | ZP, FPF, SPF, платформенные Pack, courses, guides, FMT-docs | Remote (наш CF Worker + Neon) | Платформа |
| **L4 Personal** | Пользовательские Pack-*, DS-*, личные заметки | BYOB: его Neon / Supabase / SQLite | Пользователь |

### 2.2. Knowledge Gateway (локальный прокси)

```
Клиент (Claude Code / Cursor / бот)
    │  один MCP-endpoint (stdio или SSE)
    ▼
Knowledge Gateway (локальный процесс на машине пользователя)
    │
    ├── L2: Platform Knowledge MCP (remote, наш)
    │   URL: knowledge-mcp.aisystant.workers.dev
    │   Источники: ZP, FPF, SPF, PACK-DP, PACK-education, courses, guides
    │
    └── L4: Personal Knowledge MCP (BYOB)
        Backend: Neon (его) / Supabase (его) / SQLite (локально)
        Источники: PACK-my-domain-1, PACK-my-domain-2, DS-*

    Алгоритм:
    1. search(query) → параллельно в L2 и L4
    2. Merge результатов по score (cosine similarity)
    3. Единый ответ клиенту
```

### 2.3. Backend Interface

Общий контракт для любого L4-хранилища:

```typescript
interface KnowledgeBackend {
  search(query: string, embedding: number[], limit: number): Promise<SearchResult[]>
  ingest(docs: Document[]): Promise<void>
  listSources(): Promise<Source[]>
}

// Реализации:
class NeonBackend implements KnowledgeBackend { ... }
class SupabaseBackend implements KnowledgeBackend { ... }
class SqliteBackend implements KnowledgeBackend { ... }
```

### 2.4. Варианты хранилища для пользователя

| Backend | Бесплатный tier | Vector search | Setup |
|---------|----------------|---------------|-------|
| **Neon** (pgvector) | 0.5 GB | pgvector cosine | Низкая — обкатано |
| **Supabase** (pgvector) | 500 MB | pgvector cosine | Низкая |
| **SQLite** (sqlite-vss) | Безлимит | sqlite-vss cosine | Нулевая |

### 2.5. Setup для пользователя

В `setup.sh` шаблона IWE добавляется секция:

```bash
echo "=== Настройка Knowledge Gateway ==="
echo "Ваши Pack-данные хранятся у ВАС."
echo "Выберите хранилище:"
echo "  1) Neon (рекомендуется, бесплатно до 0.5GB)"
echo "  2) Supabase (бесплатно до 500MB)"
echo "  3) Локальное (SQLite, без регистрации)"
read -p "Выбор [1]: " choice
# → записывает L4_BACKEND, L4_DATABASE_URL в ~/.iwe-env
# → init-schema.ts (создание таблиц)
# → ingest.ts (первичная индексация Pack-папок)
```

### 2.6. Синхронизация

Sync-agent (R8 Синхронизатор) при Close или по cron:
- `selective-reindex.sh` → ingest обновлённых Pack в L4 backend пользователя
- L2 обновляется платформой независимо (weekly full + selective on commit)

</details>
<details>
<summary><b>3. Что меняется в текущей архитектуре</b></summary>

| Компонент | Сейчас | Станет |
|---|---|---|
| **knowledge-mcp** | Monolith: 11 sources, 1 user | Разделяется на: L2 (platform, remote) + L4 (personal, BYOB) |
| **Neon DB** | Без tenant_id, все данные вместе | Платформенный Neon = только L2. L4 = на ресурсах пользователя |
| **ingest.ts** | Прямой доступ к Neon | + Backend interface для разных хранилищ |
| **sources.json** | Один файл, 11 источников | L2 sources (платформенные, на сервере) + L4 sources (пользовательские, локальный конфиг) |
| **search** | Один SQL-запрос | Fan-out: L2 (remote HTTP) + L4 (local backend) → merge |
| **setup.sh** | Нет MCP-регистрации | + Выбор backend + init-schema + первичный ingest |
| **selective-reindex.sh** | Прямой ingest в Neon | + Ingest через Backend interface (может быть SQLite) |

</details>
<details>
<summary><b>4. Альтернативы (рассмотрены и отклонены)</b></summary>

| Вариант | ЭМОГССБ | Почему отклонён |
|---|---|---|
| **A. Оставить как есть** | — | Пользователь не может подключить свой Pack. Не масштабируется |
| **B. Multi-tenant Neon** (все данные на платформе, tenant_id) | 8.7 | Безопасность = 7 (GDPR, trust barrier). Платформа хранит чужие бизнес-данные |
| **C. Полностью локальный** (SQLite only, без remote L2) | 8.0 | Обучаемость = 6 (нужен Node.js, embeddings API). Нет платформенных знаний без интернета |
| **D. BYOB** (предлагаемый) | **9.1** | Лучший баланс: безопасность = 10 (данные не уходят), масштаб = 10 (каждый на своём), обучаемость = 8 (setup.sh) |

</details>
<details>
<summary><b>5. АрхГейт (ЭМОГССБ 9.1)</b></summary>

| Характеристика | Оценка | Обоснование |
|---|---|---|
| Э — Эволюционируемость | **9** | Backend interface: новый backend = реализовать interface. Новый Pack = строка в sources.json |
| М — Масштабируемость | **10** | BYOB: каждый пользователь на своём хранилище. L2 на CF Workers (scale-to-zero) |
| О — Обучаемость | **8** | setup.sh делает почти всё. SQLite = нулевой порог. Neon/Supabase = завести аккаунт |
| Г — Генеративность | **9** | Каждый Pack = новая ячейка знания, автоматически доступна через gateway |
| Ск — Скорость | **8** | L4 local (SQLite) <50ms. L4 remote (Neon) ~100ms. L2 ~300ms. Параллельный fan-out |
| Со — Современность | **10** | BYOB + local-first + federated search = SOTA. Context Engineering: Select + Compress |
| Б — Безопасность | **10** | Данные пользователя НЕ на платформе. Нет PII. Нет GDPR-ответственности за L4 |
| **Итого** | **9.1** | Порог ≥8 пройден |

</details>
<details>
<summary><b>6. Вопросы для обсуждения</b></summary>

### 6.1. Архитектурные

| # | Вопрос | Варианты | Моё предпочтение |
|---|---|---|---|
| Q1 | **Gateway как отдельный процесс или встроенный в personal-mcp?** | (A) Отдельный процесс — 3 артефакта. (B) Personal-mcp сам ходит в L2 — 2 артефакта | B — меньше движущихся частей |
| Q2 | **Embeddings для L4 — кто считает?** | (A) Cloudflare AI (бесплатно, remote). (B) Локальная модель (e.g. all-MiniLM). (C) OpenAI API (платно) | A — уже работает для L2, единая модель |
| Q3 | **Формат merge результатов L2+L4** | (A) Простой merge по score. (B) Weighted merge (L4 boost для персональных запросов). (C) Cascade: сначала L4, потом L2 если мало результатов | A для MVP, B позже |
| Q4 | **Как gateway подключается к клиенту?** | (A) stdio MCP (через .mcp.json). (B) SSE/HTTP (localhost:PORT). (C) Через MCP Hub (remote) | A — стандартный для Claude Code |

### 6.2. Продуктовые

| # | Вопрос |
|---|---|
| Q5 | С какого тира доступен Knowledge Gateway? T3 (персонализация) или T4 (созидание)? |
| Q6 | Нужен ли Web App UI для управления sources (добавить/удалить Pack)? Или только CLI/config? |
| Q7 | Community MCP: может ли пользователь A опубликовать свой Pack-MCP для пользователя B? Если да — через Hub или P2P? |

### 6.3. Миграционные

| # | Вопрос |
|---|---|
| Q8 | Мигрировать текущий knowledge-mcp сразу или поэтапно? (Фаза 1: выделить L2. Фаза 2: добавить L4 + gateway) |
| Q9 | DS-Knowledge-Index-Tseren и aist-bot-docs — переносить в L4 сейчас? Это breaking change для текущих сессий Claude Code |

</details>
<details>
<summary><b>7. Связанные документы</b></summary>

- **[WP-73 §3.8](WP-73-aisystant-platform-architecture.md)** — MCP Hub (ADR-018 v2, обновлён 17 мар)
- **[DP.D.036](../../../PACK-digital-platform/pack/digital-platform/01-domain-contract/DP.D.036-byob-knowledge-architecture.md)** — Различение BYOB vs Managed
- **[DP.D.031](../../../PACK-digital-platform/pack/digital-platform/01-domain-contract/DP.D.031-mcp-access-model.md)** — MCP Access Model
- **[DP.D.035](../../../PACK-digital-platform/pack/digital-platform/01-domain-contract/DP.D.035-data-policy.md)** — Единая политика данных IWE

</details>
