# WP-183: CRM + Billing — исследование (приложение)

> **Приложение к:** [WP-183-crm-billing-architecture-proposal.md](WP-183-crm-billing-architecture-proposal.md)
> **Содержит:** полное исследование рынка, АрхГейт двух вариантов, детальные сценарии

---

<details open>
<summary><b>1. Проблема</b></summary>

Нужна система для трёх задач:
1. **CRM** — sales-команда из 5 человек управляет контактами, вузовскими группами, лидами
2. **Billing** — приём оплаты (YooKassa, Stripe, Telegram Stars), подписки T1-T4, revenue sharing
3. **Access Management** — допуск в чаты по telegram_id, управление доступами

Специфика:
- **telegram_id как primary identity** (не email) — участник может не иметь email
- **Оплата звёздами Telegram** — участник платит в боте, попадает в чат, потом (может быть) регистрируется на платформе
- **Два потока:** самообслуживание (90%+, бот → Ory → Trial) и ручной ввод (~10%, вузы, B2B)
- **Единая БД:** Neon PostgreSQL = system of record (DP.ARCH.001)

</details>

<details open>
<summary><b>2. Исследование рынка</b></summary>

### Внешние CRM — не подходят

| Решение | Почему не подходит |
|---------|-------------------|
| **Twenty** | Нет понятия группы (подтвердил архитектор). Своя БД. Нет billing |
| **EspoCRM** | PostgreSQL = experimental. Отдельная MariaDB. Бот через API = SPOF |
| **SuiteCRM** | Только MySQL. Устаревший UI |
| **Odoo CE** | Тяжёлый ERP. Subscriptions только в Enterprise (платно) |
| **Erxes** | Только MongoDB |
| **ERPNext** | Тяжёлый ERP для «только CRM». UI менее современный |
| **Frappe CRM** | Молодой. Зависит от Frappe Bench (сложная настройка) |
| **Dolibarr** | Устаревший UI. ERP/CRM — всё поверхностно |
| **Krayin** | Базовые CRM-функции. По умолчанию MySQL |
| **CiviCRM** | Только MySQL. Для НКО. Не standalone |
| **Monica** | Персональный CRM, не бизнес. Проект полумёртв |
| **IDURAR** | MongoDB. «Fair-code» ≠ open-source. Один разработчик |

### Полная таблица: open-source CRM с PostgreSQL

| CRM | Stars | Лицензия | PostgreSQL | Billing | Зрелость |
|-----|-------|----------|------------|---------|----------|
| **Twenty** | 41k | AGPL-3.0 | Нативно | Нет | Молодой (2023) |
| **Odoo CE** | 50k | LGPL-3.0 | Нативно | Да (CE урезан) | Зрелый |
| **EspoCRM** | 3k | AGPL-3.0 | Experimental (v9) | Базовый | Зрелый (2014) |
| **ERPNext** | 32k | GPL-3.0 | Да | Да (полный) | Зрелый |
| **Frappe CRM** | 2.5k | AGPL-3.0 | Да | Нет | Молодой (2023) |
| **Dolibarr** | 7k | GPL-3.0 | Да | Да | Очень зрелый (2002) |
| **Corteza** | 2k | Apache-2.0 | Да | Нет | Средний |

### Coda-based подход (идея архитектора)

Рассмотрены open-source клоны Coda/Airtable:

| Инструмент | Подключение к существующей Neon PG | Лицензия | Проблемы |
|------------|-----------------------------------|----------|----------|
| **NocoDB** | Да, core feature | Sustainable Use (не open-source!) | Только `public` schema, нет RLS, metadata sync хрупкий |
| **Teable** | **Нет** (требует выделенную БД) | AGPL-3.0 | Не может работать с существующими таблицами |
| **Baserow** | Нет (только как бэкенд) | MIT + Proprietary | Kanban и RBAC — платные |
| **NocoBase** | Да (плагин, платный) | AGPL-3.0 | Менее зрелый, документация слабая |

### Admin panel подход

