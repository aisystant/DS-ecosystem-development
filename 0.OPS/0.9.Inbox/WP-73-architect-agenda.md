# WP-73 + WP-183: Повестка обсуждения с архитектором

> **Дата:** 28 марта 2026 | **Дедлайн WP-73:** W14
> **Цель:** получить решения по критическим вопросам + согласовать принятые решения
> **Формат:** 2 блока — «нужно решение архитектора» и «информирование + совет»

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

</details>

---

## Блок А: КРИТИЧЕСКИЕ — нужно решение архитектора

> Без этих решений невозможно перейти к реализации. Нужно обсудить варианты и выбрать.

### А1. Изоляция данных в Neon — RLS vs schema vs DB

**Источник:** [WP-73 §5.1 Q1](WP-73-aisystant-platform-architecture.md) | **Блокирует:** CRM, Billing, ЦД, Knowledge Gateway, масштабирование

**Почему проблема:** Единая Neon PG — фундамент всей архитектуры (5 schemas: public, development, finance, connections, operations). CRM ([Directus](WP-183-crm-billing-architecture-proposal.md)) оборачивает эти схемы напрямую. Без решения по изоляции невозможно:
- определить, как Directus видит данные разных пользователей
- гарантировать, что менеджер CRM не видит чужие финансовые записи
- масштабировать на 3K+ пользователей (capacity plan из DECK)

**Варианты:**

| # | Вариант | Плюсы | Минусы |
|---|---------|-------|--------|
| A | **RLS (Row-Level Security)** | Одна БД, одна схема. Directus/Metabase работают нативно. Стандарт PostgreSQL | Сложность отладки RLS-политик. Один баг = утечка данных |
| B | **Schema per tenant** | Полная изоляция на уровне схемы | 1000 tenant = 1000 schemas. Directus не поддерживает dynamic schema switching |
| C | **DB per tenant** | Максимальная изоляция | Neon per-project pricing. Cross-tenant query невозможен (Metabase). Слишком дорого |

**Рекомендация:** A (RLS). RBAC Directus + RLS Neon = двойной барьер.

---

### А2. Event Bus: механизм взаимодействия между системами

**Источник:** [WP-73 §5.1 Q4](WP-73-aisystant-platform-architecture.md) | **Блокирует:** CRM↔бот, Billing→[Activity Hub](WP-109-activity-hub-lms-integration-proposal.md)→Points Engine, все новые системы

**Почему проблема:** Сейчас системы общаются напрямую (бот → Aisystant API, pull с кэшем 5 мин). Event Bus — это «доска объявлений» между системами: Billing пишет «оплата прошла», Activity Hub и бот читают каждый сам, когда нужно. При 500+ подписчиках и 7-10 системах (бот, CRM, Billing, Activity Hub, Points Engine, Notification Service, ЦД) прямые вызовы «каждый звонит каждому» превращаются в паутину.

**Вопрос архитектору:** согласен ли с поэтапным планом — начать с Outbox в Neon (Phase 0, бесплатно) и перейти на RabbitMQ при росте до 10+ систем? Или лучше сразу ставить RabbitMQ?

**Варианты:**

| # | Вариант | Плюсы | Минусы |
|---|---------|-------|--------|
| A | **Outbox + pg_notify (поэтапно)** | Нулевая новая инфра (всё в Neon). Transactional outbox = надёжность | pg_notify теряет сообщения если слушатель отключён. Нужен poller как fallback |
| B | **RabbitMQ (сразу)** | Гарантированная доставка. Dead letter queues. Готовые паттерны | +$5-10/мес. Ops overhead. Ещё один сервер |
| C | **NATS** | Легковесный. JetStream для persistence | Менее зрелая экосистема |

**Рекомендация:** A → B (поэтапно). Но нужно мнение архитектора — он знает нагрузку.

---

### А3. LMS Aisystant: замена vs обёртка (API)

**Источник:** [WP-73 §5.1 Q7, §2.4](WP-73-aisystant-platform-architecture.md) | **Блокирует:** Web App MVP (WP-65), все LMS-зависимые сценарии, CRM↔LMS

