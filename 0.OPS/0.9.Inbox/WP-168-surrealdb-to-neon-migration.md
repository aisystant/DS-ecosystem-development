---
type: work-package
number: 168
title: "Миграция SurrealDB → Neon (guides-mcp)"
status: pending
budget: "3-5h"
created: 2026-03-23
parent: WP-73
repo: DS-MCP
artifact: "SurrealDB выведен из стека, guides-mcp поглощён knowledge-mcp"
---

# РП #168: Миграция SurrealDB → Neon (guides-mcp)

## Предложение (на согласование)

Вывожу SurrealDB из стека. Данные гайдов **уже в Neon** через штатный `ingest.ts` (source `docs-courses`, 2697 docs — в 9x больше чем в SurrealDB). Поиск **уже работает** через knowledge-mcp. Осталось: переключить CI, удалить guides-mcp, выключить SurrealDB.

### Принятые решения

| # | Решение | Обоснование |
|---|---------|-------------|
| 1 | **Схема — плоская** (единая таблица `documents`) | Уже работает: `ingest.ts` → `documents` (source=`docs-courses`, 2697 docs) |
| 2 | **Эмбеддинги — CF AI 1024d** | Уже в Neon. Унификация с остальными документами. HNSW индекс настроен |
| 3 | **Единый search** (`source_type='guides'` для фильтрации) | knowledge-mcp уже поддерживает. Два MCP для одной задачи — лишнее |
| 4 | **Навигация — добавить** `get_guides_list` + `get_guide_sections` в knowledge-mcp | Парсинг `filename` по `/`, без изменения схемы. Нужно для пошагового чтения (SC-2) |
| 5 | **Rollback не нужен** — SurrealDB отключить сразу | Source-of-truth = VitePress файлы. Восстановление = повторный ingest |

### План (3 фазы)

**Фаза 1.** Добавить `get_guides_list` + `get_guide_sections` в knowledge-mcp (парсинг filename)

**Фаза 2.** Переключить CI: `publish_to_surreal` → вызов `selective-reindex.sh docs-courses` (данные уже индексируются через `ingest.ts`)

**Фаза 3.** Cleanup: удалить `DS-MCP/guides-mcp/`, `docs/scripts/publish_to_surreal/`, CI workflow `publish-to-surreal.yaml`, `migrate-guides.ts`. Выключить `surrealdb.aisystant.com`. Обновить MAP.002, MEMORY.md, WP-73 §3.8.4

### Что нужно от архитектора

> Перенос данных НЕ нужен — данные уже в Neon. Нужно только переключить CI и вычистить старое.

| # | Что нужно | Зачем | Кто делает |
|---|-----------|-------|------------|
| 1 | **Согласовать решения 1-5** (таблица выше) | Без согласования не начинаем | Архитектор |
| 2 | **Выключить `surrealdb.aisystant.com`** | Кто управляет сервером? DNS, хостинг | Архитектор (или указать кто) |
| 3 | **Доступ к GitHub Secrets** репо `docs` | Заменить `SURREAL_*` + `OPENAI_API_KEY` → `DATABASE_URL` (Neon) + `CF_AI_TOKEN` | Tseren (если есть admin) или архитектор |
| 4 | **CF Workers деплой** — подтвердить что Tseren может деплоить через `wrangler` | Деплой knowledge-mcp (ручной, нет CI) | Tseren (если `wrangler login` работает) |

**Если доступы 3-4 есть** → делаем сами, архитектор только п.1 + п.2.

### Результат

| Метрика | Было | Станет |
|---------|------|--------|
| Latency поиска | 17-20 сек | <1 сек |
| MCP для знаний | 2 | 1 |
| Внешние БД | Neon + SurrealDB | Neon |

<details>
<summary><b>Контекст (если нужны детали)</b></summary>

**SurrealDB сейчас:** 3 таблицы (guides ~30, sections ~300, chunks ~3000), OpenAI 1536d, хост `surrealdb.aisystant.com`. Единственный потребитель — guides-mcp (CF Worker).

**Neon сейчас:** source `docs-courses` = 2697 docs (source_type=`guides`), CF AI 1024d, HNSW индекс. Данные попали через штатный `ingest.ts` (не `migrate-guides.ts` — он не запускался). Регулярная переиндексация: `reindex.sh` (Пт 19:00) + `selective-reindex.sh docs-courses`.

**Покрытие инструментов:**

| guides-mcp | knowledge-mcp | Статус |
|------------|---------------|--------|
| `semantic_search` | `search(source_type='guides')` | ✅ Покрыт |
| `get_section_content` | `get_document(filename)` | ✅ Покрыт |
| `get_guides_list` | — | ❌ → Фаза 1 |
| `get_guide_sections` | — | ❌ → Фаза 1 |

**Связи:** WP-73 задача 0.3 (Фаза 0: Фундамент), WP-5 (бот), WP-7 (техдолг)

</details>

*Создан: 2026-03-23*
