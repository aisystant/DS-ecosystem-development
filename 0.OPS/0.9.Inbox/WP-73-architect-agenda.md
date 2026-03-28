# WP-73 + WP-183: Agenda для архитектора — открытые вопросы

> **Дата:** 28 марта 2026 | **Дедлайн WP-73:** W14
> **Цель:** получить решения по блокирующим вопросам для завершения Phase 2 архитектуры
> **Формат:** 31 вопрос, приоритизирован по влиянию на реализацию

<details>
<summary><b>Источники (документы в этой папке)</b></summary>

| Документ | Статус | Что содержит |
|----------|--------|-------------|
| [WP-73 — Архитектурный план](WP-73-aisystant-platform-architecture.md) | in_progress | Зонтичный: as-is, to-be, gap, ADR, roadmap (~1750 строк) |
| [WP-74 — Концепция использования](WP-74-platform-concept-of-use.md) | in_progress | 9 ролей, 17+ сценариев, тиры, UX (~430 строк) |
| [WP-183 — CRM + Billing proposal](WP-183-crm-billing-architecture-proposal.md) | proposal v7 | Directus + Metabase + Billing Module. АрхГейт 60/70 |
| [WP-183 — Research appendix](WP-183-crm-billing-research-appendix.md) | приложение | Исследование 16 CRM, сравнение, АрхГейт |
| [WP-109 — Activity Hub proposal](WP-109-activity-hub-lms-integration-proposal.md) | approved | LMS → ЦД интеграция. Заблокирован на DE-35 |
| [WP-115 — Сценарий семинара](WP-115-seminar-payment-access-scenario.md) | draft | End-to-end: маркетинг → оплата → доступ → видео |
| [WP-168 — Миграция SurrealDB → Neon](../0.99.Archive/WP-168-surrealdb-to-neon-migration.md) | ~~in_progress~~ → архив | Ф0-Ф1 done, Ф2-Ф3 ожидают доступы |

</details>

---

## Tier 1: КРИТИЧЕСКИЕ (блокируют реализацию нескольких систем)

> Решения по этим вопросам разблокируют CRM, Billing, Web App, ЦД и Knowledge Gateway одновременно.

### 1. Изоляция данных в Neon — RLS vs schema vs DB

**Источник:** [WP-73 §5.1 Q1](WP-73-aisystant-platform-architecture.md) | **Блокирует:** CRM, Billing, ЦД, Knowledge Gateway, масштабирование

**Почему проблема:** Единая Neon PG — фундамент всей архитектуры (5 schemas: public, development, finance, connections, operations). CRM ([Directus](WP-183-crm-billing-architecture-proposal.md)) оборачивает эти схемы напрямую. Без решения по изоляции невозможно:
- определить, как Directus видит данные разных пользователей
- гарантировать, что менеджер CRM не видит чужие финансовые записи
- масштабировать на 3K+ пользователей (capacity plan из DECK)

**Варианты:**

| # | Вариант | Плюсы | Минусы |
|---|---------|-------|--------|
| A | **RLS (Row-Level Security)** | Одна БД, одна схема. Directus/Metabase работают нативно. Стандарт PostgreSQL | Сложность отладки RLS-политик. Один баг = утечка данных. Тестирование RLS = отдельный процесс |
| B | **Schema per tenant** | Полная изоляция на уровне схемы | Не масштабируется: 1000 tenant = 1000 schemas. Directus не поддерживает dynamic schema switching |
| C | **DB per tenant** | Максимальная изоляция | Neon per-project pricing. Невозможен cross-tenant query (Metabase). Слишком дорого |

**Рекомендация:** A (RLS). RBAC Directus + RLS Neon = двойной барьер.

---

### 2. ORY: hosted vs self-hosted + юрисдикция