| Инструмент | Подключение к Neon PG | CRM UI | RBAC | Webhooks |
|------------|----------------------|--------|------|----------|
| **Directus** | **Да, native** (introspects schema) | Admin panel | **Да (row-level)** | **Flows — real-time** |
| **Budibase** | Да, native | App builder | Да | Да |
| **Appsmith** | Да, native | Ручная сборка | Да | Внешние |
| **ToolJet** | Да, native | Drag-and-drop | Да | Да |

</details>

<details open>
<summary><b>3. АрхГейт — два варианта</b></summary>

### Вариант 1: NocoDB + Metabase — ❌ НЕ ПРОХОДИТ

**Итого: 41/70** (порог 56)

| Характеристика | Оценка | Обоснование |
|----------------|--------|-------------|
| Эволюционируемость | **5** | Metadata sync ломается при внешних изменениях. Только `public` schema |
| Масштабируемость | **7** | Нет RLS → при росте команды все видят всё |
| Обучаемость | **8** | Spreadsheet-like UI — знакомый паттерн |
| Генеративность | **4** | Standalone инструмент, не работает в шаблоне экзокортекса |
| Скорость | **8** | Прямое чтение из PG |
| Современность | **5** | Sustainable Use License ≠ open-source (нарушает принцип #18) |
| Безопасность | **4** | Нет RLS — критический gap. Нарушает принцип #17 |

**Нарушения принципов:** #17 (три оси доступа — нет RLS), #18 (open-source first — лицензия), #2 (слабая связанность — metadata sync).

### Вариант 2: Directus + Metabase + n8n + Telegram CRM — ✅ ПРОХОДИТ

**Итого: 62/70**

| Характеристика | Оценка | Обоснование |
|----------------|--------|-------------|
| Эволюционируемость | **10** | Данные в Neon. Directus снимается без потери данных. n8n отвязывает автоматизации |
| Масштабируемость | **8** | RBAC v11 Policies. 5→50 пользователей — ок |
| Обучаемость | **9** | Менеджеры в Telegram (ноль обучения). Directus — для руководителя |
| Генеративность | **8** | CRM-команды бота шаблонизируемы. Directus переиспользуется |
| Скорость | **8** | REST/GraphQL поверх PG. n8n real-time |
| Современность | **8** | Headless data platform — SOTA. BSL 1.1 с GPLv3 fallback |
| Безопасность | **8** | RBAC v11 Policies: item-level, field-level, $CURRENT_USER |

**L2 расширения:**
- Переносимость данных: 8.3/10 ✅ (данные в PG, open format, vendor independence)
- Интероперабельность: 8.3/10 ✅ (REST + GraphQL + SQL, OpenAPI auto-generated)

**Сверка с принципами:**
- #2 (Слабая связанность) ✅ — Directus = тонкий слой, данные в Neon
- #12 (Интерфейсы через обработку) ✅ — Directus = Слой 2 + 3
- #17 (Три оси доступа) ✅ — RBAC v11 Policies
- #18 (Open-source first) ⚠️ — BSL 1.1, обоснование: нет open-source аналога с introspect PG + RBAC + Flows
- #20 (Integrate SOTA) ✅ — headless data platform

</details>

<details>
<summary><b>4. Детальные сценарии использования</b></summary>

### Сценарий A: Оплата звёздами → чат (без email)

```
1. Участник нажимает «Оплатить» в Telegram-боте
2. Бот создаёт Telegram Stars invoice (Telegram Payments API)
3. Участник оплачивает звёздами в Telegram
4. Бот получает successful_payment callback
5. Billing Service записывает в finance.payments:
   (telegram_id, amount=500stars, method=tg_stars, product=seminar_X)
6. n8n триггерится на INSERT в finance.payments:
   → INSERT в crm.chat_access (telegram_id, chat_id, expires_at=+30d)
   → Бот добавляет участника в чат (Telegram API: unbanChatMember)
   → Уведомление менеджеру: «@username оплатил семинар X»
7. Участник в чате. Email не нужен. Аккаунта на платформе нет.
8. (Позже) Участник регистрируется → Ory identity создаётся →
   crm.identity_links: telegram_id ↔ ory_identity_id → склейка данных
```

### Сценарий B: Вузовская группа (ручной ввод)

```
1. Sales-менеджер получает список 20 студентов от вуза
2. В Directus: Import CSV → collection «Группы» + collection «Контакты»
   (имя, telegram_username, группа=«МГУ Поток-5», статус=лид)
3. Менеджер отмечает оплату: статус → «оплачен» (вуз заплатил за всех)
4. n8n триггерится: для каждого контакта в группе →
   INSERT в crm.chat_access → бот добавляет в чат
5. Metabase: дашборд показывает группу в воронке
6. Через месяц: менеджер проверяет — кто зарегистрировался на платформе?
   Directus view: контакты группы + статус регистрации
```

### Сценарий C: Подписка через YooKassa/Stripe

```
1. Участник (Ory identity есть) нажимает /subscribe в боте
2. Бот → Billing Service → YooKassa/Stripe: создать подписку T2
3. Webhook → Billing Service:
   INSERT finance.subscriptions (ory_id, tier=T2, expires=+30d, auto_renew=true)
   INSERT finance.transactions (ory_id, amount=1500rub, provider=yookassa)
4. n8n триггерится:
   → Обновить Ory metadata: tier=T2
   → Бот: разблокировать T2-функции
5. Автопродление: Billing Service по cron → recurrent charge → продление
6. При неоплате: grace period 7 дней → понижение до T1
```

### Сценарий D: Менеджер работает через Telegram-бота

```
/contacts                       → список моих контактов
/contact @username              → карточка: имя, тир, платежи, группа, чаты
/add Иван Петров @ivanp МГУ-5  → создать контакт + привязать к группе
/pay @ivanp 5000 stars семинар  → зарегистрировать платёж
/group МГУ-5                    → список участников группы + статусы
/pipeline                       → мои сделки по стадиям
/at_risk                        → кто не активен 14+ дней
/stats                          → мои метрики: конверсия, MRR
```

</details>

<details>
<summary><b>5. Billing Service — детальная спецификация</b></summary>

### Strategy pattern: 5 адаптеров

```
                    ┌─────────────────┐
                    │ Billing Service  │
                    │  (orchestrator)  │
                    └────────┬────────┘
           ┌────────┬────────┼────────┬────────┐
           ▼        ▼        ▼        ▼        ▼
      ┌────────┐┌────────┐┌────────┐┌────────┐┌────────┐
      │YooKassa││ Stripe ││TG Stars││ Баллы  ││ Manual │
      │(РФ)    ││(мир)   ││(TG)    ││(внутр.)││(B2B)   │
      └────────┘└────────┘└────────┘└────────┘└────────┘
```

| Адаптер | Триггер | Webhook | Что записывает |
|---------|---------|---------|----------------|
| **YooKassa** | /subscribe → confirmationUrl | `payment.succeeded` | finance.transactions + finance.subscriptions |
| **Stripe** | /subscribe → Checkout Session | `checkout.session.completed` | finance.transactions + finance.subscriptions |
| **TG Stars** | «Оплатить» → Stars invoice | `successful_payment` (bot callback) | finance.payments (telegram_id) |
| **Баллы** | /buy_with_points | Внутренний | finance.payments + point_transactions |
| **Manual** | Менеджер → Directus/бот | — | finance.payments (manual=true, operator_id) |

### Схема данных (Neon)

```sql
-- Schema: crm
crm.leads (
  id, telegram_id, telegram_username, name, email NULL,
  source, assigned_to, status, group_id NULL, created_at
)

crm.groups (
  id, name, organization, cohort_year, manager_id, created_at
)

crm.chat_access (
  id, telegram_id, chat_id, granted_at, expires_at, granted_by
)

crm.identity_links (
  id, telegram_id, ory_identity_id, linked_at
)

crm.activities (
  id, lead_id, type: call|meeting|note|email,
  description, manager_id, created_at
)

-- Schema: finance
finance.subscriptions (
  id, ory_identity_id, tier, started_at, expires_at,
  auto_renew, provider, provider_subscription_id,
  status: active|expired|cancelled|grace_period
)

finance.transactions (
  id, ory_identity_id NULL, telegram_id NULL,
  amount, currency, provider, provider_tx_id,
  product_type: subscription|event|course,
  product_id, status, created_at
)

finance.revenue_share (
  id, transaction_id, recipient_role: author|instructor|curator|platform,
  share_percent, amount, status: pending|paid
)
```

### Revenue Sharing (из WP-73)

| Роль | Доля |
|------|------|
| Platform | 30% |
| Author | 50% |
| Instructor | 15% |
| Curator | 5% |

</details>

<details>
<summary><b>6. Unit Economics — детальный расчёт</b></summary>

### Стоимость инфраструктуры (месяц)

| Компонент | Хостинг | Стоимость/мес |
|-----------|---------|---------------|
| Directus | Railway (512 MB) | ~$5 |
| Metabase | Railway (1 GB) | ~$7 |
| n8n | Railway (512 MB) | ~$5 |
| Neon PostgreSQL | Уже есть (shared) | $0 (incremental) |
| **Итого** | | **~$17/мес** |

### Стоимость разработки (единоразово)

| Этап | Effort | Стоимость (при $50/h) |
|------|--------|-----------------------|
| Directus: деплой + настройка | 8h | $400 |
| CRM Telegram-команды для бота | 16h | $800 |
| Billing Service (Strategy pattern) | 24h | $1 200 |
| n8n: автоматизации | 8h | $400 |
| Metabase: дашборды | 8h | $400 |
| Тестирование + интеграция | 16h | $800 |
| **Итого** | **80h** | **$4 000** |

### Сценарии breakeven

| Сценарий | MRR | Platform (30%) | Маржа | Окупаемость |
|----------|-----|----------------|-------|-------------|
| 10 подписчиков T2 | $150 | $45 | $28 | ~143 мес ❌ |
| 50 подписчиков T2 | $750 | $225 | $208 | ~19 мес ⚠️ |
| 100 подписчиков T2 | $1 500 | $450 | $433 | **~9 мес** ✅ |
| 1 вуз (50 чел, 12 мес) | — | $2 700/год | $2 496/год | ~19 мес |
| 2 вуза | — | $5 400/год | $4 992/год | **~10 мес** ✅ |
| Mix: 50 B2C + 1 вуз | — | $225/мес + $225/мес | $433/мес | **~9 мес** ✅ |

### Ключевые метрики (Metabase dashboards)

| Метрика | Формула | Цель |
|---------|---------|------|
| **MRR** | SUM(active subscriptions × tier price) | Рост |
| **Churn** | Cancelled / Total active (monthly) | <5% |
| **LTV** | ARPU / Churn rate | >$180 (12 мес T2) |
| **CAC** | Marketing spend / New subscribers | <$30 |
| **Payback** | CAC / ARPU | <3 мес |
| **Revenue per group** | SUM(group payments) / groups | >$500 |
| **Conversion** | Paid / Total leads | >10% |

</details>

<details>
<summary><b>7. Directus vs EspoCRM — почему Directus</b></summary>

| Критерий | Directus | EspoCRM |
|----------|----------|---------|
| Neon PG (существующие таблицы) | **Нативно** — introspects schema | Experimental PG, не тестировано с Neon |
| Вторая БД | **Нет** — одна Neon | Да — отдельная MariaDB |
| Если упадёт | Бот и billing продолжают работать | Бот не может записать платёж (SPOF) |
| RBAC (row-level) | **v11 Policies** — item-level rules | Teams/Roles — зрелая модель |
| Webhooks | **Real-time** через Flows | Cron ~5 мин (real-time = платный Advanced Pack) |
| Email интеграция | Нет | Полная (IMAP/SMTP) |
| CRM-таймлайн | Нет (нужна custom collection) | Из коробки |
| Миграция | Легко снять — данные в Neon | Export/import |
| АрхГейт | **62/70** ✅ | Не оценивался (блокер: experimental PG) |

**Вывод:** EspoCRM лучше как CRM-продукт, но создаёт вторую БД и становится SPOF. Directus сохраняет архитектурный принцип единой Neon PG.

</details>

---

*26 марта 2026. Приложение к [WP-183-crm-billing-architecture-proposal.md](WP-183-crm-billing-architecture-proposal.md)*
