---
id: C2.DP.ARCH.003-impl
name: "Реализация ЦД: системы, схемы, безопасность, масштабирование"
type: implementation
status: approved
source: DP.ARCH.003
summary: "Извлечено из DP.ARCH.003. Текущие ИТ-системы (Railway, Neon, CF Workers), 5 schemas Neon, RLS + 5 ролей PostgreSQL, масштабирование и retention."
created: 2026-03-13
updated: 2026-03-13
---

# Реализация ЦД: системы, схемы, безопасность, масштабирование

> **Доменный источник:** [DP.ARCH.003 — Архитектура цифрового двойника](../../../../../PACK-digital-platform/pack/digital-platform/02-domain-entities/DP.ARCH.003-digital-twin-architecture.md)
>
> Этот файл содержит **реализационные детали** (HD #29: замени вендор/фреймворк — утверждение станет ложным? Да → implementation).

---

## 10. Текущие ИТ-системы и план внедрения

### 10.1 Что есть сейчас

| Система | Статус | Какие события генерирует |
|---------|--------|------------------------|
| **AIST Bot** (@aist_me_bot) | Production, Railway + Neon | Чат, марафон, лента, заметки, тест, настройки ЦД |
| **LMS** | Внешняя (Aisystant) | ДЗ, прохождение курсов, тесты |
| **MCP knowledge-mcp** | Production, CF Workers | Поиск знаний (косвенно — через бота) |
| **MCP digital-twin** | Production, CF Workers | Чтение/запись ЦД |
| **Neon DB** | Production | Профиль, сессии, QA-история, заметки, лента, марафон |
| **Claude Code** (T3–T4) | Локальный | Сессии, captures, commits |

### 10.2 Что нужно сделать

#### Фаза 0: Event Store (минимальная, 1 день)

| # | Задача | Бюджет | Результат |
|---|--------|--------|-----------|
| 1 | Создать таблицу `user_events` в Neon | 30 мин | Хранилище событий |
| 2 | Функция `log_event()` в боте | 1h | Единая точка записи |
| 3 | Подключить P0-точки: session_start, ai_chat, marathon_step | 2–3h | Начало сбора |
| 4 | Простая проекция engagement (SQL view) | 1h | Первые метрики |

**После Фазы 0:** каждое действие в боте записывается. Через неделю — данные для анализа.

#### Фаза 1: Skill Mastery (зависит от WP-55, ~1 неделя)

| # | Задача | Бюджет | Зависимость |
|---|--------|--------|-------------|
| 5 | Ячейки curriculum со skill_ids (WP-55) | 4–6h | — |
| 6 | Тестовые вопросы, привязанные к skill_ids | 2–3h | #5 |
| 7 | BKT-модуль: обновление P(known) при ответе | 2–3h | #3, #6 |
| 8 | Проекция skill_mastery в Neon | 1h | #7 |

**После Фазы 1:** бот знает P(known) по каждому принципу для каждого пользователя.

#### Фаза 2: Memory + Recommendations (~2 недели)

| # | Задача | Бюджет | Зависимость |
|---|--------|--------|-------------|
| 9 | HLR-модуль: half-life, next_review_date | 2–3h | #8 |
| 10 | Spaced repetition в ленте: вопросы по «протухающим» навыкам | 2–3h | #9 |
| 11 | Open Learner Model: /mydata показывает вектор навыков | 2–3h | #8 |
| 12 | Bottleneck рекомендация: «что учить» | 1–2h | #8 |

#### Фаза 3: LLM Extraction + Misconceptions (позже)

| # | Задача | Бюджет |
|---|--------|--------|
| 13 | Async Haiku extraction из чатов | 3–4h |
| 14 | Misconception map | 2–3h |
| 15 | Карточки методов для всех характеристик (тип A, B, C) | 3–4h |
| 16 | Qualifications проекция (стадии) | 2–3h |

#### Фаза 4: LMS интеграция (когда будет API)

| # | Задача | Бюджет |
|---|--------|--------|
| 17 | Webhook/API для приёма событий из LMS | 2–3h |
| 18 | Маппинг LMS-курсов на skill_ids | 2–3h |

---

## 13. Хранилище: 5 schemas Neon

**Принцип: ЦД = ВСЯ база данных целиком**, а не отдельная schema. Каждая schema отвечает за свой домен, но вместе они составляют полный ЦД созидателя.

```
database (ОДНА)
│
├── schema: public                      [Идентичность пользователя]
│   └── users                           ← Канонический профиль (id, telegram_id, email,
│                                          lms_id, ory_id, name, language, current_tier)
│
├── schema: development                 [Развитие: события + проекции]
│   ├── user_events                     ← Events (append-only, PARTITIONED BY RANGE)
│   ├── skill_mastery                   ← State projection (BKT)
│   ├── memory_decay                    ← State projection (HLR)
│   ├── engagement                      ← State projection (агрегаты)
│   ├── misconceptions                  ← State projection (LLM)
│   └── qualifications                  ← State projection (threshold rules)
│
├── schema: finance                     [Финансы, токены, роялти]
│   ├── token_transactions / balances   ← Лог + баланс токенов
│   ├── subscriptions / payments        ← Подписки и платежи
│   ├── royalty_rules / distributions   ← Роялти авторам
│   └── referral_rewards                ← Реферальные бонусы
│
├── schema: connections                 [Подключения к внешним системам]
│   ├── oauth_tokens                    ← pgcrypto encrypted
│   ├── api_keys                        ← pgcrypto encrypted
│   └── external_accounts               ← Discourse, LMS
│
└── schema: operations                  [Служебное: FSM, кэш, мониторинг]
    ├── fsm_states, content_cache       ← Эфемерное (можно дропнуть)
    ├── marathon_content, feed_*        ← Контент доставки
    └── error_logs, request_traces      ← Мониторинг
```

### 13.1 Критерии разделения на schemas

| # | Критерий | Вопрос | Если «нет» |
|---|----------|--------|-----------|
| 1 | **Один домен** | Все таблицы отвечают на один вопрос? | Разнести по разным schemas |
| 2 | **Независимый жизненный цикл** | Данные меняются по своему ритму? | Могут жить вместе |
| 3 | **Независимый доступ** | Разные сервисы/роли обращаются? | Могут жить вместе |
| 4 | **Тест канала** | Если убрать один канал (бот, web), домен останется? | Это домен, а не канал |

### 13.2 Bounded contexts

| Schema | Домен | Вопрос | Можно дропнуть? |
|--------|-------|--------|----------------|
| `public` | Идентичность | «Кто этот пользователь?» | Нет |
| `development` | Развитие | «Что делал, что знает и куда движется?» | Нет |
| `finance` | Финансы | «Сколько заплатил, заработал, на балансе?» | Нет |
| `connections` | Подключения | «Как подключены GitHub, LMS, WakaTime?» | Нет (секреты) |
| `operations` | Служебное | «FSM, кэш, логи?» | Да |

### 13.3 Отвергнутые варианты

| Кандидат | Решение | Причина |
|----------|---------|---------|
| `schema: bot` | Не нужна | Бот — канал, не домен. Не проходит тест канала |
| `schema: gamification` | Не нужна | Токены — finance, стадии — development.qualifications |
| `schema: learning` | Не нужна | Обучение — процесс, результаты = development |
| `schema: digital_twin` | Не нужна | ЦД = ВСЯ база, не одна schema |

### 13.4 Принцип именования

Все имена — **существительные-домены**: что содержит schema (development, finance, connections, operations). Не: кто использует (bot), не: процесс (billing), не: прилагательное (operational).

### 13.5 Потоки данных

```
┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐
│   Бот    │  │   LMS    │  │   Клуб   │  │ Web App  │
└────┬─────┘  └────┬─────┘  └────┬─────┘  └────┬─────┘
     │             │             │              │
     ▼             ▼             ▼              ▼
┌──────────────────────────────────────────────────────┐
│  development.user_events (append-only)                │
│  = Activity Hub (единая точка записи)                 │
│  Бот: log_event() напрямую                            │
│  LMS/Клуб: HTTP webhook → API → INSERT               │
│  Web App: прямой INSERT                               │
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
         │  Views (на лету) │    tokens_earned ──────┘
         │  Рекомендации    │    payment_completed
         │  Open Learner    │
         │  Model           │
         └────────┬────────┘
                  ▼
         Event: recommendation_shown
         (цикл замыкается)
```

**Activity Hub — не отдельный сервис.** `log_event()` + HTTP endpoint. Каждый новый источник = новый producer в ту же таблицу.

**Связь Events → Finance:** события `tokens_earned`, `payment_completed` пишутся и в `development.user_events` (ЦД-аналитика), и в `finance.*` (финучёт). Два bounded context смотрят на одно действие с разных сторон.

---

## 14. Безопасность

### 14.1 Row-Level Security (RLS)

RLS на всех таблицах с `user_id`. Политика: пользователь видит только свои данные.

```
user_isolation: user_id = current_setting('app.current_user_id')
```

### 14.2 Роли PostgreSQL (5 ролей)

| Роль | Доступ | Ограничения |
|------|--------|-------------|
| `bot_service` | development (INSERT events, SELECT/UPDATE проекции), finance (SELECT/INSERT/UPDATE) | Полный доступ к Events + проекциям + finance |
| `mcp_user` | development (INSERT events декларативные, SELECT проекции) | RLS ограничивает до user_id текущего пользователя |
| `web_app` | development (INSERT events, SELECT проекции), finance (SELECT/INSERT) | Чтение + запись Events + finance |
| `analyst` | development (SELECT engagement, qualifications), finance (SELECT balances) | Только агрегаты, без PII (нет доступа к user_events, payments) |
| `financier` | finance (SELECT all) | Finance полный, остальное — нет |

### 14.3 Шифрование секретов

`connections.*` — pgcrypto (`pgp_sym_encrypt`). OAuth-токены и API-ключи зашифрованы at rest. Минимальный доступ — только сервис аутентификации.

---

## 15. Масштабирование и retention

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

**Оптимизация rebuild (Фаза 3+):** При >10K событий на пользователя — snapshot-таблица `projection_snapshots` (JSONB snapshot + last_event_id). Rebuild = загрузить snapshot + replay после last_event_id. Триггер: rebuild > 1 сек.

**Параметры методов в БД (Фаза 3+):** При >30 карточек методов или per-skill BKT параметрах — таблица `indicator_registry` (indicator_id, computation_method, parameters JSONB, confidence_type, version). Триггер: потребность в per-skill настройке.

---

*Извлечено из [DP.ARCH.003](../../../../../PACK-digital-platform/pack/digital-platform/02-domain-entities/DP.ARCH.003-digital-twin-architecture.md) (2026-03-13). WP-93: separation of domain (Pack) from implementation (DS).*
