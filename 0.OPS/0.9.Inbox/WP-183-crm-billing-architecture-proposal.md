# WP-183: CRM + Billing — предложение архитектору

> **Статус:** proposal | **Источник:** оперативка ИТ 26 мар 2026
> **Связи:** WP-73, DP.SC.112, DP.SC.114, DP.SYS.001
> **Смежные системы:** WP-109 (Activity Hub — получает payment events), WP-121 (Points Engine — отдельная система начисления баллов), WP-115 (Семинар — ключевой сценарий)
> **АрхГейт:** 62/70 ✅
> **Приложение:** [WP-183-crm-billing-research-appendix.md](WP-183-crm-billing-research-appendix.md)

## Проблема

Sales-команда (5 чел) управляет контактами, вузовскими группами, оплатами. **Основной поток оплаты остаётся как сейчас** (YooKassa через LMS, подписки через бота). Дополнительно нужно поддержать: оплату звёздами Telegram, попадание в чат **без email и аккаунта** на платформе, ручной ввод вузовских групп. Нужны CRM, billing и access management — на единой Neon PG, без второй БД.

## Решение: Directus + Metabase

**Directus** оборачивает существующие таблицы Neon (schemas `crm`, `finance`). Не создаёт свою БД — introspects вашу. RBAC с row-level policies. REST + GraphQL API автогенерируются.

```
                      ┌─────────────────────────────┐
                      │        ИНТЕРФЕЙСЫ            │
                      │                              │
  Telegram Bot ◄──────┤  Directus UI     Metabase    │
  (менеджеры на       │  (руководитель   (дашборды:  │
   телефоне +         │   на компе:      MRR, воронка│
   участники)         │   таблицы,       LTV, баллы) │
                      │   bulk import,               │
                      │   группы)                    │
                      └──────────┬──────────────────┘
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
| **Metabase** | Дашборды: MRR, воронка, баллы, unit economics | AGPL-3.0 | 1 GB |
| **Billing Service** | Strategy pattern: 5 адаптеров | Своё | В составе бота |

**Без n8n.** Directus Flows покрывают автоматизации на Phase 0-1 (триггер на INSERT → HTTP POST → бот). n8n — опция на Phase 2+, если появятся сложные цепочки (5+ шагов, условия, параллельные ветки). Одним компонентом меньше.

### Интерфейсы для менеджеров

| Где | Что | Когда |
|-----|-----|-------|
| **Telegram-бот** (телефон) | `/contact`, `/group`, `/pay`, `/pipeline`, `/at_risk` — быстрые операции | На ходу, в чате с клиентом |
| **Directus UI** (браузер на компе) | Таблицы контактов, bulk import CSV, создание/управление группами, настройка доступов, полная карточка контакта | В офисе, сложные операции |
| **Metabase** (браузер) | Дашборды: MRR, воронка, баллы, когорты, unit economics | Руководитель, планёрка |

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

1. Участник оплачивает звёздами в боте
2. Billing Service → `finance.payments` (telegram_id, amount, method=tg_stars)
3. Directus Flow триггерится → `crm.chat_access` (telegram_id, chat_id, expires_at)
4. Бот добавляет в чат по telegram_id
5. Позже (если зарегистрируется) → склейка: `crm.identity_links` (telegram_id ↔ ory_id)

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
| Инфраструктура | $12/мес (без n8n) |
| **Маржа** | **$438/мес** |
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

## Effort

| Phase | Что | Часы |
|-------|-----|------|
| **0** | Схемы Neon + Directus + TG Stars + CRM-команды бота + Metabase | 40h |
| **1** | YooKassa/Stripe интеграция в Billing Service + revenue sharing + баллы + полная аналитика | 40h |
| **2** | Identity linking, B2B лицензии, feature gating, at-risk автоматизация, n8n (если нужен) | По мере роста |

## Открытые вопросы

| # | Вопрос |
|---|--------|
| Q1 | Access Management (chat_access) — часть Billing Service или отдельная SYS.019? |
| Q2 | Billing Service — модуль бота (Phase 0) или отдельный сервис (Phase 1+)? |
| Q3 | BSL 1.1 Directus — приемлемо? (бесплатно до $5M, GPLv3 через 3 года) |
| Q4 | ~~Баллы — schema `points` отдельно или часть `finance`?~~ → Решено: баллы в `finance.point_*`, но **система начисления (WP-121) отдельна** от CRM |
| Q5 | Billing adapter для Activity Hub (WP-109) — реализовать в Phase 0 CRM или в Ф0 Activity Hub? |
| Q6 | `crm.events` (семинары, потоки) — нужна таблица для WP-115. Включить в Phase 0? |

---

*26 марта 2026. Обновлено: связи WP-109/121/115, разделение систем.*
