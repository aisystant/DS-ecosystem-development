---
type: work-package
number: 168
title: "Миграция guides-mcp: SurrealDB → Neon"
status: in_progress
budget: "3-5h"
created: 2026-03-23
updated: 2026-03-26
parent: WP-73
repo: DS-MCP
artifact: "guides-mcp работает на Neon, SurrealDB выведен из стека"
---

# РП #168: Миграция guides-mcp: SurrealDB → Neon

## Статус

| Фаза | Статус | Описание |
|------|--------|----------|
| Ф0. Документ для архитектора | **выполнено** | Создан 23 мар, 2 коммита |
| Ф1. Переписать guides-mcp на Neon | **выполнено** | Коммит `9848b57` |
| Ф2. CI cleanup | ожидает Ф1 | Удалить `publish-to-surreal.yaml` |
| Ф3. Decommission SurrealDB | ожидает доступы | Выключить сервер, обновить документацию |

## Контекст (актуализирован 25 мар)

### Текущая ситуация

- **CI сломан с 12 февраля** — `publish-to-surreal.yaml` = `401 Unauthorized`. Данные в SurrealDB устарели на >40 дней
- **Latency** — 17-20 сек на запрос (SurrealDB full vector scan, без индекса)
- **Данные уже в Neon** — `ingest.ts` индексирует те же гайды как source `docs-courses` (2697 docs). Переиндексация event-driven: GitHub Action при push + `selective-reindex.sh` при Session Close

### Архитектурные различия guides-mcp vs knowledge-mcp

| Параметр | guides-mcp (текущий) | knowledge-mcp (целевой бэкенд) |
|----------|---------------------|-------------------------------|
| БД | SurrealDB (`surrealdb.aisystant.com`) | Neon pgvector (`neondb`) |
| Embedding модель | OpenAI `text-embedding-3-small` **1536d** | OpenAI `text-embedding-3-small` **1024d** (dimensions=1024) |
| Embedding вектор | `vector<1536>` | `vector(1024)` |
| Индекс | Нет (full scan) | HNSW (`vector_cosine_ops`) |
| Таблицы | `guides`, `sections`, `chunks` (3 таблицы) | `documents` (1 таблица, `source='docs-courses'`) |
| Гранулярность | guide → section → chunk (иерархия) | filename-level + автоматический chunking >10KB |
| Поиск | Только vector (cosine) | Hybrid: vector + keyword + FTS + trigram |
| Деплой | CF Worker (`guides-mcp`) | CF Worker (`knowledge-mcp`) |
| Auth | SurrealDB user/pass → JWT token cache 4 мин | Neon connection string (DATABASE_URL) |

**Критическое:** Guides-mcp генерирует **собственные embeddings** при каждом `semantic_search` запросе через OpenAI API. После миграции на Neon нужно использовать embeddings **уже существующие** в `documents.embedding` (1024d, Voyage AI) — значит, запросы `semantic_search` должны генерировать embedding через **OpenAI** (`text-embedding-3-small`, dimensions=1024), ту же модель что и при индексации.

### Согласованные решения

| # | Решение | Статус |
|---|---------|--------|
| 1 | guides-mcp остаётся как отдельный L2 MCP | ожидает согласования |
| 2 | Переписать guides-mcp на Neon | ожидает согласования |
| 3 | CI: удалить `publish-to-surreal.yaml` | ожидает согласования |
| 4 | SurrealDB — выключить | ожидает согласования |

### Что нужно от архитектора

| # | Вопрос | Статус |
|---|--------|--------|
| 1 | Согласовать решения 1-4 | ожидает |
| 2 | Кто управляет `surrealdb.aisystant.com`? | ожидает |
| 3 | Credentials SurrealDB — почему 401 с 12 фев? | ожидает |
| 4 | Доступ к GitHub Secrets репо `docs` | ожидает |
| 5 | CF Workers деплой — может ли Tseren через `wrangler`? | ожидает |

---

## Фаза 1 (сегодня): Переписать guides-mcp на Neon

> **Бюджет:** ~2-3h | **Блокер:** нет (код локально, деплой отдельно)

### Что меняется в `guides-mcp/src/index.ts`

**Удалить:**
- Весь SurrealDB-слой: `surrealSignin()`, `surrealQueryRaw()`, `surrealQuery()`, token cache (~95 строк)
- `getEmbedding()` через OpenAI API (~10 строк)
- Зависимость от `openai` в `package.json`
- Env-переменные: `SURREAL_URL`, `SURREAL_NS`, `SURREAL_DB`, `SURREAL_USER`, `SURREAL_PASS`, `OPENAI_API_KEY`

**Добавить:**
- Подключение к Neon через `@neondatabase/serverless` (neon http driver)
- Env-переменная: `DATABASE_URL` (Neon connection string)
- Secret `OPENAI_API_KEY` для OpenAI (embedding через `text-embedding-3-small`, 1024d)

