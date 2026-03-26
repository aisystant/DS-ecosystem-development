# WP-183: CRM + Billing — предложение архитектору

> **Статус:** proposal | **Источник:** оперативка ИТ 26 мар 2026
> **Связи:** WP-73, DP.SC.112, DP.SC.114, DP.SYS.001
> **Смежные системы:** WP-109 (Activity Hub — получает payment events), WP-121 (Points Engine — отдельная система начисления баллов), WP-115 (Семинар — ключевой сценарий)
> **АрхГейт:** 60/70 ✅ (после верификации Haiku R23 + доработки)
> **Приложение:** [WP-183-crm-billing-research-appendix.md](WP-183-crm-billing-research-appendix.md)

## Суть решения (30 сек)

**Все данные — в одной Neon PG. Инструменты — тонкие слои поверх неё.**

Внешние CRM (Twenty, EspoCRM, NocoDB) создают вторую БД и становятся центром (SPOF). Наше решение — CRM это **окно в данные**, не центр. Центр — бот + Neon + Ory (как в DP.ARCH.001).

- **Directus** = UI для руководителя (формы, группы, RBAC). Снимается без потери данных
- **Metabase** = дашборды (MRR, churn, LTV). Снимается без потери данных
- **Бот** = интерфейс менеджеров + обработка платежей (webhook → Neon напрямую)
- **Neon PG** = единственный источник правды (crm.\*, finance.\*)

Если Directus упадёт — бот продолжает работать. Если Metabase упадёт — платежи идут. `pg_dump` — все данные ваши.

## Проблема

Sales-команда (5 чел) управляет контактами, вузовскими группами, оплатами. **Основной поток оплаты остаётся как сейчас** (YooKassa через LMS, подписки через бота). Дополнительно нужно поддержать: оплату звёздами Telegram, попадание в чат **без email и аккаунта** на платформе, ручной ввод вузовских групп. Нужны CRM, billing и access management — на единой Neon PG, без второй БД.

## Почему не внешний CRM

| Решение | Главная проблема |
|---------|-----------------|
| **Twenty** | Нет понятия группы (подтвердил архитектор). Своя БД |
| **EspoCRM** | PostgreSQL = experimental. Отдельная MariaDB = вторая БД, бот через API = SPOF |
| **NocoDB** (coda-based, идея архитектора) | Не прошёл АрхГейт (41/70): нет RLS, лицензия не open-source, видит только `public` schema |
| **Все внешние CRM** | telegram_id как primary identity не поддерживается. TG Stars не поддерживается. Вторая БД = синхронизация |

Детали: [WP-183-crm-billing-research-appendix.md](WP-183-crm-billing-research-appendix.md) (исследование 16 CRM).

## Решение: Directus + Metabase

**Directus** оборачивает существующие таблицы Neon (schemas `crm`, `finance`). Не создаёт свою БД — introspects вашу. RBAC с row-level policies. REST + GraphQL API автогенерируются.

```
┌─────────────────────────────────────────────────────────┐
│                    ИНТЕРФЕЙСЫ (Слой 3)                   │
│                                                          │
│  Telegram Bot          Directus UI          Metabase     │
│  (мессенджер:          (веб-приложение:     (веб-приложение:│
│   телефон +             браузер на компе,   браузер,     │
│   десктоп TG)           crm.example.com)    bi.example.com)│
│                                                          │
│  Менеджеры +           Руководитель +       Руководитель +│
│  участники             менеджеры            бухгалтер    │
└──────────────────────────┬──────────────────────────────┘
                                 │
                      ┌──────────▼──────────────────┐
                      │       ОБРАБОТКА              │
                      │                              │
                      │  Billing Service  Directus   │
                      │  (YooKassa/       Flows      │
                      │   Stripe/Stars/   (триггеры  │
                      │   Баллы/Manual)   → webhooks)│
                      └──────────┬──────────────────┘
                                 │
                      ┌──────────▼──────────────────┐
                      │     Neon PostgreSQL           │
                      │  crm.* │ finance.* │ points.*│
                      └─────────────────────────────┘
```

