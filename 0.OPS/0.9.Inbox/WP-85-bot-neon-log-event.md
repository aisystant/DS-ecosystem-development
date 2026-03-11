---
title: "Реализация log_event() в боте — первый продьюсер ЦД"
type: design-proposal
status: for-review
created: 2026-03-11
author: Claude (Разработчик R4)
reviewer: Архитектор
depends_on:
  - DP.ARCH.003 (3-слойная архитектура ЦД)
  - WP-85 (Реализация ЦД в Neon)
related:
  - Структура данных ЦД в Neon — предложение для архитектора.md
  - Предложение — 3-слойная архитектура цифрового двойника.md
  - WP-73 (Архитектура ИТ-платформы)
  - WP-82 (Упрощённый онбординг с Ory)
---

# Реализация log_event() в боте — первый продьюсер ЦД

## 1. Суть предложения

Бот становится **первым продьюсером событий** в `development.user_events` (Neon). Это прототип паттерна, по которому затем подключатся LMS, Клуб и Web App.

**Принцип:** единая точка записи `log_event()` → единая таблица `user_events` → append-only.

## 2. Архитектура записи событий

### 2.1. Общая схема (все продьюсеры)

```
Бот (TG)  ──→ log_event() напрямую ──┐
LMS       ──→ HTTP webhook → API ────┤──→ development.user_events (Neon)
Клуб      ──→ HTTP webhook → API ────┤
Web App   ──→ напрямую / API ────────┘
```

### 2.2. Идентификация пользователей

Сейчас у каждой системы свой ID:
- Бот: `chat_id` (Telegram)
- LMS: `lms_id` (Java-бэкенд)
- Клуб: `discourse_username`

**Решение на текущем этапе:** бот пишет `chat_id` в поле `user_id` таблицы `user_events`. Когда появится Ory и `public.users` (WP-82), добавим маппинг:

```
public.users.id  ← единый PK
  ├── telegram_id (= chat_id)
  ├── lms_id
  ├── ory_id
  └── discourse_username
```

**Миграция:** ALTER `user_events.user_id` → FK на `public.users.id` + batch UPDATE через маппинг `chat_id → users.id`. Обратно-совместимо: старые записи сохраняются.

### 2.3. Роль Ory

Ory (WP-82, зависит от WP-73) обеспечит:
- Единый `ory_id` для SSO между системами
- OAuth2/OIDC для LMS и Клуба
- `public.users.ory_id` как связующее звено

**Ory НЕ блокирует запись событий.** Бот может писать по `chat_id` уже сейчас. LMS/Клуб подключатся через webhook после развёртывания API-слоя.

## 3. Что реализуется в боте (Фаза 1)

### 3.1. Schema + таблица

```sql
CREATE SCHEMA IF NOT EXISTS development;

CREATE TABLE IF NOT EXISTS development.user_events (
    id BIGSERIAL PRIMARY KEY,
    user_id BIGINT NOT NULL,          -- chat_id (пока без FK)
    event_type TEXT NOT NULL,          -- 'session_start', 'ai_chat', 'marathon_step'
    source TEXT NOT NULL DEFAULT 'bot',
    payload JSONB DEFAULT '{}',
    confidence REAL DEFAULT 1.0,       -- 0.0–1.0
    skill_ids TEXT[] DEFAULT '{}',
    created_at TIMESTAMPTZ DEFAULT NOW()
);
```

Партиционирование — **отложено** до >100K записей. На текущих объёмах (~100 пользователей) обычная таблица + индексы.

### 3.2. Функция log_event()

```python
async def log_event(
    user_id: int,
    event_type: str,
    payload: dict = None,
    confidence: float = 1.0,
    skill_ids: list = None,
    source: str = 'bot',
) -> int | None:
```

- Fire-and-forget (ошибка не ломает основной flow)
- Возвращает `id` записи или `None` при ошибке
- `TIMESTAMPTZ` — asyncpg корректно работает с aware datetime

### 3.3. P0 точки интеграции (3 события)

| Событие | Где врезается | payload |
|---------|---------------|---------|
| `session_start` | `db/queries/sessions.py` (новая сессия) | `{entry_point}` |
| `ai_chat` | `clients/claude_client.py` или handler Q&A | `{mode, question_length, has_tool_use}` |
| `marathon_step` | SM state lesson/question completion | `{topic_index, topic_id, complexity_level, answer_type}` |

### 3.4. Затронутые сервисы (MAP.002)

- **S12 (Q&A)** → событие `ai_chat`
- **S16 (Marathon Step)** → событие `marathon_step`
- Session tracking → событие `session_start`

## 4. Что НЕ делается сейчас

- `public.users` (ждёт WP-82/Ory)
- Партиционирование (малые объёмы)
- State-проекции (skill_mastery, engagement) — Фаза 2
- HTTP API для LMS/Клуба — Фаза 3
- RLS (Row-Level Security) — после появления multi-tenant доступа

## 5. Принятые решения (из WP-85 вопросов)

| Вопрос | Решение | Обоснование |
|--------|---------|-------------|
| 3. Database | Schemas в `aisybot` (вариант B) | JOIN работает, проще |
| 4. Timestamps | `TIMESTAMPTZ` для `development.*` | Стандарт для новых таблиц |
| 5. Миграции | В models.py бота (inline) | Бот = первый потребитель, миграция идемпотентна |
| 1. PK users | Отложен до WP-82 | Бот пишет chat_id напрямую |
| 2. Операционные поля | Отложен до WP-82 | interns живёт как есть |

**Вопрос 5 уточнение:** Миграция schema `development` живёт в боте как первом потребителе. Когда появится платформенный миграционный инструмент (DS-ecosystem-development), миграция переедет туда.

## 6. Паттерн для будущих продьюсеров

```
1. Продьюсер вызывает log_event(user_id, event_type, payload, confidence)
2. user_id = идентификатор в системе продьюсера (chat_id / lms_id / ...)
3. source = 'bot' / 'lms' / 'club' / 'web_app'
4. После создания public.users — user_id станет FK на users.id
5. Маппинг: каждый продьюсер резолвит свой ID → users.id перед записью
```

LMS и Клуб будут писать через HTTP endpoint (FastAPI или аналог), который внутри вызывает тот же `log_event()`.

---

*Ожидает согласования архитектора.*
