---
type: work-package
number: 168
title: "Миграция guides-mcp: SurrealDB → Neon"
status: pending
budget: "3-5h"
created: 2026-03-23
parent: WP-73
repo: DS-MCP
artifact: "guides-mcp работает на Neon, SurrealDB выведен из стека"
---

# РП #168: Миграция guides-mcp: SurrealDB → Neon

## Предложение (на согласование)

Перевожу платформенный guides-mcp с SurrealDB на Neon. guides-mcp остаётся как отдельный MCP (L2 Platform) — исключительно поиск по руководствам, без примеси личных знаний.

### Текущая ситуация

- **CI сломан с 12 февраля** — все 5 последних запусков `publish-to-surreal.yaml` = failure (`401 Unauthorized` к `surrealdb.aisystant.com`). Данные в SurrealDB не обновляются >1 месяца
- **Latency** — 17-20 сек на запрос (SurrealDB vector scan)
- **Данные уже в Neon** — `ingest.ts` индексирует те же гайды как source `docs-courses` (2697 docs, CF AI 1024d, HNSW). Переиндексация еженедельно (`reindex.sh`)

### Решения

| # | Решение | Обоснование |
|---|---------|-------------|
| 1 | **guides-mcp остаётся** как отдельный платформенный MCP (L2) | Чистый поиск по руководствам, без личных Pack. knowledge-mcp = L4 Personal |
| 2 | **Переписать guides-mcp на Neon** (вместо SurrealDB) | Читает из той же `documents` (source=`docs-courses`). Latency <1 сек |
| 3 | **CI: `publish-to-surreal` → `publish-to-neon`** или удалить | `ingest.ts` + `reindex.sh` уже покрывают. CI нужен только если хотим обновлять при каждом push в `docs/` |
| 4 | **SurrealDB — выключить** | Больше ни один сервис не использует |

### Что нужно от архитектора

| # | Вопрос | Зачем |
|---|--------|-------|
| 1 | **Согласовать решения 1-4** | Без согласования не начинаем |
| 2 | **Кто управляет `surrealdb.aisystant.com`?** | Чтобы выключить сервер |
| 3 | **Credentials SurrealDB** — что случилось? Почему 401 с 12 февраля? | Понять, не сломалось ли что-то ещё |
| 4 | **Доступ к GitHub Secrets** репо `docs` | Обновить/удалить workflow. Tseren = admin? |
| 5 | **CF Workers деплой** — может ли Tseren деплоить через `wrangler`? | Деплой обновлённого guides-mcp |

**Если доступы 4-5 есть** → делаем сами, архитектор: п.1 + п.2 + п.3.

### План

**Фаза 1.** Переписать `guides-mcp/src/index.ts`: SurrealDB → Neon (`documents` WHERE source=`docs-courses`). 4 инструмента сохраняются. ~2-3h

**Фаза 2.** CI: удалить `publish-to-surreal.yaml` (или заменить на `selective-reindex.sh docs-courses`). Удалить `docs/scripts/publish_to_surreal/`

**Фаза 3.** Выключить `surrealdb.aisystant.com`. Удалить `migrate-guides.ts`. Обновить MAP.002, MEMORY.md, WP-73 §3.8.4

### Результат

| Метрика | Было | Станет |
|---------|------|--------|
| Latency поиска | 17-20 сек | <1 сек |
| Данные актуальны | Нет (CI сломан с 12 фев) | Да (Neon, еженедельный reindex) |
| Внешние БД | Neon + SurrealDB | Neon |
| guides-mcp | Платформенный, отдельный | Платформенный, отдельный (на Neon) |

*Создан: 2026-03-23*