| Компонент | Роль | Лицензия | RAM |
|-----------|------|----------|-----|
| **Directus** | CRM UI (на компе) + API + RBAC + Flows (автоматизации) | BSL 1.1 (GPLv3 через 3 года) | 512 MB |
| **Metabase** | Дашборды: MRR, воронка, баллы, unit economics | AGPL-3.0 | 2 GB (JVM) |
| **Billing Module** | Strategy pattern: 5 адаптеров. Модуль бота с чёткой границей | Своё | В составе бота |

**Billing = модуль бота, не микросервис.** Для 100-1000 подписчиков отдельный сервис — преждевременная оптимизация. Billing Module — отдельный package внутри бота (`billing/providers/`, `billing/service.py`, `billing/webhooks.py`) с единственным входом `BillingService`. Выделяется в отдельный сервис при: (a) втором клиенте (веб-приложение), (b) отдельном цикле деплоя, (c) compliance-требованиях.

**Webhook-обработка — в боте, не в Directus.** Критическая коррекция после верификации: webhook от YooKassa/Stripe/TG Stars обрабатывается **ботом (Billing Module) напрямую → Neon**. Directus Flows — только для UI-триггеров (менеджер сменил статус группы → уведомление в бот). Directus не участвует в цепочке обработки платежей.

```
ПРАВИЛЬНАЯ цепочка:
  Webhook (YooKassa/Stripe) → Бот (Billing Module) → Neon (INSERT) → 200 OK
  Бот → добавить в чат → уведомить менеджера

Directus Flows — только для:
  Менеджер сменил статус в Directus UI → webhook → бот (добавить в чат)
```

### Три интерфейса (multi-surface, принцип #15)

| Интерфейс | Тип | Устройство | Кто | Что |
|-----------|-----|-----------|-----|-----|
| **Telegram-бот** | Мессенджер | Телефон + десктоп Telegram | Менеджеры, участники | `/contact`, `/group`, `/pay`, `/pipeline`, `/at_risk` — быстрые операции на ходу |
| **Directus** (crm.example.com) | **Веб-приложение** | Браузер на компьютере | Руководитель, менеджеры | Таблицы контактов, bulk import CSV, группы, RBAC, полная карточка контакта |
| **Metabase** (bi.example.com) | **Веб-приложение** | Браузер на компьютере | Руководитель, бухгалтер | Дашборды: MRR, воронка, LTV, churn, когорты, unit economics |

Directus и Metabase — полноценные веб-приложения, доступные из любого браузера. Не только Telegram.

## Оплата: как сейчас + дополнительные каналы

**Основной поток (без изменений):**
- Подписка БР → бот → Aisystant API → YooKassa → webhook → LMS активирует
- Курсы/программы → бот → `create_internship_payment()` → YooKassa → LMS

**Дополнительные каналы (новое):**

| Канал | Сценарий | Идентификатор |
|-------|----------|---------------|
| **TG Stars** | Оплата семинара/события в боте | telegram_id (без email) |
| **Manual** | Менеджер регистрирует оплату вузовской группы | telegram_id или email |
| **Баллы** | Участник оплачивает баллами | ory_id |

### Ключевой новый сценарий: оплата звёздами → чат без email

1. Участник нажимает «Оплатить» → бот создаёт Stars invoice (`currency="XTR"`, `provider_token=""`)
2. Участник оплачивает → бот получает `successful_payment` callback
3. Billing Module (в боте): idempotency check (`processed_events`) → INSERT `finance.payments` (telegram_id, amount, method=tg_stars) → INSERT `crm.chat_access` (telegram_id, chat_id, expires_at) — **всё в одной транзакции**
4. Бот добавляет участника в чат (`unbanChatMember`)
5. Бот уведомляет менеджера: «@username оплатил семинар X»
6. Позже (если зарегистрируется на платформе) → **бот при регистрации** создаёт `crm.identity_links` (telegram_id ↔ ory_id). Триггер: Ory webhook `identity.created` → бот проверяет наличие telegram_id в `crm.leads` → если есть, создаёт link

### Обработка ошибок и edge-cases