**Источник:** [WP-73 §5.1 Q2, §2.7](WP-73-aisystant-platform-architecture.md) | **Блокирует:** единый SSO, Discourse SSO (→ #7), бот↔LMS identity federation, двух-юрисдикция (P12)

**Почему проблема:** ORY Network (hosted) уже интегрирована в digital-twin-mcp и LMS. Но:
- ORY хостится за границей → 152-ФЗ вопрос по ПД граждан РФ
- Self-hosted ORY Kratos/Hydra = свой деплой, своё обслуживание
- Бот на telegram_id (T0), LMS на email/пароль — два мира без связи
- Все будущие системы (Web App, CRM, Knowledge Gateway) зависят от единого identity
- [WP-115 (сценарий семинара)](WP-115-seminar-payment-access-scenario.md) — принято решение «Ory-first», но нужен путь реализации

**Варианты:**

| # | Вариант | Плюсы | Минусы |
|---|---------|-------|--------|
| A | **ORY Network (hosted) + DPA** | Уже работает. Zero ops. DPA покрывает GDPR | 152-ФЗ: ПД граждан РФ на зарубежных серверах |
| B | **Self-hosted ORY (EU + RU)** | Полный контроль. РФ-инстанс для 152-ФЗ | Ops-нагрузка: обновления, бэкапы, мониторинг. Два инстанса = синхронизация |
| C | **ORY Network (мир) + self-hosted (РФ)** | Гибрид: hosted для основного, РФ-данные отдельно | Два identity provider = сложная федерация |

**Рекомендация:** зависит от юридической консультации (→ #24). Если 152-ФЗ требует строгой локализации → B или C. Если DPA достаточно → A.

---

### 3. Event Bus: механизм межсервисного взаимодействия

**Источник:** [WP-73 §5.1 Q4](WP-73-aisystant-platform-architecture.md) | **Блокирует:** CRM↔бот, Billing→Activity Hub, [Activity Hub](WP-109-activity-hub-lms-integration-proposal.md)→Points Engine, все новые системы

**Почему проблема:** Сейчас интеграции — прямые вызовы (бот → Aisystant API, pull с кэшем 5 мин). Для новой архитектуры (60+ сервисов) нужна асинхронная шина. Без неё:
- [CRM Phase 0](WP-183-crm-billing-architecture-proposal.md) строится на синхронных INSERT — нормально для 5 менеджеров, но не масштабируется
- Нет push-уведомлений после оплаты (gap #1 из [WP-73 §2.9.1](WP-73-aisystant-platform-architecture.md))
- [Activity Hub](WP-109-activity-hub-lms-integration-proposal.md) не может агрегировать события без подписок

**Варианты:**

| # | Вариант | Плюсы | Минусы |
|---|---------|-------|--------|
| A | **Outbox + pg_notify** | Нулевая новая инфра (всё в Neon). Transactional outbox = надёжность | pg_notify теряет сообщения если слушатель отключён. Нужен poller как fallback |
| B | **RabbitMQ** | Гарантированная доставка. Dead letter queues | Новая инфра: Railway + $5-10/мес. Ops overhead |
| C | **NATS** | Легковесный. JetStream для persistence | Менее зрелая экосистема. Меньше интеграций |

**Рекомендация:** A для Phase 0 (уже в Neon), B при росте до 10+ подписчиков.

---

### 4. Neon always-on compute

**Источник:** [WP-183 Q7](WP-183-crm-billing-architecture-proposal.md) | **Блокирует:** все платежи через бота (YooKassa, Stripe, TG Stars)

**Почему проблема:** Neon autoscaling имеет cold start 1-3 сек. Webhook от YooKassa/Stripe ожидает 200 OK за <5 сек. Если Neon спит → таймаут → платёж не обработан → потеря денег. Критично для [сценария семинара](WP-115-seminar-payment-access-scenario.md) (TG Stars).

**Варианты:**

| # | Вариант | Плюсы | Минусы |
|---|---------|-------|--------|
| A | **Always-on compute (Neon)** | Гарантия <100ms. Простое включение | +$19/мес (0.25 CU) |
| B | **Retry в Billing Module** | Бесплатно. Exponential backoff | Первый запрос ~3 сек. Сложнее код |
| C | **Connection pooler warm-up** | pgBouncer поддерживает соединение | Не решает проблему compute sleep |

**Рекомендация:** A. $19/мес vs потерянные платежи — очевидно.

---

### 5. LMS Aisystant: замена vs обёртка (API)

**Источник:** [WP-73 §5.1 Q7, §2.4](WP-73-aisystant-platform-architecture.md) | **Блокирует:** Web App MVP (WP-65), все LMS-зависимые сценарии, CRM↔LMS

**Почему проблема:** LMS — Java 8 / Vaadin 8 монолит. Содержит все курсы, подписки, оплаты (5 платёжных систем), прогресс обучения. [Activity Hub](WP-109-activity-hub-lms-integration-proposal.md) уже предполагает LMS-адаптер — но через какой интерфейс?

**Варианты:**

| # | Вариант | Плюсы | Минусы |
|---|---------|-------|--------|
| A | **Обёртка (API) на 12 мес** | Быстро. Сохраняет работающее | Lock-in в legacy на год+. API LMS ограничен |
| B | **Постепенная замена** (strangler fig) | Новые фичи в новом стеке. LMS уменьшается | Два стека параллельно. Сложность синхронизации |
| C | **Полная замена** | Чистый стек | 1000+ часов. Нереалистично |

**Рекомендация:** A с планом перехода к B через 12 мес.

---

## Tier 2: ВАЖНЫЕ (блокируют отдельные системы или фичи)

### 6. Web App hosting: Vercel vs Railway vs CF Pages

**Источник:** [WP-73 §5.1 Q3](WP-73-aisystant-platform-architecture.md) | **Блокирует:** WP-65 Web App MVP

| Вариант | Плюсы | Минусы |
|---------|-------|--------|
| **Vercel** | SSR + Edge + AI SDK. Next.js native. CDN | Vendor lock-in. Цена при росте |
| **Railway** | Уже используем (бот). Единая платформа | Нет Edge, AI SDK, ISR |
| **CF Pages** | Бесплатно. Edge. Рядом с MCP Workers | Ограниченный SSR. Нет Next.js native |

**Рекомендация:** Vercel.

### 7. Discourse SSO через ORY

**Источник:** [WP-73 §5.1 Q5](WP-73-aisystant-platform-architecture.md) | **Блокирует:** единый identity для Клуба

DiscourseConnect + ORY — стандартный путь. Зависит от решения по #2 (ORY). Вопрос: реализовать до или после Web App?

### 8. Каналы для команд SC-8

**Источник:** [WP-73 §5.1 Q6](WP-73-aisystant-platform-architecture.md), [WP-74 SC-8](WP-74-platform-concept-of-use.md) | **Блокирует:** командообразование

TG-группы (аудитория уже в Telegram) vs Zulip (topic-based threading, open-source) vs Discord (голос, реал-тайм). Design input по Zulip — в WP-73 context file.

### 9. Кеш: Redis vs CF KV

**Источник:** [WP-73 §5.1 Q8](WP-73-aisystant-platform-architecture.md) | **Блокирует:** перформанс MCP и Web App

CF KV для MCP (уже на CF Workers) + Vercel KV для Web App — по месту деплоя. Или единый Redis?

### 10. Access Management — часть Billing или отдельная система?

**Источник:** [WP-183 Q1](WP-183-crm-billing-architecture-proposal.md) | **Блокирует:** архитектура доступов

chat_access = следствие платежа → часть Billing Module. Но feature gating (тиры T1-T4) = отдельная логика. Где граница? [WP-115](WP-115-seminar-payment-access-scenario.md) предполагает access management как часть потока оплаты.

### 11. BSL 1.1 лицензия Directus

**Источник:** [WP-183 Q3](WP-183-crm-billing-architecture-proposal.md) | **Блокирует:** выбор CRM-инструмента

BSL разрешает до $5M revenue. Через 3 года → GPLv3. Зафиксировать в ADR. [Исследование альтернатив](WP-183-crm-billing-research-appendix.md) — 16 CRM проверены, ни одна не подходит.

### 12. CRM Phase 0 scope

**Источник:** [WP-183 Q5, Q6](WP-183-crm-billing-architecture-proposal.md) | **Блокирует:** порядок реализации

- Billing adapter для [Activity Hub](WP-109-activity-hub-lms-integration-proposal.md) — в Phase 0? (Рекомендация: да, `ingest_event()`)
- `crm.events` для [WP-115 семинаров](WP-115-seminar-payment-access-scenario.md) — в Phase 0? (Рекомендация: да, базовая таблица)

### 13. Chargeback-политика

**Источник:** [WP-183 Q10](WP-183-crm-billing-architecture-proposal.md) | **Блокирует:** Revenue Sharing, выплаты авторам

Hold period 14 дней. Если после settlement — вычитать из следующей выплаты. Нужно формальное решение.

### 14. Репликация данных RU↔EU

**Источник:** [WP-73 §5.1 Q13, §3.4](WP-73-aisystant-platform-architecture.md) | **Блокирует:** двух-юрисдикционная архитектура (P12)

Какие данные реплицируются? Eventual vs strong consistency? Зависит от #2 (ORY) и #24 (152-ФЗ).

---

## Tier 3: Knowledge Gateway / BYOB (блокируют WP-187, WP-189)

> Вопросы из [WP-73 §3.8 MCP Hub](WP-73-aisystant-platform-architecture.md). ADR-018 (BYOB, ЭМОГССБ 9.1) принят, нужны решения по реализации.

### 15. Gateway: отдельный процесс или встроен в personal-mcp?

**KG-Q1** | Рекомендация: встроен (меньше движущихся частей)

### 16. Embeddings L4: CF AI vs локальная vs OpenAI?

**KG-Q2** | Рекомендация: CF AI (бесплатно, единая модель с L2)

### 17. Merge L2+L4: простой vs weighted vs cascade?

**KG-Q3** | Рекомендация: простой merge по score для MVP

### 18. Подключение gateway: stdio vs SSE vs Hub?

**KG-Q4** | Рекомендация: stdio MCP (стандарт для Claude Code)

### 19. Knowledge Gateway — с какого тира? T3 или T4?

**KG-Q5** | T3 = больше пользователей, T4 = premium-фича. Продуктовое решение.

### 20. Web App UI для управления sources?

**KG-Q6** | CLI/config для MVP или Web App UI? Зависит от #6 (Web App hosting).

### 21. Community MCP: публикация Pack другим?

**KG-Q7** | Hub vs P2P. Зависит от ADR-018 (BYOB).

### 22. Миграция knowledge-mcp: сразу или поэтапно?

**KG-Q8** | Рекомендация: поэтапно (Ф1: выделить L2 → Ф2: L4 + gateway). [WP-168](../0.99.Archive/WP-168-surrealdb-to-neon-migration.md) (SurrealDB → Neon) — предпосылка, Ф0-Ф1 done.

### 23. DS-Knowledge-Index + aist-bot-docs → L4?

**KG-Q9** | Breaking change для текущих сессий Claude Code. Нужен план миграции.

---

## Tier 4: ЮРИДИЧЕСКИЕ (внешние зависимости)

> Параллельный трек. Результаты влияют на #2 (ORY), #14 (репликация), #27 (хостинг).

### 24. 152-ФЗ: scope локализации ПД граждан РФ

**Источник:** [WP-73 §5.2 Q9](WP-73-aisystant-platform-architecture.md)

Что именно считается ПД? ФИО + email = очевидно. Telegram ID? Данные обучения? Прогресс? От ответа зависит, что должно храниться в РФ. Влияет на [двух-юрисдикцию (§3.4)](WP-73-aisystant-platform-architecture.md).

### 25. Санкционный compliance

**Источник:** [WP-73 §5.2 Q11](WP-73-aisystant-platform-architecture.md)

Автоматическая проверка санкционных списков или ручная верификация? Stripe/Anthropic API — ограничения для пользователей из РФ?

### 26. Два юрлица или одно?

**Источник:** [WP-73 §5.2 Q14](WP-73-aisystant-platform-architecture.md) | **Блокирует:** WP-186 (юрготовность)

РФ-юрлицо + международное (US LLC / Estonia OÜ) — или единое? Влияет на Revenue Sharing, IP ownership, investor structure.

### 27. Выбор РФ-хостинга

**Источник:** [WP-73 §5.3 Q12](WP-73-aisystant-platform-architecture.md)

Hetzner Russia vs VK Cloud vs Selectel. Зависит от #24 (что именно локализовать).

---

## Tier 5: СТРАТЕГИЧЕСКИЕ (не блокируют, но влияют на roadmap)

**Источник:** [WP-73 §5.4](WP-73-aisystant-platform-architecture.md), [WP-74](WP-74-platform-concept-of-use.md)

| # | Вопрос | Связь |
|---|--------|-------|
| 28 | B1-B8: детальные решения по тирам T1→T4 | [WP-74 §3](WP-74-platform-concept-of-use.md) |
| 29 | C4: unit economics по тирам | Бизнес-модель |
| 30 | C6: 25 репо → масштабируемость | DevOps |
| 31 | Платформа Андрея (Discourse): замена или обёртка? | Клуб |

---

## Порядок обсуждения (рекомендация)

| Встреча | Время | Что обсуждаем | Что разблокируем |
|---------|-------|---------------|------------------|
| **1. Фундамент** | ~60 мин | #1 RLS, #2 ORY, #3 Event Bus, #4 Always-on, #5 LMS | CRM, Billing, Web App, ЦД |
| **2. Системы** | ~45 мин | #6 Vercel, #7 Discourse SSO, #10-12 CRM scope, #13 Chargeback | WP-65, WP-115, WP-183 |
| **3. Knowledge Gateway** | ~30 мин | #15-23 блоком | WP-187, WP-189 |
| **Юридика** | отдельно | #24-27 параллельным треком | Двух-юрисдикция, WP-186 |

---

<details>
<summary><b>Состояние документов в Inbox (ревью 28 мар)</b></summary>

### Активные документы

| Документ | Статус | Следующее действие |
|----------|--------|-------------------|
| [WP-73 — Архитектура](WP-73-aisystant-platform-architecture.md) | in_progress | Phase 2: спецификации модулей. Ждёт решения Tier 1 |
| [WP-74 — Концепция](WP-74-platform-concept-of-use.md) | in_progress | SC.101-116 формализованы. Обновляется параллельно с WP-73 |
| [WP-183 — CRM proposal](WP-183-crm-billing-architecture-proposal.md) | proposal v7 | Ждёт решение архитектора (Q1-Q11) |
| [WP-183 — Research](WP-183-crm-billing-research-appendix.md) | приложение | Завершён. Привязан к proposal |
| [WP-109 — Activity Hub](WP-109-activity-hub-lms-integration-proposal.md) | approved | Реализация заблокирована на DE-35 |
| [WP-115 — Семинар](WP-115-seminar-payment-access-scenario.md) | draft | На обсуждение. Зависит от WP-183 |
| ~~[WP-168 — SurrealDB → Neon](../0.99.Archive/WP-168-surrealdb-to-neon-migration.md)~~ | архив (28 мар) | Ф0-Ф1 done. Ф2-Ф3 ожидают доступы |
| **Этот документ** (Agenda) | active | Обновлять по мере получения решений |

### Кандидаты на архив (после завершения)

- ~~**WP-168**~~ — **перемещён в архив 28 мар** (Ф0-Ф1 done, Ф2-Ф3 ожидают доступы)
- **WP-183 Research appendix** — после принятия proposal → архив (решения зафиксированы в ADR)
- **WP-109** — после реализации Activity Hub → архив (знание в Pack)

### Отсутствующие (упомянуты, но не созданы)

- ~~`WP-73-knowledge-gateway-byob-proposal.md`~~ — содержание мержнуто в [WP-73 §3.8](WP-73-aisystant-platform-architecture.md). Отдельный файл не нужен

</details>

---

*28 марта 2026. Консолидировано из: [WP-73 §5](WP-73-aisystant-platform-architecture.md), [WP-183 proposal](WP-183-crm-billing-architecture-proposal.md), [WP-73 §3.8](WP-73-aisystant-platform-architecture.md).*
