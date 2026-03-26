# WP-183: CRM + Billing — предложение архитектору

> **Статус:** proposal | **Источник:** оперативка ИТ 26 мар 2026
> **Связи:** WP-73, DP.SC.112, DP.SC.114, DP.SYS.001
> **АрхГейт:** 62/70 ✅

## Проблема

Sales-команда (5 чел) управляет контактами, вузовскими группами, оплатами. Участники платят звёздами Telegram, попадают в чат **без email и аккаунта** на платформе. Нужны CRM, billing и access management — на единой Neon PG, без второй БД.

## Решение: Directus + Metabase + n8n

**Directus** оборачивает существующие таблицы Neon (schemas `crm`, `finance`). Не создаёт свою БД — introspects вашу. RBAC с row-level policies. REST + GraphQL API автогенерируются.

```
Telegram Bot ──────────→ Neon PG ←──── Directus (UI для руководителя)
  (менеджеры: /contact,     ↑              ↑
   /group, /pay)            │              │
Billing Service ───────────→│         Metabase (MRR, воронка, LTV)
  (YooKassa/Stripe/Stars)   │
n8n ←── триггер на INSERT ──┘
  (платёж → добавить в чат → уведомить менеджера)
```

| Компонент | Роль | Лицензия | RAM |
|-----------|------|----------|-----|
| **Directus** | CRM UI + API + RBAC | BSL 1.1 (GPLv3 через 3 года) | 512 MB |
| **Metabase** | Дашборды | AGPL-3.0 | 1 GB |
| **n8n** | Оркестрация автоматизаций | AGPL-3.0 | 512 MB |
| **Billing Service** | Strategy pattern: 4 адаптера | Своё | В составе бота |

**Менеджеры работают в Telegram-боте** (ноль обучения): `/contact`, `/group`, `/pay`, `/pipeline`, `/at_risk`. Directus — для руководителя и сложных операций (bulk import вузовских групп, настройка RBAC).

## Ключевой сценарий: оплата звёздами → чат без email

1. Участник оплачивает звёздами в боте
2. Billing Service → `finance.payments` (telegram_id, amount, method=tg_stars)
3. n8n триггерится → `crm.chat_access` (telegram_id, chat_id, expires_at)
4. Бот добавляет в чат по telegram_id
5. Позже (если зарегистрируется) → склейка: `crm.identity_links` (telegram_id ↔ ory_id)

## Billing Service — Strategy pattern

```
Billing Service (orchestrator)
  ├── YooKassa  (РФ, подписки)
  ├── Stripe    (мир, подписки)
  ├── TG Stars  (Telegram, события)
  ├── Баллы     (внутренняя валюта)
  └── Manual    (B2B, менеджер регистрирует)
```

Revenue sharing: platform 30%, author 50%, instructor 15%, curator 5%.

## Unit economics

| Метрика | При 100 подписчиках T2 ($15/мес) |
|---------|----------------------------------|
| MRR | $1 500 |
| Platform share (30%) | $450 |
| Инфраструктура | $17/мес |
| **Маржа** | **$433/мес** |
| Окупаемость разработки ($4 000) | **~9 мес** |

B2B: 2 вуза × 50 чел × $15 × 12 мес = $18 000/год → окупаемость **~3 мес**.

## Effort

| Phase | Что | Часы |
|-------|-----|------|
| **0** | Схемы Neon + Directus + TG Stars + CRM-команды бота + Metabase | 40h |
| **1** | YooKassa + Stripe + n8n автоматизации + revenue sharing + полная аналитика | 40h |
| **2** | Identity linking, B2B лицензии, feature gating, at-risk автоматизация | По мере роста |

## Открытые вопросы

| # | Вопрос |
|---|--------|
| Q1 | Access Management (chat_access) — часть Billing Service или отдельная SYS.019? |
| Q2 | Billing Service — модуль бота (Phase 0) или отдельный сервис (Phase 1+)? |
| Q3 | n8n или Directus Flows на Phase 0? (n8n = меньше coupling, Flows = проще старт) |
| Q4 | BSL 1.1 Directus — приемлемо? (бесплатно до $5M, GPLv3 через 3 года) |

---

*26 марта 2026*