| Ситуация | Обработка |
|----------|----------|
| **Дублирующий webhook** | `processed_events` PK (provider, event_id) → ON CONFLICT DO NOTHING → 200 OK |
| **Двойная покупка одного продукта** | UNIQUE constraint (telegram_id, product_id, period) → ошибка → сообщение «уже оплачено» |
| **Рефанд TG Stars** | Менеджер в Directus: кнопка «Рефанд» → Directus Flow → webhook → бот вызывает `refund_star_payment()`. **Telegram не возвращает 30% комиссию** — учитывать в unit economics |
| **Chargeback (YooKassa/Stripe)** | Webhook `payment.canceled` / `charge.dispute.created` → Billing Module: UPDATE `finance.payments` SET status='refunded' → откатить `crm.chat_access` → откатить `finance.revenue_ledger` (статус='reversed') |
| **Identity linking не произошёл** | Cron-задача (ежедневно): найти записи в `crm.leads` с telegram_id без match в `crm.identity_links` → уведомить менеджера список «неслинкованных» |
| **Revenue sharing округление** | Последний stakeholder получает остаток: `curator_amount = total - platform - author - instructor`. Все суммы `NUMERIC(12,2)` |

## Группы

**Полноценное управление группами в Directus:**

| Операция | Как |
|----------|-----|
| Создать группу | Directus UI → collection «Группы» → New: «МГУ Поток-5», организация, год |
| Добавить участников | Import CSV (20 студентов) → привязка к группе (M:N relation) |
| Массовое добавление в чат | Directus Flow: при смене статуса группы → «оплачено» → добавить всех в чат |
| Отслеживать прогресс | Directus view: группа → кто зарегистрировался, кто активен, кто at-risk |
| Быстрый доступ в Telegram | `/group МГУ-5` → список участников + статусы |

## Billing Service — Strategy pattern

```
Billing Service (orchestrator)
  ├── YooKassa  (РФ, подписки — основной, как сейчас)
  ├── Stripe    (мир, подписки)
  ├── TG Stars  (Telegram, события — дополнительный)
  ├── Баллы     (внутренняя валюта, начисление + списание)
  └── Manual    (B2B, менеджер регистрирует)
```

Revenue sharing: platform 30%, author 50%, instructor 15%, curator 5%.

### Технические решения (из исследования)

| Аспект | Решение |
|--------|---------|
| **Idempotency** | Таблица `finance.processed_events` (provider, event_id) PK. INSERT ON CONFLICT DO NOTHING. Дублирующие webhooks = 200 OK без обработки |
| **Webhook retry** | Отвечать 200 быстро, обрабатывать async. Stripe retry до 3 дней. YooKassa retry до 24h |
| **TG Stars** | `currency="XTR"`, `provider_token=""`, рефанд через `refund_star_payment()`. Telegram комиссия ~30% |
| **Revenue sharing** | Calculate immediately, settle с задержкой 14 дней (chargeback window). `Decimal`, не `float` |
| **Neon** | **Always-on compute обязателен** (cold start 1-3 сек ломает webhook-обработку). Direct connection string (не pooler) для Directus |
| **Metabase app DB** | Отдельная PostgreSQL (Railway Postgres), НЕ в Neon. Metabase метаданные не должны быть в бизнес-БД |
| **Directus + Neon SSL** | `DB_SSL=true`, `DB_POOL__MIN=0`, `DB_POOL__MAX=10` |
| **Audit log** | Directus activity + revisions включены по умолчанию. Фиксирует: кто, что, когда, diff полей. Добавить retention policy |
| **Encryption** | Neon: encryption at rest (AES-256) по умолчанию. Directus RBAC для ограничения доступа к PII-полям по ролям |
| **Реестр адаптеров** | `billing-adapters.yaml`: name, type, status, version. Новый адаптер = строка в yaml + класс в `billing/providers/` |

## Связка CRM с другими системами

```
                    ┌────────────────┐
                    │   Ory Network   │ ← identity, тиры, SSO
                    └───────┬────────┘
                            │ ory_identity_id
    ┌───────────────────────┼───────────────────────┐
    │                       │                        │
    ▼                       ▼                        ▼
┌────────┐          ┌──────────────┐         ┌────────────┐
│  LMS   │          │   CRM (Neon) │         │    Бот     │
│Aisystant│         │  crm.*       │         │(Telegram)  │
│        │◄────────►│  finance.*   │◄───────►│            │
│курсы,  │ подписки │  points.*    │ платежи │ /subscribe │
│видео   │ доступы  │              │ команды │ /pay       │
└────┬───┘          └──────┬───────┘         └─────┬──────┘
     │                     │                        │
     ▼                     ▼                        ▼
┌────────┐          ┌──────────────┐         ┌────────────┐
│Digital │          │   Metabase   │         │  Telegram   │
│Twin MCP│          │  (дашборды)  │         │   чаты     │
│(ЦД)    │          │  MRR, LTV,   │         │(chat_access)│
│        │          │  баллы, UE   │         │            │
└────────┘          └──────────────┘         └────────────┘
```