**Почему проблема:** LMS Aisystant — Java 8 / Vaadin 8 монолит (2014). Содержит все курсы, подписки, оплаты (5 платёжных систем), прогресс обучения. Все новые системы (Web App, [Activity Hub](WP-109-activity-hub-lms-integration-proposal.md), CRM) должны с ним взаимодействовать. Вопрос — через какой интерфейс? Архитектор знает LMS изнутри и понимает, какие API уже есть и насколько они покрывают потребности.

**Варианты:**

| # | Вариант | Плюсы | Минусы |
|---|---------|-------|--------|
| A | **Обёртка (API) на 12 мес** | Быстро. Сохраняет работающее. Web App вызывает LMS API | Lock-in в legacy на год+. API LMS может быть ограничен |
| B | **Постепенная замена** (strangler fig) | Новые фичи в новом стеке. LMS уменьшается | Два стека параллельно. Сложность синхронизации |
| C | **Полная замена** | Чистый стек | 1000+ часов. Нереалистично |

**Рекомендация:** A с планом перехода к B через 12 мес. Но нужен ответ архитектора: какие API у LMS уже есть? Можно ли получить прогресс, подписки, оплаты через API?

---

### А4. Web App hosting: Vercel vs Railway vs CF Pages

**Источник:** [WP-73 §5.1 Q3](WP-73-aisystant-platform-architecture.md) | **Блокирует:** WP-65 Web App MVP

| Вариант | Плюсы | Минусы |
|---------|-------|--------|
| **Vercel** | SSR + Edge + AI SDK. Next.js native. CDN | Vendor lock-in. Цена при росте |
| **Railway** | Уже используем (бот). Единая платформа | Нет Edge, AI SDK, ISR |
| **CF Pages** | Бесплатно. Edge. Рядом с MCP Workers | Ограниченный SSR. Нет Next.js native |

**Дополнительный контекст:** Next.js (React) — путь к мобильному приложению: PWA (иконка на экране, push-уведомления) → React Native (нативное приложение, переиспользуется код). Выбор стека сейчас определяет стоимость мобилки потом.

**Рекомендация:** Vercel.

---

### А5. Access Management — часть Billing или отдельная система?

**Источник:** [WP-183 Q1](WP-183-crm-billing-architecture-proposal.md) | **Блокирует:** архитектура доступов

**Почему проблема:** Сейчас всё управление доступами — внутри LMS (system-school.ru). Но в новой архитектуре появляются каналы оплаты **мимо LMS**:
- TG Stars (оплата прямо в Telegram, LMS не участвует)
- Ручная регистрация вузовских групп (менеджер вводит в CRM)
- Баллы (внутренняя валюта)

В этих случаях Billing Module (в боте) обрабатывает платёж и записывает в Neon. **Кто после этого выдаёт доступ?**

Есть два типа доступа:
1. **После оплаты** (chat_access) — заплатил за семинар → бот добавляет в чат. Прямое следствие платежа.
2. **По подписке** (feature gating) — тир T2 → доступны определённые функции бота, курсы, MCP.

Если Billing Module отвечает за оба типа — он становится «богом», который знает и про деньги, и про доступы, и про тиры. Это хрупко. Если Access Management отдельно — нужен ещё один компонент.

**Вопрос архитектору:** где провести границу между Billing и Access Management? Можно ли решить при реализации или нужно определить сейчас, чтобы не переделывать? Как это устроено в текущем LMS — смешано или разделено?

---

## Блок Б: СОГЛАСОВАНИЕ — решение принято, нужен совет или информирование

> Мы уже определились. Ставим в известность архитектора и спрашиваем, нет ли подводных камней.

### Б1. ORY: self-hosted в РФ ✅ решение принято

**Источник:** [WP-73 §5.1 Q2, §2.7, §3.4](WP-73-aisystant-platform-architecture.md)

**Решение:** поднимаем self-hosted ORY (Kratos/Hydra) в РФ для 152-ФЗ. ORY Network (hosted, EU) остаётся для международных пользователей. Два инстанса, единый identity через федерацию.

**Вопрос архитектору:** как лучше организовать федерацию двух инстансов? Один primary + один replica? Или два равноправных с sync?

