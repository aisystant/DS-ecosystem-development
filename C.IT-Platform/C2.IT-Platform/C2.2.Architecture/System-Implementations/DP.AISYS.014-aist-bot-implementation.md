---
source: PACK-digital-platform/pack/digital-platform/02-domain-entities/DP.AISYS.014-aist-bot.md
type: implementation-extract
created: 2026-03-13
summary: "Реализационные детали AIST Bot: SM architecture, integrations, DB mapping, WP model, issue funnel"
---

# AIST Bot — Implementation Details

> **Source-of-truth (домен):** [DP.AISYS.014-aist-bot.md](../../../../../PACK-digital-platform/pack/digital-platform/02-domain-entities/DP.AISYS.014-aist-bot.md)
>
> Этот файл содержит **реализационные детали** (HD #29: «заменишь вендора — утверждение станет ложным»). Доменные принципы остаются в Pack.

---

## 6. Текущая реализация

### 6.1. State Machine

**Архитектура:** YAML-driven State Machine (transitions.yaml -> states/ -> handlers/).

```
Telegram Update -> Middleware -> Router -> Dispatcher -> SM.handle()
  -> Current State.handle() -> event -> transitions.yaml -> Next State.enter()
```

### 6.2. Режимы обучения (mode-aware routing)

| Режим | Стейты | Как попасть |
|-------|--------|------------|
| **Марафон** | workshop.marathon.* (lesson -> question -> bonus -> task) | /learn при mode=marathon |
| **Лента** | feed.* (topics -> digest) | /learn при mode=feed |

**`get_user_mode_state(user)`** — единая точка определения целевого стейта по режиму.

### 6.3. Интеграции

| Система | Интерфейс | Текущий статус |
|---------|-----------|----------------|
| Claude API (Sonnet + Haiku, model routing) | `clients/claude.py` | Active |

#### 6.3.1. Model Routing (Route-by-Complexity)

Бот использует два Claude-модели с роутингом по сложности задачи:

| Модель | Задачи | Критерий |
|--------|--------|----------|
| **Haiku** | Feed «почему это важно», FAQ L1/L2, /mydata | Структурированный вывод, latency-critical |
| **Sonnet** | Уроки, практика, вопросы, консультации L3, tool_use | Креативный/аналитический вывод |

**Принцип:** дешёвая модель для структурированных задач, мощная — для creative reasoning. Вызывающий код передаёт `model=CLAUDE_MODEL_HAIKU` явно; default = Sonnet. Экономия: ~40% стоимости API при сохранении качества ответов.
| knowledge-mcp v3.1 (CF Workers AI, bge-m3) | `clients/mcp.py`, `core/knowledge.py` | Active |
| PostgreSQL (Neon.com, asyncpg) | `db/`, asyncpg pool | Active |
| aiogram 3.x | Telegram Bot Framework | Active |
| GitHub API (OAuth) | `clients/github_api.py` | Active |
| Стратег (TG integration) | `notify.sh` + `/rp`, `/plan`, `/report` | Active |
| Цифровой двойник | `clients/digital_twin.py` | In progress |

---

## 4.5.1. Маппинг данных: Бот -> Цифровой двойник

При подключении ЦД (Настройки -> Подключения -> Цифровой двойник) данные из БД бота автоматически переливаются в `1_declarative` секцию ЦД.

**Когда происходит перелив:**

1. **При подключении** — сразу после OAuth авторизации все 10 полей переливаются автоматически (полный sync в `oauth_server.py:twin_callback_handler`)
2. **При обновлении профиля** — каждое сохранение поля в боте (через `update_intern`) автоматически синхронизирует изменённое поле в ЦД (инкрементальный sync, fire-and-forget)
3. **Ежечасная проверка** — scheduler проверяет подключённых пользователей и досинхронизирует если предыдущий sync не удался (`core/scheduler.py:_sync_dt_connected_users`)

**Реализация:** `clients/digital_twin.py` -> `PROFILE_DT_MAPPING`, `sync_profile()`, `sync_fields()`

| # | Поле бота (DB) | Путь в ЦД | Индикатор | Конвертация |
|---|---------------|-----------|-----------|-------------|
| 1 | `name` | `1_declarative/1_1_profile/02_Имя` | IND.1.1.2 | string -> string |
| 2 | `occupation` | `1_declarative/1_1_profile/01_Занятие` | IND.1.1.1 | string -> string |
| 3 | `interests` | `1_declarative/1_2_goals/01_Интересы` | IND.1.2.1 | string -> string (список через запятую) |
| 4 | `goals` | `1_declarative/1_2_goals/09_Цели обучения` | IND.1.2.2 | string -> string |
| 5 | `role` | `1_declarative/1_3_selfeval/06_Роли` | IND.1.3.3 | string -> string |
| 6 | `study_duration` | `1_declarative/1_3_selfeval/11_Срок обучения` | IND.1.3.6 | string -> string |
| 7 | `current_problems` | `1_declarative/1_4_context/01_Текущие проблемы` | IND.1.4.1 | string -> string |
| 8 | `desires` | `1_declarative/1_4_context/02_Желания` | IND.1.4.2 | string -> string |
| 9 | `schedule_time` | `1_declarative/1_4_context/05_Режим обучения` | IND.1.4.5 | time string -> string |
| 10 | `feed_schedule_time` | `1_declarative/1_4_context/04_Удобное время` | IND.1.4.4 | time string -> string |

**Не переливаются (системные поля бота):** `telegram_id`, `language`, `experience_level`, `marathon_completed`.

---

## 8.1. Модель сопровождения (Umbrella WP)

Бот — система с непрерывной работой. Для управления используется **гибридная модель (Variant C)**:

| Тип РП | Номер | Что содержит | Context file |
|--------|-------|-------------|--------------|
| **Развитие** (зонтичный) | WP #5 | Фичи из MAPSTRATEGIC, backlog 10-20 пунктов | `WP-5-bot-ux-ui.md` |
| **Техдолг** (зонтичный) | WP #7 | Баги, latency, cleanup, code TODOs | `WP-7-bot-tech-debt.md` |
| **Крупная фича** (эпизодический) | WP #N | Задача >=4h с отдельным lifecycle | Создаётся -> делается -> архивируется |

**Правило отсечки:** >=4h или отдельный definition of done -> эпизодический РП.
**Примеры эпизодических:** Stars (#9), Feed pre-gen (#37), миграция DB (#27), Railway->EU (#38).
**Гигиена:** Done-пункты удаляются из context file, не накапливаются. Каждую неделю в WeekPlan — конкретный scope.

#### Issue Funnel (Воронка замечаний) — v2 DB-native

Двухуровневый триаж: auto-classify в реальном времени + review при сессии.

```
helpful=false / ✏️ comment
        |
        v
core/feedback_triage.py (Bot, Haiku)
        |
        |-> 1. LLM classify -> category (L/C/U/K) + severity + cluster
        |-> 2. INSERT feedback_triage (DB)
        |-> 3. IF severity>=high OR ✏️ -> TG alert СРАЗУ
        |
        v
unsatisfied-report.sh (daily)
        |
        v
unsatisfied-questions.md = REPORT (не inbox)
  структура: ✏️ замечания -> 🔴 urgent -> 📊 кластеры -> 📈 статистика

                            +-->  Review (Open WP-7) --> WP-7 backlog
feedback_triage DB ---------+      1. Читай structured report
fleeting-notes.md ----------+      2. Review предклассифицированного
captures.md ----------------+      3. Бюджет + приоритет
```

**Процесс:** бот PROCESSES.md § 6 (Issue Triage, двухуровневый).

---

## 9. Реализация (Downstream)

| Репо | Ветка | Статус |
|------|-------|--------|
| [DS-IT-systems/aist_bot_newarchitecture](https://github.com/TserenTserenov/DS-IT-systems) | new-architecture | Active |