| Связка | Как работает | Данные |
|--------|-------------|--------|
| **CRM → Ory** | Регистрация → Ory identity → `crm.identity_links` | ory_id ↔ telegram_id |
| **CRM → LMS** | Подписка/курс → LMS API (как сейчас) | subscription status |
| **CRM → Бот** | Directus Flow → webhook → бот добавляет/удаляет из чата | chat_access |
| **CRM → ЦД** | `crm.identity_links` → Digital Twin MCP по ory_id | активность, прогресс |
| **CRM → Баллы** | Billing Service пишет `type=spent` в `finance.point_transactions` (WP-121). Metabase читает `finance.point_balances` | баланс, история |
| **CRM → Metabase** | Прямое чтение из Neon (те же таблицы) | MRR, churn, LTV, UE |
| **CRM → Activity Hub** | Billing Service → `ingest_event()` (WP-109) при каждом платеже. Payment event в `user_events` | payment_completed |
| **CRM → WP-115** | `crm.chat_access` + `finance.transactions` + `crm.events` обслуживают сценарий семинара | доступ, оплата, видео |

### Баллы — отдельная система (→ WP-121)

**Points Engine (WP-121) — отдельная система от CRM.** Владеет таблицами `finance.point_rules`, `finance.point_transactions`, `finance.point_balances`.

CRM + Billing **взаимодействует** с Points Engine:
- **Списание:** Billing Service пишет `type=spent` в `finance.point_transactions` при оплате баллами
- **Чтение:** Metabase читает `finance.point_balances` для дашбордов
- **Начисление:** Points Engine сам вычисляет баллы из `user_events` (WP-109) по правилам `point_rules`

Подробнее: [WP-121](../../../DS-my-strategy/inbox/WP-121-point-rules-and-implementation.md).

### Activity Hub — учёт payment events (→ WP-109)

Billing Service при каждом успешном платеже пишет факт в Activity Hub (WP-109) через `ingest_event()`:
- `source='billing'`, `event_type='payment_completed'`
- Это позволяет WP-121 начислять баллы за покупки
- Activity Hub использует `crm.identity_links` для Identity Resolution (telegram_id ↔ ory_id)

Подробнее: [WP-109](WP-109-activity-hub-lms-integration-proposal.md).

## Unit economics

| Метрика | При 100 подписчиках T2 ($15/мес) |
|---------|----------------------------------|
| MRR | $1 500 |
| Platform share (30%) | $450 |
| Инфраструктура | $17/мес (Directus $5 + Metabase $10-12 + Neon always-on ~$0) |
| **Маржа** | **$433/мес** |
| Окупаемость разработки ($4 000) | **~9 мес** |

B2B: 2 вуза × 50 чел × $15 × 12 мес = $18 000/год → окупаемость **~3 мес**.

**Metabase unit economics dashboard:** CAC, LTV, payback period, churn, ARPU по тирам, revenue per group, баллы → конверсия в оплату.

## Сценарии использования (полный список)