---

### Б2. Neon always-on compute ✅ решение принято

**Источник:** [WP-183 Q7](WP-183-crm-billing-architecture-proposal.md)

**Решение:** включаем always-on (+$19/мес, 0.25 CU). Cold start 1-3 сек ломает webhook-обработку платежей (YooKassa/Stripe/TG Stars ждут ответ за <5 сек). Критично для [сценария семинара](WP-115-seminar-payment-access-scenario.md).

**Вопрос архитектору:** есть ли что-то, что мы не учли? Может, есть более элегантное решение?

---

### Б3. CRM: Directus + Metabase ✅ proposal готов

**Источник:** [WP-183 proposal](WP-183-crm-billing-architecture-proposal.md), [исследование](WP-183-crm-billing-research-appendix.md)

**Решение:** Все данные — в одной Neon PG. Directus = UI для руководителя (оборачивает существующие таблицы). Metabase = дашборды. Billing Module = модуль бота. 16 внешних CRM исследованы — ни одна не подходит (нет telegram_id, нет TG Stars, вторая БД). АрхГейт: 60/70.

**Вопрос архитектору:** замечания по proposal? Особенно: Directus BSL 1.1 лицензия, CRM Phase 0 scope (что включать первым), Billing adapter для [Activity Hub](WP-109-activity-hub-lms-integration-proposal.md).

---

### Б4. Discourse SSO через ORY

**Источник:** [WP-73 §5.1 Q5](WP-73-aisystant-platform-architecture.md)

DiscourseConnect + ORY — стандартный путь. **Вопрос:** реализовать до или после Web App? Какие подводные камни с текущим Discourse?

---

### Б5. Каналы для команд SC-8

**Источник:** [WP-73 §5.1 Q6](WP-73-aisystant-platform-architecture.md), [WP-74 SC-8](WP-74-platform-concept-of-use.md)

TG-группы (аудитория в Telegram) vs Zulip (topic-threading, open-source) vs Discord (голос). Не срочно, но хотим мнение.

---

### Б6. Кеш: CF KV + Vercel KV

**Источник:** [WP-73 §5.1 Q8](WP-73-aisystant-platform-architecture.md)

CF KV для MCP (уже на CF Workers) + Vercel KV для Web App — по месту деплоя. Единый Redis пока избыточен. Согласен?

---

### Б7. Chargeback-политика

**Источник:** [WP-183 Q10](WP-183-crm-billing-architecture-proposal.md)

Предложение: hold period 14 дней перед settlement авторам. Если chargeback после settlement — вычитать из следующей выплаты. Нужна валидация от архитектора (он знает текущий поток YooKassa).

---

### Б8. Репликация данных RU↔EU

**Источник:** [WP-73 §5.1 Q13, §3.4](WP-73-aisystant-platform-architecture.md)

Связано с Б1 (ORY self-hosted). Какие данные реплицируются между юрисдикциями? Eventual vs strong? Зависит от 152-ФЗ scope. Информируем архитектора о направлении, спрашиваем мнение по sync-механизму.

---

## Блок В: Knowledge Gateway / BYOB (блокируют WP-187, WP-189)

> Вопросы из [WP-73 §3.8 MCP Hub](WP-73-aisystant-platform-architecture.md). ADR-018 (BYOB, ЭМОГССБ 9.1) принят, нужны решения по реализации.

| # | Вопрос | Рекомендация | Тип |
|---|--------|-------------|-----|
| В1 | Gateway — отдельный процесс или встроен в personal-mcp? | Встроен (меньше частей) | совет |
| В2 | Embeddings L4: CF AI vs локальная vs OpenAI? | CF AI (бесплатно, единая модель) | совет |
| В3 | Merge L2+L4: простой vs weighted vs cascade? | Простой merge для MVP | совет |
| В4 | Подключение gateway: stdio vs SSE vs Hub? | stdio MCP (стандарт Claude Code) | совет |
| В5 | Knowledge Gateway — с какого тира? T3 или T4? | Продуктовое решение (не архитектор) | бизнес |
| В6 | Web App UI для управления sources? | CLI/config для MVP | совет |
| В7 | Community MCP: публикация Pack другим? | Зависит от ADR-018 | решение |
| В8 | Миграция knowledge-mcp — сразу или поэтапно? | Поэтапно (Ф1: L2 → Ф2: L4 + gateway) | решение |
| В9 | DS-Knowledge-Index + aist-bot-docs → L4? | Breaking change, нужен план | решение |

