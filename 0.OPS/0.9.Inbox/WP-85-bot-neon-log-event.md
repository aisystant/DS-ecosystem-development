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

## Вопросы для обсуждения с архитектором

### Q1. Стратегия первичного ключа для таблицы `public.users` (блокер — WP-82/Ory)

**Контекст:** По архитектуре DP.ARCH.003 цифровой двойник должен иметь единую таблицу `public.users` с `id BIGSERIAL PRIMARY KEY` и маппингом на внешние идентификаторы (`telegram_id`, `lms_id`, `ory_id`, `discourse_username`). Сейчас в боте основная таблица пользователей — `interns`, где `chat_id BIGINT` является первичным ключом. На `chat_id` ссылаются ~15 таблиц и весь код бота.

Бот уже пишет события в `development.user_events`, используя `chat_id` как `user_id`. Когда появится Ory и `public.users`, потребуется миграция.

**Варианты:**
- **Вариант A (рекомендуемый):** Добавить колонку `id BIGSERIAL` к таблице `interns` параллельно с существующим `chat_id`. Таблица `public.users` создаётся как VIEW или алиас поверх `interns`. Бот продолжает работать с `chat_id` без изменений. Минимальный риск — ничего не ломается.
- **Вариант B:** Создать новую таблицу `public.users` с `id BIGSERIAL PRIMARY KEY`. Постепенно мигрировать все внешние ключи (~15 таблиц) и весь код бота с `chat_id` на `users.id`. Высокий риск — требует масштабного рефакторинга.
- **Вариант C:** Оставить `chat_id` как первичный ключ. Колонку `id` добавить позже, когда появится web-приложение. Технический долг откладывается.

**Зависимость:** Решение блокируется WP-82 (упрощённый онбординг с Ory). До появления Ory бот пишет `chat_id` напрямую в `user_events.user_id`.

### Q2. Разделение операционных и идентификационных данных пользователя

**Контекст:** Таблица `interns` содержит ~40 полей, смешивая идентификационные данные с операционными. По архитектуре `public.users` должен хранить только identity-данные (8 полей: id, telegram_id, name, language, timezone и т.д.). Операционные данные — это:
- Состояние конечного автомата: `mode`, `current_state`, `marathon_status`, `feed_status`
- Настройки обучения: `schedule_time`, `complexity_level`, `current_context`
- Метрики вовлечённости: `active_days_streak`, `longest_streak` (в будущем будут вычисляться из Events — Layer 1 цифрового двойника)

**Варианты:**
- **Вариант A:** Переименовать `interns` в `operations.user_state`. Создать чистую `public.users` рядом с только identity-полями. Чёткое разделение, но требует обновления всех запросов к `interns`.
- **Вариант B (рекомендуемый):** Создать `public.users` с 8 identity-полями. Таблица `interns` продолжает существовать под старым именем — бот работает с ней как раньше. Постепенная миграция: новый код обращается к `public.users` за identity, к `interns` за операционными данными. Не ломает бота.

**Зависимость:** Ждёт WP-82 (Ory), так как identity-поля связаны с единой авторизацией.

### Q3. План миграции `user_events.user_id` при появлении Ory

**Контекст:** Сейчас `development.user_events.user_id` содержит `chat_id` (Telegram ID). Когда будет создана `public.users` с `id BIGSERIAL`, нужно будет:
1. Создать маппинг `chat_id → users.id` через таблицу `public.users`
2. Выполнить batch UPDATE всех существующих записей в `user_events`: заменить `chat_id` на `users.id`
3. Добавить FK constraint: `ALTER TABLE development.user_events ADD FOREIGN KEY (user_id) REFERENCES public.users(id)`
4. Обновить код `log_event()` в боте: резолвить `chat_id → users.id` перед записью

**Вопрос:** Кто и когда выполняет эту миграцию? Варианты:
- Автоматический скрипт при первом старте после развёртывания Ory
- Ручной скрипт, запускаемый разработчиком
- Часть миграции WP-82

### Q4. Достаточность метрик Engagement View (Layer 2)

**Контекст:** Создан SQL View `development.engagement` — первая проекция Layer 2 цифрового двойника. View агрегирует данные из `user_events` по каждому пользователю и содержит 15 метрик:

| Метрика | Описание |
|---------|----------|
| `sessions_total` | Общее количество сессий |
| `ai_chats_total` | Количество вопросов ИИ-консультанту |
| `marathon_steps_total` | Пройденные шаги марафона (уроки + вопросы) |
| `marathon_tasks_total` | Сданные рабочие продукты |
| `feed_completed_total` | Завершённые дайджесты Ленты (с фиксацией) |
| `training_attempts_total` | Попытки тренировки принципов |
| `training_passed_total` | Успешные попытки тренировки |
| `assessments_total` | Пройденные тесты систематичности |
| `events_total` | Общее количество событий |
| `first_event_at` / `last_event_at` | Даты первого и последнего событий |
| `active_days` | Количество уникальных дней с активностью |
| `events_last_7d` / `events_last_30d` | Активность за последние 7 и 30 дней |

**Вопрос:** Достаточно ли этих метрик для Layer 2, или нужны дополнительные проекции? Возможные расширения:
- `skill_mastery` — уровень освоения компетенций (на основе `skill_ids` и `confidence`)
- `learning_velocity` — скорость прогресса (события в единицу времени, тренд)
- `engagement_score` — составная метрика вовлечённости

### Q5. Архитектура HTTP API для записи событий из LMS и Клуба

**Контекст:** Бот пишет события напрямую в Neon через asyncpg (он работает в том же процессе, что и подключение к БД). LMS (Java-бэкенд Aisystant) и Клуб (Discourse) — внешние системы, которым нужен HTTP endpoint для записи событий в `development.user_events`.

**Вопросы для решения:**
- **Технология:** FastAPI-сервис (полноценный API) или Cloudflare Worker / Cloud Function (serverless, дешевле)?
- **Аутентификация:** API key (простой, для server-to-server) или Ory token (единая авторизация, но сложнее)?
- **Размещение кода:** Отдельный репозиторий `DS-digital-twin-api` или скрипты в `DS-ecosystem-development`?
- **Формат событий:** Использовать CloudEvents envelope (DP.SOTA.003) или собственный формат, совместимый с текущим `log_event()`?

---

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