| # | Сценарий | Интерфейс | Описание |
|---|----------|-----------|----------|
| 1 | Оплата звёздами → чат | Бот | Участник платит Stars → попадает в чат без email |
| 2 | Вузовская группа | Directus (комп) | Import CSV 20 студентов → группа → массовое добавление в чат |
| 3 | Подписка YooKassa/Stripe | Бот | Как сейчас, + запись в CRM для аналитики |
| 4 | Менеджер: быстрый просмотр | Бот (телефон) | `/contact @username` → карточка |
| 5 | Менеджер: pipeline | Бот (телефон) | `/pipeline` → сделки по стадиям |
| 6 | Менеджер: at-risk | Бот (телефон) | `/at_risk` → неактивные 14+ дней |
| 7 | Руководитель: bulk import | Directus (комп) | CSV → контакты + привязка к группе |
| 8 | Руководитель: RBAC | Directus (комп) | Настроить кто что видит |
| 9 | Руководитель: дашборд | Metabase (комп) | MRR, воронка, LTV, баллы |
| 10 | Создание группы | Directus (комп) | Новая группа → участники → статус → чат |
| 11 | Управление группой | Directus + бот | Добавить/удалить участника, сменить статус |
| 12 | Регистрация ручного платежа | Directus или бот | Менеджер фиксирует оплату (B2B, нал) |
| 13 | Склейка identity | Автоматически | telegram_id ↔ ory_id при регистрации на платформе |
| 14 | Начисление баллов | Автоматически | Activity Hub (WP-109) → Points Engine (WP-121). CRM не участвует |
| 15 | Оплата баллами | Бот | Billing Service → `type=spent` в Points Engine (WP-121) → доступ |
| 16 | Семинар end-to-end | Бот + Directus | [WP-115](WP-115-seminar-payment-access-scenario.md): оплата → чат → видео → cleanup |
| 17 | Отмена подписки | Бот | Участник /cancel → Billing Module → YooKassa/Stripe cancel → grace 7 дней → T1 |
| 18 | Рефанд Stars | Directus → бот | Менеджер нажимает «Рефанд» → бот вызывает `refund_star_payment()` → откат доступа |
| 19 | Reconciliation | Cron (еженедельно) | Сверка Stripe/YooKassa records vs `finance.payments` → alert при расхождении |
| 20 | Identity linking alert | Cron (ежедневно) | Неслинкованные telegram_id → уведомление менеджеру |

## АрхГейт (верифицировано Haiku R23)

**L1: 60/70 ✅** (порог 56)

| Характеристика | Оценка | Комментарий |
|----------------|--------|-------------|
| Эволюционируемость | **9** | Directus introspects Neon. Strategy pattern. Billing Module с чёткой границей → выделяется в сервис при росте |
| Масштабируемость | **8** | RBAC. Neon масштабируется. Billing stateless. 5→50 менеджеров — ок |
| Обучаемость | **9** | Telegram = ноль обучения. Directus для руководителя. PROCESSES.md для онбординга |
| Генеративность | **7** | CRM = инструмент команды, не генеративная платформа. Directus переиспользуется |
| Скорость | **8** | Бот < 3 сек. Directus REST < 200ms. Metabase кеширует |
| Современность | **8** | Headless data platform. Strategy pattern. Event-driven Flows. yaml-реестр адаптеров |
| Безопасность | **8** | RBAC v11 row-level. Neon encryption at rest. Audit log. Secrets в env vars |

**Замечания верификатора (Haiku R23) и ответы:**

| Замечание | Принято? | Действие |
|-----------|---------|----------|
| Billing в составе бота = shared process | ✅ Частично | Модуль с чёткой границей. Выделяется в сервис при росте |
| Нет PROCESSES.md | ✅ | Написать в Phase 0 (+4h) |
| Нет yaml-реестра адаптеров | ✅ | `billing-adapters.yaml` в Phase 0 (+2h) |
| PII encryption не описано | ✅ | Neon AES-256 at rest + Directus RBAC для PII-полей |
| Audit log не описан | ✅ | Directus activity + revisions (OOTB) + retention policy |
| Webhook через Directus = SPOF | ✅ | **Коррекция:** webhook → бот (Billing Module) → Neon напрямую. Directus не в цепочке платежей |
| Identity linking не описан | ✅ | Ory webhook `identity.created` → бот → `crm.identity_links`. Cron для неслинкованных |
| Chargeback не описан | ✅ | Webhook → UPDATE status='refunded' → откат chat_access + revenue_ledger |
| Нет Event Bus | ❌ | Webhook'и обрабатываются ботом синхронно. Kafka для 5 менеджеров = overengineering |
| Нет SAGA для платежей | ❌ | Одна транзакция: payment + chat_access + revenue_ledger. Не distributed |
| Обучаемость = 4 | ❌ | Telegram — знакомый интерфейс. /help + PROCESSES.md = достаточно |
| Генеративность = 3 | ❌ | CRM ≠ генеративная платформа. 7 — справедливо для Зоны Б |

**L2 (информативно):** Переносимость 8.3 ✅, Интероперабельность 8.0 ✅, Сохранность знаний 7.3 ✅