---

## Блок Г: ЮРИДИЧЕСКИЕ (параллельный трек, не архитектор)

> Результаты влияют на Б1 (ORY), Б8 (репликация), Г4 (хостинг).

| # | Вопрос | Блокирует |
|---|--------|-----------|
| Г1 | 152-ФЗ: что именно считается ПД? (telegram_id? данные обучения?) | Б1, Б8, Г4 |
| Г2 | Санкционный compliance (Stripe/Anthropic API — ограничения?) | Выбор провайдеров |
| Г3 | Два юрлица (РФ + международное) или одно? | WP-186 (юрготовность) |
| Г4 | Выбор РФ-хостинга (Hetzner Russia / VK Cloud / Selectel) | Б1, инфраструктура |

---

## Блок Д: СТРАТЕГИЧЕСКИЕ (не срочно)

| # | Вопрос | Связь |
|---|--------|-------|
| Д1 | B1-B8: детальные решения по тирам T1→T4 | [WP-74 §3](WP-74-platform-concept-of-use.md) |
| Д2 | Unit economics по тирам | Бизнес-модель |
| Д3 | 25 репо → масштабируемость | DevOps |
| Д4 | Платформа Андрея (Discourse): замена или обёртка? | Клуб |

---

## Порядок обсуждения (рекомендация)

| Встреча | Время | Блок А (решения) | Блок Б (согласование) |
|---------|-------|-------------------|----------------------|
| **1. Фундамент** | ~60 мин | А1 RLS, А2 Event Bus, А3 LMS | Б1 ORY self-hosted, Б2 Always-on, Б3 CRM proposal |
| **2. Web App + детали** | ~30 мин | А4 Vercel, А5 Access Mgmt | Б4-Б8 (быстрый проход) |
| **3. Knowledge Gateway** | ~30 мин | — | В1-В9 блоком |

---

<details>
<summary><b>Состояние документов в Inbox (ревью 28 мар)</b></summary>

### Активные документы

| Документ | Статус | Следующее действие |
|----------|--------|-------------------|
| [WP-73 — Архитектура](WP-73-aisystant-platform-architecture.md) | in_progress | Phase 2: спецификации модулей. Ждёт решения Блока А |
| [WP-74 — Концепция](WP-74-platform-concept-of-use.md) | in_progress | SC.101-116 формализованы. Обновляется параллельно с WP-73 |
| [WP-183 — CRM proposal](WP-183-crm-billing-architecture-proposal.md) | proposal v7 | Ждёт согласование архитектора (Б3) |
| [WP-183 — Research](WP-183-crm-billing-research-appendix.md) | приложение | Завершён. Привязан к proposal |
| [WP-109 — Activity Hub](WP-109-activity-hub-lms-integration-proposal.md) | approved | Реализация заблокирована на DE-35 |
| [WP-115 — Семинар](WP-115-seminar-payment-access-scenario.md) | draft | На обсуждение. Зависит от WP-183 |
| **Этот документ** (Повестка) | active | Обновлять по мере получения решений |

### Архив

- ~~[WP-168 — SurrealDB → Neon](../0.99.Archive/WP-168-surrealdb-to-neon-migration.md)~~ — архив (28 мар). Ф0-Ф1 done, Ф2-Ф3 ожидают доступы

### Кандидаты на архив (после завершения)

- **WP-183 Research appendix** — после принятия proposal → архив
- **WP-109** — после реализации Activity Hub → архив

</details>

---

*28 марта 2026. Консолидировано из: [WP-73 §5](WP-73-aisystant-platform-architecture.md), [WP-183 proposal](WP-183-crm-billing-architecture-proposal.md), [WP-73 §3.8](WP-73-aisystant-platform-architecture.md).*