**Переписать 4 инструмента:**

| Инструмент | SurrealDB (было) | Neon (станет) |
|-----------|-------------------|---------------|
| `get_guides_list` | `SELECT FROM guides WHERE lang=$lang` | `SELECT DISTINCT ON (filename) filename, content FROM documents WHERE source='docs-courses'` — извлечь каталог гайдов из filename patterns |
| `get_guide_sections` | `SELECT FROM sections WHERE guide_id=$id` | `SELECT filename, content FROM documents WHERE source='docs-courses' AND filename LIKE $pattern` — секции по структуре filename |
| `get_section_content` | `SELECT content FROM sections WHERE guide_id=$id AND slug=$slug` | `SELECT content FROM documents WHERE source='docs-courses' AND filename=$filename` |
| `semantic_search` | OpenAI embedding → `vector::similarity::cosine()` в SurrealDB | OpenAI embedding (1024d) → `1 - (embedding <=> $vec)` в Neon pgvector |

**Маппинг данных (SurrealDB → Neon):**

В Neon таблице `documents` для `source='docs-courses'`:
- `filename` = путь к .md файлу (напр. `systems-thinking/02-methodology/01-intro.md`)
- `content` = текст документа (или чанка для файлов >10KB с breadcrumb `::`)
- `embedding` = vector(1024) — OpenAI text-embedding-3-small (dimensions=1024)
- `search_vector` = tsvector для FTS

Иерархия `guide → section → chunk` воссоздаётся из структуры `filename`:
- Guide = первый сегмент пути (`systems-thinking/`)
- Section = второй+ сегмент (`02-methodology/01-intro.md`)
- Chunk = записи с `::` в filename (`01-intro.md::Section Name`)

### Шаги реализации

1. **Изучить данные** — запрос к Neon: какие filename patterns есть для `source='docs-courses'`? Сколько записей? Структура?
2. **Переписать DB-слой** — удалить SurrealDB, добавить Neon (`@neondatabase/serverless`)
3. **Переписать `get_guides_list`** — каталог из уникальных guide-директорий
4. **Переписать `get_guide_sections`** — секции из filename-структуры внутри guide
5. **Переписать `get_section_content`** — прямой SELECT по filename
6. **Переписать `semantic_search`** — CF AI embedding + pgvector cosine
7. **Обновить `wrangler.toml`** — убрать SURREAL_*, добавить `[ai] binding`
8. **Обновить `package.json`** — убрать `openai`, добавить `@neondatabase/serverless`
9. **Локальный тест** — `wrangler dev` + curl к `/mcp`
10. **Коммит** — ветка `feature/neon-migration`

### Риски Ф1

| Риск | Митигация |
|------|-----------|
| Структура filename в `docs-courses` не позволяет воссоздать иерархию guide/section | Шаг 1: изучить данные ДО написания кода |
| OpenAI API недоступен без ключа | Использовать существующий OPENAI_API_KEY из guides-mcp |
| `@neondatabase/serverless` + CF Workers совместимость | Уже работает в knowledge-mcp — копируем паттерн |

---

## Фаза 2: CI cleanup

> **Бюджет:** ~30 мин | **Блокер:** доступ к GitHub Secrets репо `docs` (вопрос 4)

- Удалить `docs/.github/workflows/publish-to-surreal.yaml`
- Удалить `docs/scripts/publish_to_surreal/` (Python-скрипт ingestion)
- Опционально: добавить `selective-reindex.sh docs-courses` как workflow при push в `docs/ru/**`

---

## Фаза 3: Decommission SurrealDB

> **Бюджет:** ~30 мин | **Блокер:** ответ архитектора (вопросы 2-3)

- Выключить `surrealdb.aisystant.com`
- Удалить `knowledge-mcp/scripts/migrate-guides.ts` (legacy migration script)
- Обновить MAP.002: убрать SurrealDB из стека
- Обновить MEMORY.md: убрать упоминания SurrealDB
- Обновить WP-73 §3.8.4: отметить SurrealDB как decommissioned

---

## Результат

| Метрика | Было | Станет |
|---------|------|--------|
| Latency поиска | 17-20 сек | <1 сек (HNSW) |
| Данные актуальны | Нет (CI сломан с 12 фев) | Да (Neon, event-driven reindex при push) |
| Embedding модель | OpenAI 1536d | OpenAI text-embedding-3-small 1024d (та же учётка, dimensions=1024) |
| Внешние БД | Neon + SurrealDB | Neon |
| guides-mcp | Платформенный, отдельный | Платформенный, отдельный (на Neon) |

*Создан: 2026-03-23. Обновлён: 2026-03-26*