## Effort

| Phase | Что | Часы |
|-------|-----|------|
| **0** | Схемы Neon + Directus (Railway + Neon SSL) + TG Stars + CRM-команды бота + Metabase (Railway + отдельная app DB) + `billing-adapters.yaml` + PROCESSES.md + retry pattern для Flows | 48h |
| **1** | YooKassa/Stripe адаптеры + idempotency (`processed_events`) + revenue sharing (calculate + settle) + Metabase дашборды (MRR, churn, LTV, когорты, unit economics) | 40h |
| **2** | Identity linking, B2B лицензии, feature gating, at-risk автоматизация, n8n (если цепочки усложнятся), Billing Service как отдельный сервис (если нужен) | По мере роста |

## Открытые вопросы

| # | Вопрос | Рекомендация из исследования |
|---|--------|------------------------------|
| Q1 | Access Management (chat_access) — часть Billing или отдельная SYS.019? | Часть Billing Module (chat_access = следствие платежа) |
| Q2 | ~~Billing — модуль или сервис?~~ | **Решено:** модуль бота с чёткой границей. Выделять при росте |
| Q3 | BSL 1.1 Directus — приемлемо? | Да. BSL разрешает внутреннее использование до $5M. GPLv3 через 3 года. Зафиксировать в ADR |
| Q4 | ~~Баллы~~ | **Решено:** `finance.point_*`, система начисления = WP-121 |
| Q5 | Billing adapter для Activity Hub (WP-109) — в Phase 0 CRM? | Простой `ingest_event()` call — включить в Phase 0 |
| Q6 | `crm.events` (семинары, потоки) для WP-115 — в Phase 0? | Да, базовая таблица |
| Q7 | Neon always-on compute — включить? | **Обязательно** для webhook-обработки (cold start 1-3 сек ломает YooKassa/Stripe) |
| Q8 | ~~Directus Flows retry~~ | **Решено:** webhook → бот напрямую (не через Directus). Retry не нужен — бот обрабатывает синхронно |
| Q9 | Reconciliation job — включить в Phase 0 или Phase 1? | Phase 1 (когда появятся реальные платежи для сверки) |
| Q10 | Chargeback: откат settlement если уже выплачен автору? | Нужна политика: hold period 14 дней. Если после settlement — вычитать из следующей выплаты |
| Q11 | Промо-коды — нужны в Phase 0? | Нет. Phase 2+ или отдельный РП (маркетинг) |

## Scope и границы

**В scope WP-183:** CRM (контакты, группы, воронка) + Billing (подписки, Stars, manual, revenue sharing) + Access Management (chat_access).

**Вне scope WP-183 (отдельные РП):**
- SC-15 (маркетинг): A/B тесты, конверсионные триггеры C1-C7, реферальная программа, амбассадоры, landing pages
- Промо-коды: отдельная таблица `marketing.promo_codes`, не часть Billing Module
- Mobile/PWA: мультиповерхностный доступ (SC-7) — отдельная тема

**Рекомендация:** CAC tracking добавить в `crm.leads` как поле `source` (органика, реферал, кампания, вуз) — минимальная подготовка для будущего маркетинг-РП

## Зависимости и передача

### Event Bus (→ WP-73 задача 0.5)

CRM Phase 0 строится **без Event Bus** — Billing Module пишет INSERT'ы в Neon синхронно. Это корректно для текущего масштаба (5 менеджеров, 100-1000 подписчиков).

**При появлении Event Bus** (Neon outbox + pg_notify, WP-73 Фаза 0 задача 0.5):
- Billing Module публикует события (`payment_completed`, `subscription_changed`, `access_granted`) в outbox
- Activity Hub (WP-109) подписывается на `payment_completed` вместо прямого вызова `ingest_event()`
- Points Engine (WP-121) подписывается на события из Activity Hub
- Nudge Engine подписывается на `subscription_changed`

**Объём доработки:** ~4h (адаптер outbox в Billing Module + миграция `ingest_event()` → подписка). Не рефакторинг — переключение одного слоя.

**Event Bus не является отдельным РП** — это инфраструктурная задача внутри roadmap WP-73 (8-12h).

---

*26 марта 2026. v7: + секция Event Bus как зависимость. 20 сценариев.*
