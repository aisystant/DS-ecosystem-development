---
title: "Структура данных ЦД в Neon — предложение для архитектора"
type: architecture-proposal
status: for-review
created: 2026-02-26
updated: 2026-02-26
author: Tseren + Claude (Opus)
reviewer: Архитектор
depends_on: DP.ARCH.003
related:
  - "Предложение — 3-слойная архитектура цифрового двойника.md"
  - "DP.ARCH.003-digital-twin-architecture.md"
---

# Структура данных ЦД в Neon — предложение для архитектора

> **Контекст:** [DP.ARCH.003](https://github.com/TserenTserenov/PACK-digital-platform/blob/main/pack/digital-platform/02-domain-entities/DP.ARCH.003-digital-twin-architecture.md) описывает 3-слойную архитектуру ЦД (Events → State → Views). Этот документ — **как конкретно организовать хранение в Neon PostgreSQL** с учётом бота, будущего Web App, Activity Hub, финансов (включая роялти авторам) и безопасности.
>
> **Важно:** Цифровой двойник — это ВСЯ база данных целиком, а не отдельная schema. Каждая schema отвечает за свой домен, но вместе они составляют полный ЦД созидателя.

---

## 1. Итоговая схема

```
Проект Neon: aisystant (ОДИН проект, ОДНА database)
│
└── database: aisystant
    │
    ├── schema: public                      [Идентичность пользователя]
    │   └── users                           ← Канонический профиль пользователя
    │       id, telegram_id, email,            Один пользователь — много входов.
    │       lms_id, ory_id, name,              Связка тиров: бот → web → LMS.
    │       language, current_tier,             FK для всех остальных таблиц.
    │       created_at, updated_at
    │
    ├── schema: development                 [Развитие: события + проекции]
    │   │
    │   │  Events (append-only, неизменяемый лог)
    │   ├── user_events                     ← ВСЕ действия из ВСЕХ систем
    │   │   PARTITIONED BY RANGE (created_at)  Append-only. Никогда не UPDATE/DELETE.
    │   │   Источники: бот, LMS, клуб, web app.
    │   │   Содержимое (ответы, тексты) — в payload (JSONB).
    │   │   Декларации пользователя — тоже Events (confidence=0.3-0.5).
    │   │   4 направления: себя, других, сообщества, экосистемы.
    │   │
    │   │  State projections (вычисляемые из Events)
    │   │  Начальные проекции (Фаза 1-2), архитектура поддерживает N:
    │   ├── skill_mastery                   ← State projection (BKT): P(known) по навыкам
    │   ├── memory_decay                    ← State projection (HLR): полураспад, spaced repetition
    │   ├── engagement                      ← State projection (агрегаты): streak, регулярность
    │   ├── misconceptions                  ← State projection (LLM): карта заблуждений
    │   └── qualifications                  ← State projection (threshold rules): стадия
    │
    │      Views — НЕ хранятся. Вычисляются на лету
    │      (рекомендации, отчёты, Open Learner Model).
    │      Факт показа View → Event в user_events.
    │
    ├── schema: finance                     [Финансы, токены, роялти]
    │   ├── token_transactions              ← Лог начислений/списаний токенов
    │   ├── token_balances                  ← Текущий баланс (проекция)
    │   ├── subscriptions                   ← Подписки (Telegram Stars, web)
    │   ├── payments                        ← Входящие платежи
    │   ├── royalty_rules                   ← Правила: автору X% за руководство Y
    │   ├── royalty_distributions           ← Факт: автору начислено Z₽ за период
    │   └── referral_rewards                ← Реферальные бонусы
    │
    ├── schema: connections                 [Подключения к внешним системам]
    │   ├── oauth_tokens                    ← GitHub, LMS, ORY (pgcrypto encrypted)
    │   ├── api_keys                        ← WakaTime
    │   └── external_accounts               ← Discourse, LMS accounts
    │
    └── schema: operations                  [Служебное: FSM, кэш, контент, мониторинг]
        ├── fsm_states                      ← Telegram FSM (состояние диалога)
        ├── content_cache                   ← Временный кэш (TTL)
        ├── marathon_content                ← Контент доставки (шаблоны уроков)
        ├── feed_weeks / feed_sessions      ← Расписание доставки контента
        ├── scheduled_publications          ← Планы публикаций
        ├── error_logs                      ← Ошибки
        ├── pending_fixes                   ← AutoFix
        ├── request_traces                  ← Observability
        ├── feedback_reports                ← Тикеты
        └── feedback_triage                 ← Автотриаж
```

---

## 2. Почему именно эти schemas: критерии и обоснования

### 4 критерия разделения на schemas

| # | Критерий | Вопрос | Если «нет» |
|---|----------|--------|-----------|
| 1 | **Один домен** | Все таблицы отвечают на один вопрос? | Разнести по разным schemas |
| 2 | **Независимый жизненный цикл** | Данные меняются по своему ритму? | Могут жить вместе |
| 3 | **Независимый доступ** | Разные сервисы/роли обращаются? | Могут жить вместе |
| 4 | **Тест канала** | Если убрать один канал (бот, web), домен останется? | Это домен, а не канал |

### Обоснование каждой schema

| Schema | Домен | Вопрос, на который отвечает | Почему отдельная |
|--------|-------|----------------------------|-----------------|
| `public` | Идентичность | «Кто этот пользователь?» | PostgreSQL default. ТОЛЬКО каноническая идентичность (users). FK для всех остальных schemas. Контент и расписание — в operations (служебная механика). Действия пользователя — events в development |
| `development` | Развитие | «Что делал, что знает и куда движется этот созидатель?» | Ядро ЦД. Все 4 направления развития (себя, других, сообщества, экосистемы) — единый поток событий. Свой жизненный цикл: append-only events + пересчитываемые проекции. Отдельный доступ: BKT-модуль, MCP, аналитик |
| `finance` | Финансы | «Сколько заплатил, сколько заработал, сколько на балансе?» | Другой bounded context. Финансы требуют аудит-трейла, reconciliation, роялти-распределение. Свой жизненный цикл (месячные периоды, выплаты). Доступ: финансист видит finance, но НЕ видит development |
| `connections` | Подключения | «Как подключены GitHub, LMS, WakaTime?» | Секреты (pgcrypto). Минимальный доступ — только сервис аутентификации. Если убрать WakaTime — development не пострадает |
| `operations` | Служебное | «Какое состояние FSM, кэш, контент доставки, ошибки?» | Эфемерные и служебные данные: FSM, кэш, расписание контента, шаблоны уроков, мониторинг. Можно полностью дропнуть без потерь для ЦД |

### Почему НЕ выделены отдельно

| Кандидат | Решение | Причина |
|----------|---------|---------|
| **schema: bot** | Не нужна | Бот — канал ввода, не домен. Не проходит тест канала: данные обучения принадлежат development, финансы — finance |
| **schema: gamification** | Не нужна | Токены/баллы — это финансы (finance). Стадии/квалификации — это проекция (development.qualifications) |
| **schema: learning** | Не нужна | Обучение — процесс. Его результаты = развитие (development). Ложное разделение: события обучения питают те же проекции |
| **schema: digital_twin** | Не нужна | ЦД = ВСЯ база целиком, а не одна schema. Назвать одну schema «digital_twin» = сказать, что остальные — не часть ЦД |

### Принцип именования

Все имена — **существительные-домены одного типа**: что содержит schema (development, finance, connections, operations). Не: кто использует (bot), не: процесс (billing), не: прилагательное (operational).

---

## 3. Bounded contexts (5 schemas)

| Schema | Bounded Context | Можно дропнуть без потерь? |
|--------|----------------|---------------------------|
| `public` | Идентичность (только users) | Нет |
| `development` | Развитие созидателя (все 4 направления) | Нет |
| `finance` | Финансы, токены, роялти | Нет |
| `connections` | Внешние подключения (секреты) | Нет (секреты) |
| `operations` | Эфемерное (FSM, кэш, логи) | Да |

### Ключевые решения

| Решение | Обоснование |
|---------|-------------|
| **Один проект Neon, одна database** | JOIN между schemas. Единый billing. При <1K пользователей отдельный проект — overengineering |
| **Schemas вместо databases** | Логическая изоляция + RLS. Таблицы видят друг друга через cross-schema FK |
| **Бот НЕ выделен в schema** | Бот — канал ввода, не домен. Данные развития = development, финансы = finance, служебное = operations |
| **`finance` — отдельная schema** | Баланс токенов — не характеристика созидателя, а операционный показатель платформы. Роялти, подписки, платежи — отдельный bounded context со своим аудитом. Начальные проекции ЦД — про развитие, token_balances среди них нет |
| **`operations` — отдельная schema** | Явно маркирует эфемерные данные. Без неё `public` превращается в свалку за полгода |

---

## 4. Ключевые таблицы: детали

### 4.1 public.users — Канонический профиль

```sql
CREATE TABLE public.users (
    id              BIGSERIAL PRIMARY KEY,

    -- Идентификаторы (один пользователь — много входов)
    telegram_id     BIGINT UNIQUE,
    email           TEXT UNIQUE,
    lms_id          TEXT UNIQUE,
    ory_id          TEXT UNIQUE,

    -- Профиль
    name            TEXT DEFAULT '',
    language        TEXT DEFAULT 'ru',
    current_tier    INTEGER DEFAULT 1,    -- 1=бот, 2=бот+web, 3=полный

    created_at      TIMESTAMPTZ DEFAULT NOW(),
    updated_at      TIMESTAMPTZ DEFAULT NOW()
);
```

**Переход между тирами:**

```
Тир 1: telegram_id заполнен, email = NULL     ← онбординг через бота
Тир 2: telegram_id + email                    ← добавил web app
Тир 3: все ID связаны                         ← полная интеграция
```

Декларации пользователя (цели, интересы, самооценка) — НЕ здесь. Они записываются как Events в `development.user_events` с типами `goal_set`, `self_assessed`, `profile_updated`. Причина: декларации меняются со временем → нужна история.

### 4.2 development.user_events — Единый лог действий (Events)

```sql
CREATE TABLE development.user_events (
    id              BIGSERIAL,
    user_id         BIGINT NOT NULL REFERENCES public.users(id),
    event_type      TEXT NOT NULL,
    source          TEXT NOT NULL,         -- 'bot', 'lms', 'club', 'web_app'
    payload         JSONB NOT NULL DEFAULT '{}',
    confidence      REAL DEFAULT 1.0,     -- 0.0-1.0
    skill_ids       TEXT[] DEFAULT '{}',
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    PRIMARY KEY (id, created_at)
) PARTITION BY RANGE (created_at);

-- Партиции по месяцам
CREATE TABLE development.user_events_2026_03
    PARTITION OF development.user_events
    FOR VALUES FROM ('2026-03-01') TO ('2026-04-01');

-- Индексы
CREATE INDEX idx_events_user_time
    ON development.user_events (user_id, created_at DESC);
CREATE INDEX idx_events_type
    ON development.user_events (event_type, created_at DESC);
CREATE INDEX idx_events_skills
    ON development.user_events USING GIN (skill_ids);
```

**Каталог типов событий:**

| event_type | source | Что в payload | confidence |
|---|---|---|---|
| `test_answered` | bot, lms | question, skill, answer, correct, feedback | 0.9 |
| `homework_submitted` | lms | homeworkId, skillIds[], score | 0.9 |
| `marathon_step` | bot | lessonId, stepId, completed, timeSpentMs | 0.9 |
| `feed_answered` | bot | questionId, answer, correct | 0.9 |
| `ai_chat` | bot | sessionId, message, extractedSkills[] | 0.5 |
| `note_created` | bot | text, tags[] | 0.7 |
| `post_published` | club | topicId, title | 0.9 |
| `comment_created` | club | topicId, text | 0.7 |
| `referral_completed` | web | invitedUserId | 1.0 |
| `session_start` | bot, web | platform | 1.0 |
| `goal_set` | bot, web | goal, targetSkill | 1.0 |
| `self_assessed` | bot | skillId, selfRating | 0.3 |
| `profile_updated` | bot, web | field, oldValue, newValue | 1.0 |
| `recommendation_shown` | system | skill, text, reason | 1.0 |
| `report_generated` | system | period, summary | 1.0 |
| `tokens_earned` | system | amount, reason, referenceEventId | 1.0 |
| `tokens_spent` | web | amount, item | 1.0 |
| `payment_completed` | finance | paymentId, amount, currency | 1.0 |
| `subscription_started` | finance | plan, expiresAt | 1.0 |
| `seminar_attended` | bot, web | seminarId, title, duration | 0.9 |
| `practicum_step` | bot, lms | practicumId, stepId, completed | 0.9 |
| `residency_progress` | lms | residencyId, milestone, status | 0.9 |
| `guide_published` | web | guideId, title, domain | 0.9 |
| `guide_reviewed` | club | guideId, reviewerId, score | 0.8 |
| `question_answered` | club | topicId, helpedUserId | 0.8 |
| `peer_review` | club | reviewedUserId, feedback | 0.7 |

**Содержимое (ответы, тексты) хранится в payload.** Отдельные таблицы `answers`, `qa_history` не нужны — всё в Events.

**4 направления развития созидателя — в одном потоке событий:**

| # | Направление | Что делает | Примеры событий |
|---|-------------|-----------|----------------|
| 1 | **Развитие себя** | Учится, практикуется, рефлексирует, проходит программы | `test_answered`, `marathon_step`, `self_assessed`, `goal_set`, `seminar_attended`, `practicum_step`, `residency_progress`, `feed_answered` |
| 2 | **Развитие других** | Помогает другим в чатах, отвечает на вопросы, комментирует | `comment_created` (помощь), `question_answered`, `peer_review` |
| 3 | **Развитие сообщества** | Участвует в жизни сообщества, привлекает участников | `post_published`, `referral_completed`, `event_organized` |
| 4 | **Развитие экосистемы** | Создаёт руководства, методологии, внешние публикации | `guide_published`, `guide_reviewed`, `methodology_contributed` |

Все 4 направления различаются по `event_type`, а не по schema. Один поток → одна таблица → разные проекции.

### 4.3 State projections (development)

**Проекции — не фиксированный список.** Архитектура Event Sourcing позволяет создавать неограниченное число проекций из одного потока событий. Новая проекция = новая таблица + replay.

Ниже — **начальные 5 проекций** (Фаза 1-2). В модели характеристик созидателя описано 30+ измерений (6 кибер + 5 физических + 5 когнитивных + 5 социальных + 5 волевых + 4 интегральных), объединённых в CHR-Space — многомерное пространство состояний. Каждая характеристика потенциально = отдельная проекция или ось существующей.

**Источники:** Модель характеристик 2.2, CHR-Space созидателя, раздел 4.5 руководства «Методы саморазвития» (характеристики человека в системном контексте).

Начальные проекции (каждая — отдельная таблица, пересчитывается из Events):

```sql
-- State projection (BKT): Skill Mastery
-- Одна строка = один навык одного пользователя
CREATE TABLE development.skill_mastery (
    user_id         BIGINT NOT NULL REFERENCES public.users(id),
    skill_id        TEXT NOT NULL,
    p_known         REAL DEFAULT 0.1,
    bloom_depth     INTEGER DEFAULT 0,    -- 0-5
    attempts        INTEGER DEFAULT 0,
    correct_count   INTEGER DEFAULT 0,
    last_event_id   BIGINT,
    updated_at      TIMESTAMPTZ DEFAULT NOW(),
    PRIMARY KEY (user_id, skill_id)
);

-- State projection (HLR): Memory Decay
CREATE TABLE development.memory_decay (
    user_id         BIGINT NOT NULL REFERENCES public.users(id),
    skill_id        TEXT NOT NULL,
    half_life_days  REAL DEFAULT 1.0,
    p_recall_now    REAL DEFAULT 1.0,
    next_review_at  TIMESTAMPTZ,
    repetitions     INTEGER DEFAULT 0,
    updated_at      TIMESTAMPTZ DEFAULT NOW(),
    PRIMARY KEY (user_id, skill_id)
);

-- State projection (агрегаты): Engagement Profile
-- Одна строка = один пользователь
CREATE TABLE development.engagement (
    user_id                 BIGINT PRIMARY KEY REFERENCES public.users(id),
    streak_days             INTEGER DEFAULT 0,
    active_days_7d          INTEGER DEFAULT 0,
    active_days_30d         INTEGER DEFAULT 0,
    regularity              REAL DEFAULT 0.0,
    avg_session_min         REAL DEFAULT 0.0,
    preferred_hour          INTEGER,
    events_per_active_day   REAL DEFAULT 0.0,
    updated_at              TIMESTAMPTZ DEFAULT NOW()
);

-- State projection (LLM): Misconception Map
CREATE TABLE development.misconceptions (
    id              SERIAL PRIMARY KEY,
    user_id         BIGINT NOT NULL REFERENCES public.users(id),
    skill_id        TEXT NOT NULL,
    misconception   TEXT NOT NULL,
    evidence_count  INTEGER DEFAULT 1,
    confidence      REAL DEFAULT 0.5,
    first_seen_at   TIMESTAMPTZ DEFAULT NOW(),
    last_seen_at    TIMESTAMPTZ DEFAULT NOW()
);

-- State projection (threshold rules): Qualifications
CREATE TABLE development.qualifications (
    user_id         BIGINT PRIMARY KEY REFERENCES public.users(id),
    stage           TEXT DEFAULT 'random',
    mastery_index   REAL DEFAULT 0.0,
    agency_index    REAL DEFAULT 0.0,
    worldview_level INTEGER DEFAULT 0,
    updated_at      TIMESTAMPTZ DEFAULT NOW()
);

```

### 4.4 finance.* — Финансы, токены, роялти авторам

```sql
-- Токены: лог операций
CREATE TABLE finance.token_transactions (
    id              SERIAL PRIMARY KEY,
    user_id         BIGINT NOT NULL REFERENCES public.users(id),
    amount          INTEGER NOT NULL,         -- +50 или -100
    action_type     TEXT NOT NULL,            -- 'homework', 'post', 'referral',
                                              -- 'subscription', 'purchase', 'royalty'
    reference_type  TEXT,                     -- 'event', 'subscription', 'payment'
    reference_id    TEXT,                     -- ID источника
    metadata        JSONB DEFAULT '{}',
    created_at      TIMESTAMPTZ DEFAULT NOW()
);

-- Токены: текущий баланс (проекция из transactions)
CREATE TABLE finance.token_balances (
    user_id         BIGINT PRIMARY KEY REFERENCES public.users(id),
    total_tokens    INTEGER DEFAULT 0,
    loyalty_tier    INTEGER DEFAULT 1,        -- 1-5
    updated_at      TIMESTAMPTZ DEFAULT NOW()
);

-- Подписки
CREATE TABLE finance.subscriptions (
    id              SERIAL PRIMARY KEY,
    user_id         BIGINT NOT NULL REFERENCES public.users(id),
    provider        TEXT NOT NULL,            -- 'telegram_stars', 'stripe', 'manual'
    provider_id     TEXT,                     -- ID платежа в провайдере
    plan            TEXT NOT NULL,            -- 'basic', 'premium'
    status          TEXT DEFAULT 'active',    -- 'active', 'cancelled', 'expired'
    amount          INTEGER NOT NULL,         -- сумма в минимальных единицах
    currency        TEXT DEFAULT 'XTR',       -- 'XTR' (Stars), 'RUB', 'USD'
    started_at      TIMESTAMPTZ NOT NULL,
    expires_at      TIMESTAMPTZ NOT NULL,
    cancelled_at    TIMESTAMPTZ,
    created_at      TIMESTAMPTZ DEFAULT NOW()
);

-- Платежи (входящие)
CREATE TABLE finance.payments (
    id              SERIAL PRIMARY KEY,
    user_id         BIGINT NOT NULL REFERENCES public.users(id),
    provider        TEXT NOT NULL,
    provider_payment_id TEXT NOT NULL,
    amount          INTEGER NOT NULL,
    currency        TEXT NOT NULL,
    status          TEXT DEFAULT 'completed', -- 'pending', 'completed', 'refunded'
    metadata        JSONB DEFAULT '{}',
    created_at      TIMESTAMPTZ DEFAULT NOW()
);

-- Правила распределения авторам
CREATE TABLE finance.royalty_rules (
    id              SERIAL PRIMARY KEY,
    resource_type   TEXT NOT NULL,            -- 'guide', 'course', 'template'
    resource_id     TEXT NOT NULL,            -- ID руководства/курса
    author_user_id  BIGINT NOT NULL REFERENCES public.users(id),
    share_percent   REAL NOT NULL,            -- 0.0-1.0 (напр. 0.7 = 70%)
    active          BOOLEAN DEFAULT TRUE,
    created_at      TIMESTAMPTZ DEFAULT NOW(),
    UNIQUE(resource_id, author_user_id)
);

-- Факт распределений авторам
CREATE TABLE finance.royalty_distributions (
    id              SERIAL PRIMARY KEY,
    rule_id         INTEGER NOT NULL REFERENCES finance.royalty_rules(id),
    payment_id      INTEGER NOT NULL REFERENCES finance.payments(id),
    author_user_id  BIGINT NOT NULL REFERENCES public.users(id),
    amount          INTEGER NOT NULL,         -- сумма автору
    currency        TEXT NOT NULL,
    period_start    DATE NOT NULL,
    period_end      DATE NOT NULL,
    status          TEXT DEFAULT 'pending',   -- 'pending', 'paid', 'confirmed'
    paid_at         TIMESTAMPTZ,
    created_at      TIMESTAMPTZ DEFAULT NOW()
);

-- Реферальные бонусы
CREATE TABLE finance.referral_rewards (
    id              SERIAL PRIMARY KEY,
    referrer_id     BIGINT NOT NULL REFERENCES public.users(id),
    referred_id     BIGINT NOT NULL REFERENCES public.users(id),
    reward_type     TEXT NOT NULL,            -- 'tokens', 'discount', 'extension'
    reward_amount   INTEGER NOT NULL,
    trigger_event   TEXT NOT NULL,            -- 'registration', 'first_payment',
                                              -- 'subscription_active_30d'
    status          TEXT DEFAULT 'pending',   -- 'pending', 'granted', 'expired'
    granted_at      TIMESTAMPTZ,
    created_at      TIMESTAMPTZ DEFAULT NOW(),
    UNIQUE(referrer_id, referred_id, trigger_event)
);
```

**Как работает распределение авторам:**

```
Пользователь купил доступ к руководству «Методы саморазвития»
                    │
                    ▼
finance.payments: {user_id: 42, amount: 500, currency: 'RUB'}
                    │
                    ▼
finance.royalty_rules: resource='guide-self-dev',
                       author=77, share=0.70
                    │
                    ▼
finance.royalty_distributions: {
    author: 77,
    amount: 350,         ← 70% от 500
    status: 'pending'    ← ждёт выплаты
}
                    │
                    ▼ (ежемесячно)
status → 'paid', paid_at = NOW()
```

### 4.5 connections.* — Подключения к внешним системам

```sql
CREATE EXTENSION IF NOT EXISTS pgcrypto;

CREATE TABLE connections.oauth_tokens (
    user_id         BIGINT NOT NULL REFERENCES public.users(id),
    provider        TEXT NOT NULL,          -- 'github', 'lms', 'ory'
    access_token    BYTEA NOT NULL,         -- pgp_sym_encrypt(token, key)
    refresh_token   BYTEA,
    expires_at      TIMESTAMPTZ,
    created_at      TIMESTAMPTZ DEFAULT NOW(),
    PRIMARY KEY (user_id, provider)
);

CREATE TABLE connections.api_keys (
    user_id         BIGINT NOT NULL REFERENCES public.users(id),
    provider        TEXT NOT NULL,          -- 'wakatime'
    api_key         BYTEA NOT NULL,         -- pgp_sym_encrypt(key, secret)
    connected_at    TIMESTAMPTZ DEFAULT NOW(),
    PRIMARY KEY (user_id, provider)
);

CREATE TABLE connections.external_accounts (
    user_id         BIGINT NOT NULL REFERENCES public.users(id),
    provider        TEXT NOT NULL,          -- 'discourse', 'lms'
    external_username TEXT NOT NULL,
    metadata        JSONB DEFAULT '{}',
    connected_at    TIMESTAMPTZ DEFAULT NOW(),
    PRIMARY KEY (user_id, provider)
);
```

---

## 5. Потоки данных: как ЦД наращивается

```
┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐
│   Бот    │  │   LMS    │  │   Клуб   │  │ Web App  │
│ (T1)     │  │ (webhook)│  │ (webhook)│  │ (direct) │
└────┬─────┘  └────┬─────┘  └────┬─────┘  └────┬─────┘
     │             │             │              │
     ▼             ▼             ▼              ▼
┌──────────────────────────────────────────────────────┐
│  development.user_events (append-only)                │
│  = Activity Hub (единая точка записи)                 │
│                                                       │
│  Бот: log_event() напрямую (тот же Neon)              │
│  LMS/Клуб: HTTP webhook → API → INSERT               │
│  Web App: прямой INSERT (тот же Neon)                 │
└──────────────────┬───────────────────────────────────┘
                   │ on_event() / cron rebuild
      ┌────────────┼────────────┐
      ▼            ▼            ▼
┌──────────┐ ┌──────────┐ ┌──────────┐
│  skill   │ │ engage-  │ │ qualifi- │       ┌──────────────┐
│ mastery  │ │  ment    │ │ cations  │       │   finance.*  │
└──────────┘ └──────────┘ └──────────┘       │  (отдельный  │
      │            │            │            │   BC)        │
      └────────────┼────────────┘            └──────┬───────┘
                   ▼                                │
         ┌─────────────────┐                        │
         │  Views (на лету) │                        │
         │  Рекомендации    │    tokens_earned ──────┘
         │  Open Learner    │    payment_completed
         │  Model           │
         └────────┬────────┘
                  │
                  ▼
         Event: recommendation_shown
         (цикл замыкается)
```

**Activity Hub — не отдельный сервис.** Это функция `log_event()` + HTTP endpoint для внешних источников. Всё пишется в одну таблицу `development.user_events`.

**Каждый новый источник** (LMS, клуб, реферальная программа) — это новый producer, который пишет в ту же таблицу. Проекции автоматически учитывают новые типы событий.

**Связь Events → Finance:** события `tokens_earned`, `payment_completed`, `subscription_started` пишутся и в `development.user_events` (для ЦД-аналитики), и в `finance.*` (для финансового учёта). Это не дублирование — это два bounded context, которые смотрят на одно действие с разных сторон.

---

## 6. Миграция текущих таблиц бота

### Текущее состояние

```
Neon: aisystant
├── database: aisybot       ← ~30 таблиц бота
└── database: digitaltwin   ← Данные ЦД (path + data)
```

### Куда переезжает каждая таблица

| Текущая таблица | → Schema | Почему |
|---|---|---|
| `interns` (профиль) | `public.users` | Канонический профиль |
| `answers` | `development` | Events (test_answered) |
| `qa_history` | `development` | Events (ai_chat) |
| `training_attempts` | `development` | Events (test_answered) |
| `training_progress` | `development` | State projection |
| `activity_log` | `development` | Events (session_start) |
| `assessments` | `development` | Events (self_assessed) |
| `training_settings` | `public.users` | Preferences (поля в users) |
| `user_sessions` | `development` | Events (session_start) |
| `service_usage` | `development` | Events (service_used) |
| `published_posts` | `development` | Events (post_published) |
| `subscriptions` | `finance` | Подписки |
| `user_access` | `finance` | Тиры доступа |
| `conversion_events` | `finance` | Воронки → монетизация |
| `tier_events` | `finance` | Тиры |
| `github_connections` | `connections` | OAuth |
| `wakatime_connections` | `connections` | API keys |
| `discourse_accounts` | `connections` | Внешние аккаунты |
| `fsm_states` | `operations` | Telegram FSM |
| `content_cache` | `operations` | TTL-кэш |
| `error_logs` | `operations` | Мониторинг |
| `pending_fixes` | `operations` | AutoFix |
| `request_traces` | `operations` | Observability |
| `feedback_reports` | `operations` | Тикеты |
| `feedback_triage` | `operations` | Автотриаж |
| `marathon_content` | `operations` | Контент доставки (шаблоны) |
| `feed_weeks` | `operations` | Расписание контента |
| `feed_sessions` | `operations` | Сессии доставки |
| `scheduled_publications` | `operations` | Планы публикаций |

### План миграции (пошаговый)

| Шаг | Что | Результат |
|-----|-----|-----------|
| 1 | Создать schemas в aisybot | Структура готова |
| 2 | Создать `public.users` из `interns` | Каноническая идентичность |
| 3 | Создать `development.user_events` (пустая, партиционированная) | Events готов |
| 4 | Добавить `log_event()` в бот → каждое действие пишется в user_events | Начало сбора |
| 5 | Создать таблицы проекций | State projections готовы |
| 6 | Создать `finance.*` таблицы, перенести subscriptions, user_access | Finance готов |
| 7 | Перенести OAuth → `connections.*` | Секреты изолированы |
| 8 | Перенести FSM, кэш, логи → `operations.*` | Служебное изолировано |
| 9 | Replay данных из `digitaltwin` database → Events | Исторические данные |
| 10 | Удалить database `digitaltwin` (после проверки) | Одна database |

**Обратная совместимость:** MCP-сервер digital-twin продолжает работать, но читает из новых таблиц. `write_digital_twin(path, data)` → транслируется в `INSERT INTO development.user_events`.

---

## 7. Безопасность

### 7.1 Row-Level Security (RLS)

```sql
-- Включить RLS на таблицах с пользовательскими данными
ALTER TABLE development.user_events ENABLE ROW LEVEL SECURITY;
ALTER TABLE development.skill_mastery ENABLE ROW LEVEL SECURITY;
ALTER TABLE finance.token_balances ENABLE ROW LEVEL SECURITY;
ALTER TABLE finance.subscriptions ENABLE ROW LEVEL SECURITY;
-- ... (все таблицы с user_id)

-- Политика: пользователь видит только свои данные
CREATE POLICY user_isolation ON development.user_events
    USING (user_id = current_setting('app.current_user_id')::BIGINT);
```

### 7.2 Роли PostgreSQL

```sql
-- Бот: полный доступ к Events + проекциям + finance
CREATE ROLE bot_service;
GRANT USAGE ON SCHEMA development, finance TO bot_service;
GRANT INSERT ON development.user_events TO bot_service;
GRANT SELECT, UPDATE ON ALL TABLES IN SCHEMA development TO bot_service;
GRANT SELECT, INSERT, UPDATE ON ALL TABLES IN SCHEMA finance TO bot_service;

-- MCP (per-user, через OAuth): ограниченный доступ
CREATE ROLE mcp_user;
GRANT USAGE ON SCHEMA development TO mcp_user;
GRANT INSERT ON development.user_events TO mcp_user;  -- только декларативные
GRANT SELECT ON ALL TABLES IN SCHEMA development TO mcp_user;
-- RLS ограничивает до user_id текущего пользователя

-- Web App: чтение проекций + запись Events + finance
CREATE ROLE web_app;
GRANT USAGE ON SCHEMA development, finance TO web_app;
GRANT INSERT ON development.user_events TO web_app;
GRANT SELECT ON ALL TABLES IN SCHEMA development TO web_app;
GRANT SELECT, INSERT ON ALL TABLES IN SCHEMA finance TO web_app;

-- Аналитик: только агрегаты, без PII
CREATE ROLE analyst;
GRANT USAGE ON SCHEMA development, finance TO analyst;
GRANT SELECT ON development.engagement TO analyst;
GRANT SELECT ON development.qualifications TO analyst;
GRANT SELECT ON finance.token_balances TO analyst;
-- Нет доступа к user_events (тексты), payments (суммы per user)

-- Финансист: finance полный, остальное — нет
CREATE ROLE financier;
GRANT USAGE ON SCHEMA finance TO financier;
GRANT SELECT ON ALL TABLES IN SCHEMA finance TO financier;
```

---

## 8. Масштабирование и retention

| Метрика | Текущее | При 1K users | При 10K users |
|---------|---------|-------------|---------------|
| Events/месяц | ~1K | ~100K | ~1M |
| Размер user_events | <1MB | ~50MB | ~500MB |
| Размер проекций | <1MB | ~5MB | ~50MB |
| Neon tier | Free (512MB) | Free/Launch | Launch ($19/мес) |

**Retention policy:**
- Events < 2 лет → горячее хранилище (активные партиции)
- Events > 2 лет → архив (старые партиции detach → cold storage)
- Проекции → всегда актуальные (пересчёт из Events)

---

## 9. PostHog и аналитика

**PostHog на текущем этапе НЕ нужен.**

| Задача | PostHog | user_events (свой) |
|--------|---------|---------------------|
| P(known) по навыкам (BKT) | Нет | Да |
| Когда навык протухнет (HLR) | Нет | Да |
| Streak, регулярность | Нет | Да |
| Воронки конверсии | Да | Да (через finance) |
| A/B тесты, feature flags | Да | Нет (не нужно сейчас) |
| Session replay | Да | Нет (не нужно без web UI) |

**Когда пересмотреть:** Web App с полноценным UI + >5K пользователей.

---

## 10. На будущее (Фаза 3+)

### 10.1 projection_snapshots — оптимизация rebuild

При текущем масштабе (<1K пользователей, <1000 событий на человека) rebuild проекций из всех Events — мгновенный. Snapshot-оптимизация понадобится, когда событий станет >10K на пользователя.

```sql
-- Planned for Phase 3+: когда rebuild из Events станет медленным
CREATE TABLE development.projection_snapshots (
    user_id         BIGINT NOT NULL REFERENCES public.users(id),
    projection_type TEXT NOT NULL,         -- 'skill_mastery', 'engagement', ...
    snapshot_data   JSONB NOT NULL,
    last_event_id   BIGINT NOT NULL,
    created_at      TIMESTAMPTZ DEFAULT NOW(),
    PRIMARY KEY (user_id, projection_type)
);
-- Rebuild = загрузить snapshot + replay событий после last_event_id
```

**Триггер:** rebuild одного пользователя > 1 сек.

### 10.2 indicator_registry — параметры методов в БД

Сейчас метамодель (какие индикаторы, формулы, зависимости, тип A/B/C) живёт в Pack-документе DP.ARCH.003. Это правильное разделение: Модель — в Pack, Данные — в Neon.

Когда карточек методов станет 30+ и параметры BKT начнут настраиваться per-skill (разные prior для ZP.1 и FPF.Holon), появится необходимость в таблице:

```sql
-- Planned for Phase 3
CREATE TABLE development.indicator_registry (
    indicator_id        TEXT PRIMARY KEY,     -- 'skill_mastery.ZP.1'
    computation_method  TEXT NOT NULL,        -- 'BKT', 'HLR', 'aggregate'
    parameters          JSONB NOT NULL,       -- {p_init: 0.1, p_learn: 0.3, ...}
    confidence_type     TEXT NOT NULL,        -- 'A' (direct), 'B' (proxy), 'C' (declaration)
    version             INTEGER DEFAULT 1,
    created_at          TIMESTAMPTZ DEFAULT NOW()
);
```

**Триггер:** >30 карточек методов или потребность в per-skill BKT параметрах.

### 10.3 Расширение проекций → CHR-Space

Начальные 5 проекций покрывают базовые потребности. Но модель характеристик созидателя описывает **30+ измерений** (CHR-Space, раздел 2.2.4). Подобно тому, как характеристики автомобиля (скорость, экономичность, безопасность) описывают его профиль, характеристики человека (агентность, обучаемость, стрессоустойчивость, калибр) описывают профиль созидателя.

**Примеры будущих проекций:**

| Проекция | Из каких событий | Метод |
|----------|-----------------|-------|
| `agency` (агентность) | goal_set, self_assessed, task_completed | Composite score |
| `stress_resilience` (стрессоустойчивость) | engagement при нагрузке, recovery patterns | Time-series analysis |
| `techno_integration` (техноинтеграция) | WakaTime, экзокортекс usage, tool adoption | Aggregate + decay |
| `social_impact` (социальное влияние) | comment_created, question_answered, referral | Network analysis |
| `creativity` (креативность) | guide_published, methodology_contributed | Output + novelty score |
| `learning_velocity` (скорость обучения) | test_answered (accuracy over time per skill) | Regression slope |

**Каждая новая проекция = новая таблица + replay событий.** Архитектура Event Sourcing это позволяет: лог неизменяем, проекции создаются ретроспективно.

### 10.4 Исследовательская лаборатория

На будущих этапах — создание «лаборатории характеристик»: среды, которая позволяет на основе накопленных событий:

1. **Экспериментировать** с новыми проекциями (replay на копии данных)
2. **Выявлять корреляции** между характеристиками (CHR-Space §6: матрица корреляций)
3. **Обнаруживать синергии** (MHT-эффекты: агентность + интеллект + калибр → лидерский потенциал)
4. **Строить персональную траекторию** развития (gap-анализ: Target(role) - Current(state))
5. **Валидировать методы вычисления** характеристик (A/B-тестирование формул на исторических данных)

**Триггер:** >1K пользователей с >6 мес историей событий, потребность в персонализированных траекториях.

---

## 11. АрхГейт: ЭМОГССБ

| Характеристика | Оценка | Обоснование |
|---|---|---|
| **Э** Эволюционируемость | 9 | Новый источник = новый event_type. Новая проекция = новая таблица + replay. Finance изолирован — растёт независимо от development |
| **М** Масштабируемость | 8 | Партиционирование events по месяцам. Neon serverless auto-scale. Plan: при >10K — Kafka/CDC, projection snapshots |
| **О** Обучаемость | 9 | 5 schemas, чёткие bounded contexts. «Событие → проекция» за 2 минуты. Единообразные имена-домены |
| **Г** Генеративность | 9 | Ретроспективные запросы. Replay для новых проекций. Open Learner Model. Finance с роялти авторам |
| **С** Скорость | 8 | Append <10ms. Snapshot read <50ms. BKT update <1ms. View 2-4 сек |
| **С** Современность | 8 | Event Sourcing + CQRS (proven). Neon serverless. Партиционирование. pgcrypto |
| **Б** Безопасность | 8 | RLS per user_id. 5 ролей PostgreSQL (bot, mcp, web, analyst, financier). pgcrypto для токенов. connections schema |
| | **Сумма** | **59/70 (8.4) — проходит АрхГейт (порог ≥8)** |

### Известные слабости (plan to address)

| Слабость | Риск | Когда решать |
|----------|------|-------------|
| JSONB payload без schema validation | Разнородные payload через год | Фаза 1: JSON Schema или CHECK constraint |
| Нет pgvector | Если нужны embeddings в ЦД | Фаза 3 (LLM extraction) |
| Нет CDC (Change Data Capture) | Real-time проекции запаздывают | При >10K users |
| PII в user_events payload | GDPR right-to-erasure | Фаза 2: sanitize при archival |
| indicator_registry в markdown | Параметры BKT не версионированы | Фаза 3: таблица в development |

---

## 12. Вопросы для архитектора

1. **Один проект Neon, schemas vs отдельные databases.** Предлагаем schemas (JOIN + RLS). Есть ли возражения?

2. **user_events — единая таблица vs отдельные таблицы по event_type?** Предлагаем единую (проще, один индекс, один поток). При >1M событий/месяц — можно партиционировать дополнительно по event_type.

3. **Содержимое (тексты ответов, вопросов) в payload JSONB vs отдельные таблицы.** Предлагаем в payload (одна точка правды). Но payload может быть большим (>10KB для ai_chat). Нужен ли limit?

4. **Retention policy.** Предлагаем: события < 2 лет горячие, > 2 лет snapshot + archive. Или хранить навсегда?

5. **Миграция с текущей структуры.** Можно ли начать с Фазы 0 (добавить `development.user_events` в текущую database) параллельно с существующими таблицами? Постепенная миграция vs big bang?

6. **Activity Hub.** Предлагаем: не отдельный сервис, а функция `log_event()` + HTTP endpoint. При каком масштабе выделять в отдельный сервис?

7. **Связь user_id.** Бот использует telegram `chat_id`, LMS — свой `user_id`, ORY — свой. Предлагаем `public.users` с маппингом всех ID. Согласуется ли это с планами по SSO?

8. **Finance: роялти авторам.** Предлагаем `finance.royalty_rules` + `royalty_distributions`. Достаточно ли для MVP, или нужна более сложная модель (несколько авторов на один ресурс, каскадные роялти)?

---

## 13. Связанные документы

| Документ | Где | Отношение |
|----------|-----|-----------|
| DP.ARCH.003 | PACK-digital-platform | Source-of-truth архитектуры ЦД (Events → State → Views) |
| Предложение — 3-слойная архитектура | Этот inbox | Архитектурное обоснование |
| DP.SOTA.009 | PACK-digital-platform | Knowledge-Based Digital Twins (SOTA) |
| DP.AISYS.014 | PACK-digital-platform | Бот: интеграция с ЦД |
| DP.ARCH.002 | PACK-digital-platform | Service Tiers (тиры обслуживания) |
| Модель характеристик 2.2 | DS-ecosystem-development (A2.2.4) | 30+ характеристик созидателя → будущие проекции |
| CHR-Space созидателя | DS-ecosystem-development (A2.2.4) | 26-мерное пространство состояний |
| Раздел 4.5 «Характеристики человека в системном контексте» | Руководство «Методы саморазвития» | Концепция: характеристики человека как системы |

---

*Создано: 2026-02-26. Обновлено: 2026-02-26. Статус: for-review.*
*Авторы: Tseren + Claude (Opus)*
