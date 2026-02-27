---
type: work-package
number: 73
title: "Новая архитектура и план развития ИТ-платформы Aisystant"
status: in_progress
budget: "10-15h (~5-7 сессий)"
created: 2026-02-26
deadline: W14
repo: DS-ecosystem-development
artifact: "Архитектурный план: as-is экосистема, to-be архитектура, roadmap миграции"
source: "WP-65 (IWE Web App) + WP-24 (ЦД) + стратегия платформы"
---

# РП #73: Новая архитектура и план развития ИТ-платформы Aisystant

## Контекст

Платформа Aisystant — ядро экосистемы развития интеллекта. Текущая архитектура: Discourse + LMS + Telegram-бот + ИИ-агенты. Назрела потребность в новой архитектуре с Web App как драйвером, цифровым двойником, биллингом, программой лояльности и ИИ-агентами.

**Зонтичный РП:** объединяет и координирует WP-65 (IWE Web App MVP), WP-24 (ЦД), и новые направления (биллинг, лояльность, ORY миграция).

---

## Концепция использования

> Роли, сценарии, тиры и UX-принципы вынесены в отдельный документ: **[WP-73a — Концепция использования ИТ-платформы Aisystant](WP-73a-platform-concept-of-use.md)**
>
> Содержание WP-73a:
> - 9 платформенных ролей (люди): Участник, Автор, Администратор, Бухгалтер, Маркетолог, Наставник, Тех.оператор, Амбассадор, Админ (владелец)
> - 10 ИИ-ролей (агенты): Проводник, Консультант, ДЗ-чекер, Стратег, Экстрактор, Оценщик, Статистик, Модератор, Публикатор, Командный координатор
> - 10 сценариев использования (SC-1 → SC-10, включая управление потоками и наставничество)
> - Тиры: T0 (бэк-офис), T1–T4 (учащиеся), TM1–TM3 (наставники), T5 (владелец)
> - UX «банковское приложение для развития» + дашборды по ролям
> - Сводные матрицы: сценарии × роли, сценарии × предметные области × системные уровни

---

## IntegrationGate

| # | Вопрос | Ответ |
|---|--------|-------|
| 1 | Тип | Система (platform) — новая архитектура всей платформы |
| 2 | Контур | L2 Platform (ядро) |
| 3 | Роли | Архитектор, Разработчик, Product Owner |
| 4 | Продукты | Архитектурный план, roadmap, спецификации модулей |
| 5 | Процессы | Архитектурное проектирование → миграция → развёртывание |

## Артефакт

Документ **«Архитектурный план Aisystant v2»** включает:
1. **As-is:** полная карта текущей платформы (все системы, репо, интеграции)
2. **To-be:** целевая архитектура (Web App + ЦД + биллинг + лояльность + ИИ-агенты)
3. **Gap-анализ:** что есть → что нужно → что мигрировать
4. **Roadmap:** фазы и приоритеты развития
5. **ADR:** ключевые архитектурные решения

## Связь с другими РП

| РП | Связь |
|----|-------|
| #65 | IWE Web App MVP — станет основным драйвером и первой реализацией |
| #24 | Цифровой двойник — ядро данных платформы |
| #5 | Бот: развитие — один из каналов (surface) |
| #40 | Экзокортекс шаблон — шаблон для пользователей |
| #63 | Терминология — единый язык платформы |

## Ключевые направления развития

### 1. Web App (драйвер)
- Каноническая поверхность IWE (RU + EN)
- «Банковское приложение для развития» (аналогия из WP-65)
- Дашборд + чат + ЦД + знания

### 2. Цифровой двойник
- 3-слойная архитектура (Events → State → Views) — DP.ARCH.003
- Neon DB (5 schemas: public/development/finance/connections/operations)
- MCP-интерфейс (digital-twin-mcp)

### 3. Биллинг и подписки
- Модель подписки (trial → paid)
- ORY для аутентификации (миграция с текущей)
- Платёжные интеграции

### 4. Программа лояльности
- Токены за активность (ДЗ, посты, вклад в экосистему)
- Статусы и привилегии
- Интеграция с биллингом

### 5. Разделение текстов и моделирования
- Руководства (тексты) — отдельно (Aisystant LMS / docs)
- Рабочая тетрадь (моделирование) — в Web App / боте
- Связь через программу обучения

### 6. ИИ-агенты
- 7 агентов монорепо DS-ai-systems
- Агенты работают на бэкенде → Web App показывает результаты
- Проводник, Стратег, Экстрактор и др.

## Текущая инфраструктура (as-is, для сбора)

### Системы платформы
- LMS Aisystant (aisystant repo)
- Discourse (systemsworld.club)
- Telegram-бот (@aist_me_bot)
- MCP-серверы (knowledge-mcp, digital-twin-mcp, guides-mcp, composer)
- ИИ-агенты (DS-ai-systems)
- Документация (docs → VitePress)
- SystemsSchool_bot (расписание, стажировки)

### Инфраструктура
- Railway (бот, бэкенд)
- Neon (PostgreSQL)
- Cloudflare
- Kubernetes (?)
- ORY (миграция в процессе?)

## Прогресс

### Phase 0: Сбор знаний (26 фев — эта сессия)
- [x] Инвентаризация всех репо и систем (22 активных репо)
- [x] Сбор всех текстов и обсуждений о платформе
- [x] Карта as-is (текущая архитектура)
- [x] Сбор идей и обсуждений (Web App, ЦД, биллинг, лояльность)

### Phase 1: Архитектурный план (26 фев)
- [x] To-be архитектура v2 (13 принципов, ASCII-диаграмма, 22 ключевых изменения)
- [x] ЭМОГССБ-оценка: **8.3/10** (проходит АрхГейт)
- [x] Gap-анализ: **31 подсистема** (13 создать, 11 доработать, 7 минимальный gap)
- [x] Roadmap: **4 фазы** (Фаза 0 → Фаза 3, март 2026 → 2027+)
- [x] ADR: **14 решений** (7 принятых, 7 предлагаемых)
- [x] ADR-014: Трёхосевая модель доступов + Позиции (DP.D.034) — Permission = Entitlement ∩ Role ∩ Scope; Позиции = бандлы назначения (ЭМОГССБ 8.7)
- [x] Роли и сервисы: 43 существующих + **17 новых** (S44-S60)
- [x] 10 сценариев использования (SC-1 → SC-10, вынесены в WP-73a)
- [x] Двух-юрисдикционная архитектура (P12): RU + World
- [x] UX «банковское приложение для развития»
- [x] 3 оси тиров: T0 (бэк-офис), T1–T4 (учащиеся), TM1–TM3 (наставники), T5 (владелец)
- [x] Роли: учащиеся, наставники, операторы (бухгалтер/CRM, админы) — вынесены в WP-73a
- [x] Панель наставника, CRM-панель, панель бэк-офиса — описаны в WP-73a §2
- [ ] **Согласование с архитектором:** Q1-Q14 (ожидание)
- [ ] **Юридическая консультация:** Q9, Q11, Q14 (ожидание)

### Phase 2: Спецификации модулей (следующий шаг)
- [ ] Спецификация Web App (обновить WP-65: двойной деплой, «банковский» UX)
- [ ] Спецификация Billing (новый WP: Stripe + YooKassa, feature gating, P12)
- [ ] Спецификация ЦД (обновить WP-24: Event Store + 5 проекций)
- [ ] Спецификация Loyalty / Proof-of-Impact (новый WP: токены, ESG)
- [ ] План миграции SurrealDB → Neon

---

## Собранные знания (Phase 0 — 26 фев)

> Source-of-truth: реальные файлы и код. Здесь — навигация + выжимки.

### 1. Реестр репозиториев платформы (22 активных)

**Source:** `DS-ecosystem-development/0.OPS/REPOSITORY-REGISTRY.md`

| # | Репо | Тип | Назначение |
|---|------|-----|-----------|
| 0 | ZP | Base/Принципы | Нулевые принципы (6 мета-ограничений) |
| 1 | FPF (ailev) | Base/Принципы | First Principles Framework |
| 2 | SPF | Base/Принципы | Second Principles Framework |
| 3 | FMT-S2R | Base/Форматы | Structured Second-level Repository |
| 14 | FMT-exocortex-template | Base/Форматы | Exocortex template (fork & deploy) |
| 4 | PACK-personal | Pack | Персональное развитие (224 entities) |
| 5 | PACK-ecosystem | Pack | Экосистема развития интеллекта |
| 6 | PACK-digital-platform | Pack | ИТ-платформа (213 entities, source-of-truth) |
| 20 | PACK-MIM | Pack | Мастерская (25 entities) |
| 24 | PACK-education | Pack | Методика обучения (43 entities) |
| 8 | DS-twin | DS/instrument | MCP-сервис ЦД (Cloudflare Workers) |
| 9 | DS-Knowledge-Index-Tseren | DS/instrument | Посты + публикации |
| 10 | DS-ecosystem-development | DS/governance | Координация экосистемы |
| 11 | DS-my-strategy | DS/governance | Личное стратегирование |
| 12 | docs (aisystant) | DS/surface | VitePress руководства (RU/EN) |
| 13 | DS-marathon-v2-tseren | DS/surface | Программа марафона |
| 15 | DS-ai-systems | DS/instrument | Монорепо 7 ИИ-систем |
| 18 | digital-twin-mcp | DS/instrument | MCP-сервер ЦД (Ory OAuth) |
| 19 | aist_bot_newarchitecture | DS/instrument | Telegram-бот (State Machine) |
| 21 | aisystant (external) | DS/instrument | LMS Aisystant (Java/Vaadin) |
| 22 | SystemsSchool_bot (external) | DS/instrument | TG-бот стажировок |
| — | DS-MCP | DS/instrument | knowledge-mcp + guides-mcp + composer |

### 2. Текущая архитектура (as-is)

**Source:** `DP.ARCH.001-platform-architecture.md`

#### 3-слойная архитектура

```
Layer 3: ИНТЕРФЕЙСЫ (thin clients)
  ├── Telegram Bot (@aist_me_bot)
  ├── Web LMS (aisystant.system-school.ru, Java/Vaadin)
  ├── Discourse (systemsworld.club)
  ├── Claude Code CLI (T4)
  └── [PLANNED] Web App (Next.js)

Layer 2: ОБРАБОТКА (два типа peer-to-peer)
  ├── Zone A: ИИ-системы (LLM, stateless)
  │   ├── Стратег (R1, Grade 3)
  │   ├── Экстрактор (R2, Grade 3)
  │   ├── Консультант (R3, Grade 2)
  │   ├── Проводник (R4, Grade 2)
  │   ├── Оценщик (R5, Grade 2)
  │   ├── Наладчик (R6, Grade 2)
  │   └── Статистик (R7, Grade 1)
  └── Zone B: Детерминированные (code, stateful, MCP)
      ├── Digital Twin (DS-twin, CF Workers, Ory OAuth)
      ├── Knowledge MCP (CF Workers, 5400+ docs, 9 sources)
      ├── Guides MCP (CF Workers, ~40 гайдов)
      ├── Composer MCP (бот-ассистент)
      ├── LMS Aisystant (Java, system-school.ru)
      ├── Billing [PLANNED]
      ├── ORY (identity, OAuth2) [MIGRATING]
      ├── CRM [PLANNED]
      └── Event Bus [PLANNED]

Layer 1: ДАННЫЕ + ИНФРАСТРУКТУРА
  ├── Neon PostgreSQL (pgvector, pg_trgm)
  ├── GitHub Repos (25+)
  ├── Railway (Python bot, EU Amsterdam)
  ├── Cloudflare Workers (MCP, global edge)
  └── Cache (Redis planned)
```

#### Топология деплоя (DP.D.030)

| Компонент | Провайдер | Регион | Стоимость |
|-----------|-----------|--------|-----------|
| Бот (Python, aiogram) | Railway | EU Amsterdam | $5/мес |
| MCP-серверы (TypeScript) | Cloudflare Workers | Global (auto) | Free tier |
| DB (PostgreSQL + pgvector) | Neon | EU Frankfurt | Free → $20/мес |
| Код + шаблон | GitHub | — | Free |
| Руководства (VitePress) | ? | ? | ? |

**Решение архитектора (19 фев):** Текущая связка верна. Позже Railway → Kubernetes.

#### Тиры обслуживания (DP.ARCH.002 → детали в [WP-73a §3](WP-73a-platform-concept-of-use.md))

> **Тиры = ось Entitlement** в трёхосевой модели доступов (ADR-014, P13). Тир определяет «что ДОСТУПНО», а не «что можно ДЕЛАТЬ» (это роль) и не «над чем» (это scope).

| Ось | Тиры | Для кого |
|-----|------|----------|
| **T0** | Бэк-офис / Администрирование | CRM-оператор, оператор потоков, администратор доступов, куратор |
| **T1–T4** | Старт → Изучение → Персонализация → Созидание | Учащиеся (траектория роста) |
| **TM1–TM3** | Стажёр → Наставник → Старший наставник | Наставники (дополнительно к T2+) |
| **T5** | Владелец платформы | Суперпозиция T0 + T4 + TM3 |

### 3. Архитектурные решения (уже принятые)

| # | Решение | Файл | Score |
|---|---------|------|-------|
| ADR-001 | **Multi-surface с Web-ядром (Next.js)** для международной аудитории | `01D-adr-web-ui-platform.md` | 69/80 |
| DP.ARCH.003 | **3-слойный ЦД:** Events → State → Views (Event Sourcing) | `DP.ARCH.003-digital-twin-architecture.md` | 52/60 (8.7) |
| DP.D.030 | **Топология:** Railway + CF Workers + Neon + GitHub → K8s | `DP.D.030-deployment-topology.md` | — |
| DP.D.031 | **MCP:** knowledge=публичный, digital-twin=приватный | `DP.D.031-mcp-access-model.md` | — |
| DP.D.033 | **Role-centric:** роль ≠ исполнитель | `DP.D.033-role-centric-architecture.md` | 50/60 |
| Архитектор-19фев | Railway→K8s, Event-driven sync, Grafana Cloud, Webhook | `architect-questions-2026-02-20.md` | — |

### 4. Цифровой двойник (DP.ARCH.003)

**Neon DB — 5 schemas (предложение для архитектора):**

| Schema | Назначение | Ключевые таблицы |
|--------|-----------|-----------------|
| `public` | User identity | users (canonical profile) |
| `development` | Growth: events + projections | user_events (append-only), skill_mastery (BKT), memory_decay (HLR), engagement, misconceptions, qualifications |
| `finance` | Billing, tokens, royalties | token_transactions, token_balances, subscriptions, payments, royalty_rules |
| `connections` | OAuth tokens, API keys | oauth_tokens (pgcrypto), api_keys, external_accounts |
| `operations` | FSM, cache, content, monitoring | fsm_states, content_cache, error_logs |

**Event Sourcing:** `user_events` таблица, 40+ типов событий, append-only, JSONB payload, confidence scores (0.0-1.0).

**5 проекций состояния:** skill_mastery (BKT), memory_decay (HLR), engagement, misconceptions, qualifications.

**MCP ЦД:** digital-twin-mcp (Cloudflare Workers), 3 инструмента: describe_by_path, read_digital_twin, write_digital_twin. **ORY OAuth2 уже интегрирован** (PKCE flow в worker-sse.js).

### 5. Биллинг и лояльность

**Source:** `DS-ecosystem-development/.../Описание системы биллинга 3.2.md`

**5 функций:**
1. Управление тарифами (freemium, subscription, pay-per-course, семейные/корпоративные)
2. Управление доступами (feature gating, quota, auto-отключение)
3. Программа лояльности (бонусы, реферальная, cashback, накопительные скидки)
4. Распределение доходов (Revenue Sharing: platform 30%, author 50%, instructor 15%, curator 5%)
5. Финансовая отчётность (MRR, ARR, LTV, CAC, churn)

**Каналы оплаты (P12 — две юрисдикции, единый биллинг):**
- **Россия 🇷🇺:** YooKassa, Paybox, TG Stars, system-school.ru (подписка БР + отдельные курсы)
- **Мир 🌍:** Stripe, PayPal, TG Stars
- **Единый Billing Service** с адаптерами по юрисдикции (Strategy pattern). Подписки, тарифы, токены — общие

**Токеновая экономика:**
- Зарабатываются за: slots (5-10), modules (20-50), posts (10-30), WP (20-100), помощь (10-50), проекты (50-500)
- Тратятся на: premium курсы (100-500), консультации (50-200), сертификация (100-300)

### 6. Разделение руководств и рабочей тетради

**Source:** `Описание платформы обучения 3.2.md` + `Структура репозитория руководств 0.9.md`

**Принципиальное разделение:**

| Компонент | Что | Доступ | Где |
|-----------|-----|--------|-----|
| **Тексты руководств** | Чтение теории, объяснения | ОТКРЫТЫЙ (в репо docs/, Memory Bank, MCP) | VitePress (docs), Knowledge MCP |
| **Рабочая тетрадь** | Кейсы, упражнения, моделирование | ПО ПОДПИСКЕ (premium feature) | LMS → Web App |
| **Интерактивный моделер** | Симуляции, визуализации концепций | ПО ПОДПИСКЕ | LMS → Web App |
| **ДЗ-чекер** | ИИ-проверка заданий | ПО ПОДПИСКЕ | Бот / Web App |

**Репозиторий руководств:**
- Иерархическая структура: P.G.S.SS.T (Программа.Руководство.Раздел.Подраздел.ТипОбъекта)
- Один подраздел = один файл (гранулярный MCP-доступ)
- YAML frontmatter, assets/ для картинок
- Типы: текст, таблицы, кейсы, вопросы, картинки
- Импорт из API (scripts/import_md/run.sh + metadata repo)

### 7. ORY (идентификация)

**Статус:** ORY OAuth2 уже интегрирован в digital-twin-mcp (worker-sse.js):
- PKCE flow: `/authorize` → Ory `/oauth2/auth` → callback → token exchange
- ORY_PROJECT_URL, ORY_CLIENT_ID, ORY_CLIENT_SECRET в env
- ID token декодирование, refresh tokens хранятся в KV
- **Открытый вопрос архитектора:** хранение ORY за границей + репликация (с Пашей)

**LMS Aisystant (Java):** Текущая авторизация через `aisystant.system-school.ru` (email + пароль), TG-привязка. Миграция на ORY — необходима для единого SSO.

### 8. Открытые вопросы (из обсуждения с архитектором, 19 фев)

| # | Вопрос | Статус |
|---|--------|--------|
| B1-B8 | Детальные решения по тирам T1→T4 | **Открыт** |
| C5 | Изоляция данных (RLS vs schema vs DB) | **Открыт** |
| — | ORY за границей + репликация | **Открыт** (Андрей + Паша) |
| — | Платформа Андрея (Discourse) | **Открыт** |
| — | Конфигурация агентов (что может/не может) | **Открыт** |
| C4 | Unit economics по тирам | **Открыт** |
| C6 | 25 репо → масштабируемость | **Открыт** |

### 9. Посты и публикации о платформе

| Дата | Пост | Тема |
|------|------|------|
| 2026-02-25 | Выбор интерфейсной платформы IWE (5 вариантов) | ADR-001, Next.js winner |
| 2026-02-19 | Пять конфигураций IWE | Варианты настройки |
| 2026-02-17 | Harness engineering — IWE | Упряжь для интеллекта |
| 2026-02-10 | Архитектура платформы: 3 слоя | Популярное изложение DP.ARCH.001 |
| 2026-02-10 | Как устроена система | Механика экзокортекса |
| 2026-02-18 | Не личный экзокортекс | Public vs personal |
| 2026-02-16 | Агенты заработали автономно: W08 | Отчёт по работе агентов |

### 10. Техстек ключевых систем (из кода)

| Система | Язык | Фреймворк | DB | Deploy | Auth |
|---------|------|-----------|----|--------|------|
| **Aisystant LMS** | Java 8 + Groovy | Vaadin 8, Spring Data JPA, Hibernate | PostgreSQL + Solr 8.5 | WAR (Nomad?) | **Ory Network** + legacy Keycloak |
| **Aist Bot** | Python 3.11 | aiogram 3.20, asyncpg | Neon PostgreSQL | Railway (Docker) | TG auth, GitHub OAuth |
| **SystemsSchool Bot** | Python 3.13 | python-telegram-bot 22.0 | Нет (API calls) | **Vultr K8s** (Werf/Helm) | Aisystant API |
| **knowledge-mcp** | TypeScript | CF Workers | Neon + pgvector | Cloudflare Workers | Public |
| **digital-twin-mcp** | JavaScript | CF Workers | Neon + CF KV | Cloudflare Workers | **Ory OAuth2 (PKCE)** |
| **guides-mcp** | TypeScript | CF Workers | **SurrealDB** ⚠️ | Cloudflare Workers | — |
| **fsm-mcp** | TypeScript | CF Workers | — | Cloudflare Workers | — |
| **docs** | Node.js | VitePress | SurrealDB (publish) ⚠️ | VK Cloud VM + Nomad | — |

> ⚠️ **SurrealDB — скорее всего, отказ.** Guides-mcp и docs publishing pipeline используют SurrealDB. При миграции на новую архитектуру заменить на Neon PostgreSQL (единая БД экосистемы).

**Платёжные системы в LMS:** Stripe, YooKassa, Paybox, Ecwid, Tilda (все webhook). TG Stars — в боте.

**Ory Network:** Проект `thirsty-goldstine-5xjpbvdi2b.projects.oryapis.com`. Используется в LMS и digital-twin-mcp. Keycloak — legacy (только тесты).

### 11. Карта ИТ-систем (17 подсистем из DS-ecosystem-development)

1. **Цифровой двойник** (DS-twin, digital-twin-mcp)
2. **LMS и обучение** (aisystant, system-school.ru)
3. **Клуб** (Discourse, systemsworld.club)
4. **CRM** [PLANNED]
5. **Биллинг и оплата** [PLANNED]
6. **Централизованное хранилище** (Memory Bank / Knowledge MCP)
7. **Хаб активностей** (Activity Hub) [PLANNED]
8. **Проводник** (Route Guide AI) [PLANNED]
9. **Apps SDK и маркетплейс** [PLANNED]
10. **ORY** (Identity & Access) [MIGRATING]
11. **Proof-of-Impact** (токены) [PLANNED]
12. **Эпистемический граф** [PLANNED]
13. **Бот Aist** (aist_bot_newarchitecture)
14. **SystemsSchool_bot** (стажировки)
15. **MCP-серверы** (knowledge, guides, twin, composer)
16. **ИИ-агенты** (DS-ai-systems, 7 систем)
17. **Публикатор** (club publishing pipeline)

---

## Phase 1: Целевая архитектура (To-be)

> Sources: DP.ARCH.001 (3-layer), DP.ARCH.002 (tiers), DP.ARCH.003 (ЦД), ADR-001 (multi-surface), DP.D.030 (deploy), DP.D.031 (MCP access), DP.D.033 (role-centric), DP.IWE.001 (IWE concept), DP.MAP.002 (43 services), SC-1…SC-9 (сценарии).

### Архитектурные принципы (из DP.ARCH.001 + дополнения)

| # | Принцип | Суть |
|---|---------|------|
| P1 | **Interfaces never access data directly** | Всегда через Layer 2 (Processing) |
| P2 | **AI-системы UI-agnostic** | Не знают, какой интерфейс используется |
| P3 | **Evolvability-first** | При выборе между простотой сейчас и расширяемостью — расширяемость |
| P4 | **Alienability** (отчуждаемость) | Platform-space vs User-space. Персонализация через user-space конфигурацию |
| P5 | **Role ≠ Executor** (DP.D.033) | Роли описываются отдельно от исполнителей. Замена исполнителя не ломает описание |
| P6 | **Knowledge ≠ User Data** (DP.D.031) | Знания — публичные. Данные пользователя — приватные. Чёткая граница |
| P7 | **Event Sourcing для ЦД** (DP.ARCH.003) | Каждое действие = immutable event. Состояние = проекция из событий |
| P8 | **Multi-surface** (ADR-001) | Web App = каноническая поверхность. Бот, CLI, ChatGPT = адаптеры |
| P9 | **Единая БД** | Neon PostgreSQL (pgvector). Отказ от SurrealDB. Одна СУБД на всё |
| P10 | **Команды = люди + ИИ-агенты** (SC-8) | ИИ-агенты — полноценные участники команд |
| P11 | **IPO** (Input → Processing → Output) | Каждый компонент описывается через IPO паттерн |
| P12 | **Единое сообщество, две юрисдикции** | Сообщество — одно на весь мир. Активность, токены, репутация — общие. Юридические границы — только те, что требует закон (152-ФЗ, санкции, платёжные ограничения). Никаких искусственных разделений |
| P13 | **Permission = Entitlement ∩ Role ∩ Scope** (ADR-014, DP.D.034) | Три оси + Позиции (именованные бандлы). Назначение одним действием. «Админ-1 vs Админ-2» = одна роль, разный scope |

### Целевая архитектура v2

```
╔══════════════════════════════════════════════════════════════════════════╗
║                        Layer 3: ИНТЕРФЕЙСЫ                              ║
║                     (thin clients, UI-agnostic)                         ║
╠══════════════════════════════════════════════════════════════════════════╣
║                                                                          ║
║  ┌──────────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌────────┐║
║  │  ★ Web App   │  │ TG Bot   │  │ Claude   │  │ Discord  │  │ ChatGPT│║
║  │  (Next.js)   │  │ @aist_me │  │ Code CLI │  │ (Teams)  │  │  Apps  │║
║  │  Canonical   │  │ Fast ch. │  │ T4/T5    │  │ SC-8     │  │ Agents │║
║  └──────┬───────┘  └────┬─────┘  └────┬─────┘  └────┬─────┘  └───┬────┘║
║         │               │             │             │             │      ║
╠═════════╪═══════════════╪═════════════╪═════════════╪═════════════╪══════╣
║         └───────────────┴─────────────┴─────────────┴─────────────┘      ║
║                                    │                                     ║
║                          ┌─────────▼─────────┐                           ║
║                          │    API Gateway     │                           ║
║                          │  (ORY SSO + RBAC)  │                           ║
║                          └─────────┬─────────┘                           ║
║                                    │                                     ║
╠════════════════════════════════════╪══════════════════════════════════════╣
║                        Layer 2: ОБРАБОТКА                                ║
║                                    │                                     ║
║  ┌─────────────────────────────────┼────────────────────────────────┐    ║
║  │              Zone A: ИИ-системы (stateless, LLM)                │    ║
║  │                                 │                                │    ║
║  │  ┌──────────┐ ┌──────────┐ ┌───┴──────┐ ┌──────────┐           │    ║
║  │  │Стратег R1│ │Экстрактор│ │Проводник │ │Консультант│          │    ║
║  │  │ Grade 3  │ │  R2 Gr3  │ │  R4 Gr2  │ │  R3 Gr2  │          │    ║
║  │  └──────────┘ └──────────┘ └──────────┘ └──────────┘           │    ║
║  │  ┌──────────┐ ┌──────────┐ ┌──────────┐                        │    ║
║  │  │Оценщик R5│ │Наладчик  │ │Статистик │                        │    ║
║  │  │  Grade 2 │ │ R6 Gr2   │ │ R10 Gr1  │                        │    ║
║  │  └──────────┘ └──────────┘ └──────────┘                        │    ║
║  └──────────────────────────────────────────────────────────────────┘    ║
║                                    │                                     ║
║  ┌─────────────────────────────────┼────────────────────────────────┐    ║
║  │         Zone B: Детерминированные (stateful, MCP, code)         │    ║
║  │                                 │                                │    ║
║  │  ── Данные и знания ──                                          │    ║
║  │  ┌─────────────┐  ┌──────────────┐  ┌──────────────┐           │    ║
║  │  │★ Digital    │  │★ Knowledge   │  │  Guides MCP  │           │    ║
║  │  │  Twin MCP   │  │   MCP        │  │  (→ Neon PG) │           │    ║
║  │  │ (private)   │  │  (public)    │  │  (public)    │           │    ║
║  │  └─────────────┘  └──────────────┘  └──────────────┘           │    ║
║  │  ┌─────────────┐  ┌──────────────┐                              │    ║
║  │  │★ Epistemic  │  │★ Unified     │                              │    ║
║  │  │  Graph (ESG)│  │  Search      │                              │    ║
║  │  │ (Proof-of-I)│  │ (cross-sys)  │                              │    ║
║  │  └─────────────┘  └──────────────┘                              │    ║
║  │                                                                  │    ║
║  │  ── Экономика и идентичность ──                                 │    ║
║  │  ┌─────────────┐  ┌──────────────┐  ┌──────────────┐           │    ║
║  │  │★ Billing &  │  │★ Loyalty /   │  │  ORY         │           │    ║
║  │  │  Payments   │  │  Proof-of-   │  │  (Identity)  │           │    ║
║  │  │  (Stripe+TG)│  │  Impact      │  │  SSO         │           │    ║
║  │  └─────────────┘  └──────────────┘  └──────────────┘           │    ║
║  │  ┌─────────────┐  ┌──────────────┐                              │    ║
║  │  │★ Certific-  │  │★ Revenue     │                              │    ║
║  │  │  ation Svc  │  │  Sharing     │                              │    ║
║  │  │ (diplomas)  │  │ (royalties)  │                              │    ║
║  │  └─────────────┘  └──────────────┘                              │    ║
║  │                                                                  │    ║
║  │  ── Обучение и контент ──                                       │    ║
║  │  ┌─────────────┐  ┌──────────────┐  ┌──────────────┐           │    ║
║  │  │  LMS        │  │★ Workbook /  │  │★ ДЗ-чекер   │           │    ║
║  │  │  Aisystant  │  │  Моделер     │  │  (AI HW     │           │    ║
║  │  │  (legacy→API│  │ (exercises)  │  │   Checker)  │           │    ║
║  │  └─────────────┘  └──────────────┘  └──────────────┘           │    ║
║  │  ┌─────────────┐  ┌──────────────┐  ┌──────────────┐           │    ║
║  │  │★ Personal   │  │★ Seminar /   │  │★ Mentor      │           │    ║
║  │  │  Guide Gen  │  │  Webinar Svc │  │  Panel /     │           │    ║
║  │  │  (WP-58)    │  │ (live events)│  │  Streams Mgmt│           │    ║
║  │  └─────────────┘  └──────────────┘  └──────────────┘           │    ║
║  │                                                                  │    ║
║  │  ── Оркестрация и взаимодействие ──                             │    ║
║  │  ┌─────────────┐  ┌──────────────┐  ┌──────────────┐           │    ║
║  │  │★ CRM /      │  │★ Activity    │  │★ Event Bus   │           │    ║
║  │  │  Onboarding │  │   Hub        │  │  (Orchestr.) │           │    ║
║  │  └─────────────┘  └──────────────┘  └──────────────┘           │    ║
║  │  ┌─────────────┐  ┌──────────────┐  ┌──────────────┐           │    ║
║  │  │★ Notific-   │  │★ Team        │  │  Composer    │           │    ║
║  │  │  ation Svc  │  │  Service     │  │  MCP (FSM)   │           │    ║
║  │  │(push/email) │  │  (SC-8)      │  │              │           │    ║
║  │  └─────────────┘  └──────────────┘  └──────────────┘           │    ║
║  └──────────────────────────────────────────────────────────────────┘    ║
║                                    │                                     ║
╠════════════════════════════════════╪══════════════════════════════════════╣
║                   Layer 1: ДАННЫЕ + ИНФРАСТРУКТУРА                       ║
║                                    │                                     ║
║  ┌──────────────┐  ┌──────────────┐│ ┌──────────────┐  ┌──────────────┐ ║
║  │★ Neon PG     │  │  GitHub      ││ │  Vercel /    │  │  Cloudflare  │ ║
║  │ (pgvector,   │  │  Repos (25+) ││ │  Railway     │  │  Workers     │ ║
║  │  RLS, Event  │  │              ││ │  → K8s       │  │  (MCP edge)  │ ║
║  │  Store)      │  │              ││ │              │  │              │ ║
║  └──────────────┘  └──────────────┘│ └──────────────┘  └──────────────┘ ║
║  ┌──────────────┐  ┌──────────────┐│ ┌──────────────┐                   ║
║  │  ORY Network │  │  Redis /     ││ │  Monitoring  │                   ║
║  │  (hosted)    │  │  CF KV       ││ │  (Grafana)   │                   ║
║  │              │  │  (cache)     ││ │              │                   ║
║  └──────────────┘  └──────────────┘│ └──────────────┘                   ║
╚══════════════════════════════════════════════════════════════════════════╝

★ = новый или существенно переработанный компонент
```

### Ключевые изменения As-is → To-be

| # | Изменение | Обоснование |
|---|-----------|-------------|
| 1 | **Web App (Next.js)** как каноническая поверхность | ADR-001: международная аудитория, rich UI, PWA, «банковское приложение для развития» |
| 2 | **API Gateway + ORY SSO** | Единая точка входа для всех интерфейсов. SSO через ORY для Web App, бот, CLI |
| 3 | **SurrealDB → Neon** | Принцип P9: единая СУБД. Guides-mcp и docs publishing мигрируют на Neon |
| 4 | **Billing & Payments** | Новый сервис: Stripe (web) + TG Stars (бот) + LMS programs. Feature gating, подписки |
| 5 | **Loyalty / Proof-of-Impact** | Токеновая экономика. Начисление за вклад, epistemic status, vesting |
| 6 | **CRM / Onboarding** | Персональная воронка: SC-1 (онбординг) + конверсия T1→T5 |
| 7 | **Activity Hub** | Единый поток событий: обучение, проекты, сообщество, токены. Source для ЦД |
| 8 | **Event Bus / Orchestration** | Loose coupling. Шире чем шина: оркестрация workflows, sagas, retries |
| 9 | **Team Service** (SC-8) | Формирование команд: подбор по ЦД, каналы (Discord), ИИ-агенты как участники |
| 10 | **Discord** как дополнительная поверхность | SC-8: реал-тайм командная работа, голосовые чаты, ИИ-агенты в каналах |
| 11 | **LMS Aisystant → API** | Legacy LMS обёртывается API-слоем для интеграции с Web App (не переписывается целиком) |
| 12 | **Railway → Kubernetes** | Долгосрочная миграция. Сначала Web App на Vercel, бот на Railway, потом всё в K8s |
| 13 | **Monitoring (Grafana Cloud)** | Решение архитектора 19 фев. Centralized observability |
| 14 | **RLS в Neon** | Предпочтительный вариант изоляции данных (DP.D.031, вопрос C5). Одна БД, фильтрация по user_id |
| 15 | **Notification Service** | Push/email/in-app. Критичен для UX «банковского приложения» — ежедневная привычка |
| 16 | **ДЗ-чекер → сервис** | Выделить из LMS в отдельный ИИ-сервис, доступный через Web App и бот |
| 17 | **Рабочая тетрадь / Моделер → Web App** | Из LMS в Web App: интерактивные упражнения, кейсы, симуляции |
| 18 | **Эпистемический граф (ESG)** | Граф знаний/компетенций экосистемы. Зависимость для Proof-of-Impact, сертификации |
| 19 | **Unified Search** | Кросс-системный поиск: знания + руководства + ЦД + посты + кейсы |
| 20 | **Certification System** | Цифровые сертификаты, верификация, привязка к ЦД и ESG |
| 21 | **Revenue Sharing** | Автоматическое распределение: platform 30%, author 50%, instructor 15%, curator 5% |
| 22 | **Генератор персонального руководства** (WP-58) | ИИ-генерация маршрута из ЦД + целей + контекста |

### Двух-юрисдикционная архитектура (P12)

> **Принцип:** Одно сообщество. Две юрисдикции. Раздельные сайты и железо — всё остальное общее.

Экосистема работает в двух правовых пространствах: **Россия** (152-ФЗ, санкционные ограничения, блокировки сервисов) и **мир** (GDPR, международные платёжные системы, свободный доступ к сервисам). При этом сообщество **едино**: участник из России и участник из Берлина видят друг друга, обмениваются знаниями, работают в одних командах, имеют общие токены и репутацию.

#### Что РАЗДЕЛЕНО (сайты + железо)

| Компонент | Россия | Мир | Причина |
|-----------|--------|-----|---------|
| **Web App (сайт)** | `ru.aisystant.com` (или аналог) — хостинг в РФ | `aisystant.com` — Vercel / EU | Блокировки, латентность, 152-ФЗ |
| **Серверы (железо)** | Hetzner Russia / VK Cloud / Selectel | Railway EU → K8s EU | 152-ФЗ, доступность из РФ |
| **Платежи** | YooKassa, Paybox, TG Stars | Stripe, PayPal, TG Stars | Stripe/PayPal не работают в РФ |
| **PII (персональные данные)** | Хранение ПД граждан РФ в РФ (152-ФЗ ст.18) | Neon EU Frankfurt (GDPR) | 152-ФЗ требует локализации |

#### Что ОБЩЕЕ (единое, без разделений)

| Компонент | Реализация |
|-----------|-----------|
| **Сообщество** | Единый Discourse (systemsworld.club), единый Discord, единые команды (SC-8) |
| **Токены и репутация** | Один токеновый движок, один эпистемический статус. Нет «российских» и «международных» токенов |
| **Цифровой двойник** | Единая модель ЦД, общие проекции, общие данные прогресса |
| **Знания и руководства** | Единый Knowledge MCP, единые руководства (RU + EN), общий контент |
| **ИИ-агенты** | Одни и те же агенты для всех участников |
| **Activity Hub** | Общий поток активности, общая статистика |
| **Учётная запись** | Единый ORY SSO, один аккаунт на весь мир |
| **Billing логика** | Единые подписки, тарифы, feature gating. Различаются только платёжные адаптеры |
| **Обучение** | Единые программы, единые ДЗ, единый ДЗ-чекер, единая сертификация |

#### Архитектура: два фронтенда, единый бэкенд

```
                         ПОЛЬЗОВАТЕЛИ
                    RU Россия    World Мир
                        |           |
               +--------v--+  +-----v--------+
               |  Web App  |  |   Web App     |
               |  RU site  |  |  World site   |
               | (РФ хост) |  |  (Vercel EU)  |
               +--------+--+  +-----+---------+
                        |           |
                        +-----+-----+
                              |
               +--------------v--------------+
               |       API Gateway           |
               |     (ORY SSO + RBAC)        |
               |  Routing по юрисдикции      |
               +--------------+--------------+
                              |
    +-------------------------+-------------------------+
    |         ЕДИНЫЙ ЛОГИЧЕСКИЙ СЛОЙ (бэкенд)           |
    |                                                     |
    |  Community . Tokens . DT . Knowledge . AI agents    |
    |  Activity Hub . CRM . Certification . Search        |
    |  Event Bus . Notification . Team Service            |
    +-------------------------+---------------------------+
    |  Billing Adapter: RU    |  Billing Adapter: World   |
    |  YooKassa, Paybox, TGS  |  Stripe, PayPal, TGS     |
    +-------------------------+---------------------------+
    |    DB + PII: RU node    |    DB + PII: EU node      |
    |  (Hetzner RU / VK Cloud)|  (Neon EU Frankfurt)      |
    +-------------------------+---------------------------+
```

**Ключевое:** Два фронтенда — один код (Next.js), разный деплой. API Gateway определяет юрисдикцию по аккаунту и маршрутизирует к нужному платёжному адаптеру и PII-хранилищу. Вся бизнес-логика, знания, токены, сообщество — общие.

**Billing:** Единый Billing Service с адаптерами (Strategy pattern). Пользователь привязывается к юрисдикции по стране регистрации. Внутри — единые подписки, единые тарифы, единые токены. Различаются только каналы оплаты.

**Данные — две ноды, один логический слой:**
- **РФ-нода:** PostgreSQL в российском ЦОД — ПД граждан РФ (ФИО, email, телефон, адрес) + реплика операционных данных для низкой латентности
- **EU-нода:** Neon EU Frankfurt — ПД международных пользователей + мастер-данные (знания, контент, токены)
- **Синхронизация:** Event Bus обеспечивает eventual consistency между нодами. Общие данные (токены, активность, знания) реплицируются в обе стороны
- Нужна юридическая консультация по точному разграничению

**ORY:** Единый ORY. Если доступ из РФ заблокирован — self-hosted ORY на РФ-ноде с федерацией к основному.

#### Открытые вопросы P12

| # | Вопрос | Контекст |
|---|--------|----------|
| Q9 | 152-ФЗ: точный scope локализации ПД | Какие данные обязательно в РФ? Только ФИО+email или шире? Юр. консультация |
| Q10 | Единый тариф в разных валютах? | RUB / USD / EUR — один тариф с конвертацией или региональные цены? |
| Q11 | Sanction compliance | Нужна ли автоматическая проверка санкционных списков? |
| Q12 | Выбор РФ-хостинга | Hetzner Russia vs VK Cloud vs Selectel — для Web App + DB + PII |
| Q13 | Репликация данных RU↔EU | Какие данные реплицировать? Eventual consistency vs strong? |
| Q14 | Два юрлица или одно? | РФ-юрлицо + международное? Влияет на 152-ФЗ, договоры, оплату |

### Роли и сервисы в To-be (на основе DP.MAP.002)

Из 43 текущих сервисов **все сохраняются**. Добавляются новые:

| # | Новый сервис | Роль | Триггер | Исполнитель |
|---|-------------|------|---------|-------------|
| S44 | Team Matching | Проводник (R4) | On-demand | Web App + AI |
| S45 | Billing Check | Billing Service | Event (subscription change) | Deterministic |
| S46 | Token Mint | Loyalty Service | Event (confirmed action) | Deterministic |
| S47 | Onboarding Flow | CRM | Event (new registration) | Web App |
| S48 | Guide Import | Publisher (R21) | Scheduled | Neon (replaces SurrealDB) |
| S49 | Activity Feed | Activity Hub | Event (any user action) | Deterministic |
| S50 | Team Channel Setup | Team Service | Event (team formed) | Discord API |
| S51 | Send Notification | Notification Svc | Event (ЦД insight, deadline, streak) | Push/email/in-app |
| S52 | Check Homework | ДЗ-чекер | On-demand (student submit) | AI + Web App |
| S53 | Issue Certificate | Certification Svc | Event (course completed + ESG verified) | Deterministic |
| S54 | Generate Personal Guide | Guide Generator | On-demand (user request) | AI + ЦД + Knowledge |
| S55 | Cross-system Search | Unified Search | On-demand | Neon pgvector + FTS |
| S56 | ESG Update | Epistemic Graph | Event (new evidence: cert, peer review, WP) | Deterministic + AI |
| S57 | Revenue Split | Revenue Sharing | Event (payment received) | Deterministic |
| S58 | Manage Stream | Stream Mgmt (T0) | On-demand (admin creates stream) | Web App (admin panel) |
| S59 | Grade Homework | Mentor Panel (TM) | On-demand (mentor reviews) | Web App (mentor panel) |
| S60 | CRM Dashboard | CRM/Бэк-офис (T0) | On-demand (bookkeeper views) | Web App (back-office panel) |

---

## Phase 1: Gap-анализ

### Подсистемы: As-is → To-be

| # | Подсистема | As-is | To-be | Gap | Приоритет |
|---|-----------|-------|-------|-----|-----------|
| 1 | **Web App** | ❌ Не существует | Next.js + Vercel/Railway, каноническая поверхность | 🔴 Создать с нуля | **P0** |
| 2 | **ORY SSO** | 🟡 Частично (digital-twin-mcp PKCE, LMS legacy) | Единый SSO для всех поверхностей + RBAC | 🟡 Интеграция Web App + миграция LMS | **P0** |
| 3 | **Цифровой двойник** | 🟡 MCP работает, Event Sourcing спроектирован (DP.ARCH.003), схемы в Neon | Полный 3-слойный ЦД: Events → State → Views, 5 проекций | 🟡 Реализовать Event Store + проекции (WP-24 Phase 1-3) | **P1** |
| 4 | **Billing** | 🟡 TG Stars в боте, LMS programs на system-school.ru | Единый Billing: Stripe + TG Stars + подписки + feature gating | 🔴 Создать Billing Service, интегрировать с ORY и Web App | **P1** |
| 5 | **Knowledge MCP** | ✅ Работает (5400+ docs, 9 sources, pgvector) | Без изменений. Добавить индексацию новых sources | 🟢 Минимальный gap | P3 |
| 6 | **Guides MCP** | 🟡 Работает, но на SurrealDB | Миграция на Neon PostgreSQL | 🟡 Миграция БД | **P1** |
| 7 | **Composer MCP (FSM)** | ✅ Работает (бот-ассистент) | Без существенных изменений | 🟢 Минимальный gap | P3 |
| 8 | **TG Bot** | ✅ Работает (prod + pilot, T1-T3) | Сохраняется как fast channel. Добавить deeplink на Web App | 🟢 Минимальный gap | P2 |
| 9 | **Claude Code IWE** | ✅ Работает (T4-T5, экзокортекс) | Без изменений. Шаблон (WP-40) продолжает развитие | 🟢 Минимальный gap | P3 |
| 10 | **LMS Aisystant** | ✅ Java 8 монолит, Vaadin 8, legacy | Обернуть API-слоем для Web App. Рабочая тетрадь → Web App. Долгосрочно: замена или декомпозиция | 🟡 API-слой, интеграция с ORY | **P2** |
| 11 | **Discourse (Клуб)** | ✅ Работает (systemsworld.club) | Сохраняется для community. Интеграция с Web App (SSO, deeplinks) | 🟢 SSO интеграция | P2 |
| 12 | **CRM / Бэк-офис (T0)** | ❌ Не существует | CRM (контакты, воронка, подписки, MRR/churn/LTV) + панель бэк-офиса для бухгалтера/CRM-оператора + онбординг (SC-1). Revenue Sharing отчётность | 🔴 Создать | **P2** |
| 13 | **Loyalty / Proof-of-Impact** | ❌ Не существует (токены описаны, но не реализованы) | Токеновый движок: начисление, vesting, epistemic status, баланс | 🔴 Создать | **P2** |
| 14 | **Activity Hub** | ❌ Не существует | Агрегатор событий из всех систем → ЦД, токены, статистика | 🔴 Создать | **P2** |
| 15 | **Event Bus** | ❌ Не существует (синхронные вызовы) | Async event-driven интеграция между подсистемами | 🔴 Создать | **P1** |
| 16 | **Team Service** | ❌ Не существует | Формирование команд, канальная интеграция (Discord), ИИ-агенты | 🔴 Создать | **P3** |
| 17 | **Discord** | ❌ Не используется | Поверхность для команд (SC-8): каналы, voice, боты-агенты | 🔴 Интеграция | **P3** |
| 18 | **ИИ-агенты (11+ ролей)** | ✅ 7 систем в DS-ai-systems: Стратег (R1, Grade 3), Экстрактор (R2, Gr3), Консультант (R3, Gr2), Проводник (R4, Gr2), Оценщик (R5, Gr2), Наладчик (R6, Gr2), Статистик (R10, Gr1). **ИИ-ассистенты:** Ассистент Ученика (composer-mcp), ZP-тренер (WP-57), Персональный гид (WP-58), ДЗ-чекер, Модератор клуба, Публикатор (R21) | Расширить: командные агенты (SC-8), интеграция с Web App (agent activity feed), API для structured output, approve/reject. Новые роли: Командный координатор, Вебинар-ассистент | 🟡 API для Web App, новые роли, агентная оркестрация | P2 |
| 19 | **Docs (VitePress)** | ✅ Работает, SurrealDB для publish | Миграция publish на Neon. Интеграция с Web App (SSO, deeplinks) | 🟡 Миграция SurrealDB, SSO | **P1** |
| 20 | **Monitoring** | 🟡 Минимальный (error_logs в Neon) | Grafana Cloud: метрики, логи, алерты | 🟡 Настроить Grafana | P2 |
| 21 | **Notification Service** | ❌ Не существует | Push/email/in-app уведомления, персональные nudges из ЦД. Критичен для «банковского приложения» | 🔴 Создать | **P1** |
| 22 | **ДЗ-чекер (AI HW Checker)** | 🟡 Существует в LMS (Java), частично через бота | Единый ДЗ-чекер: Web App + бот + LMS. ИИ-проверка с обратной связью | 🟡 Вынести в отдельный сервис, интегрировать с Web App | **P1** |
| 23 | **Certification System** | 🟡 Частично в LMS (сертификаты PDF) | Сертификация через Web App: цифровые сертификаты, верификация, epistemic status | 🟡 Расширить, интегрировать с ЦД и Web App | **P2** |
| 24 | **Рабочая тетрадь / Моделер** | 🟡 Существует в LMS (кейсы, упражнения) | Интерактивная рабочая тетрадь в Web App: кейсы, моделирование, симуляции | 🟡 Перенести из LMS в Web App, добавить интерактивность | **P1** |
| 25 | **Генератор персонального руководства** | ❌ Не существует (WP-58, pending) | ИИ-генерация персонального руководства на основе ЦД, целей и контекста | 🔴 Создать | **P2** |
| 26 | **Эпистемический граф (ESG)** | ❌ Не существует (описан, не реализован) | Граф знаний и компетенций экосистемы. Критическая зависимость для Proof-of-Impact и сертификации | 🔴 Создать | **P2** |
| 27 | **Unified Search** | ❌ Не существует | Кросс-системный поиск: руководства + знания + ЦД + посты + кейсы | 🔴 Создать | **P2** |
| 28 | **Семинары / Вебинары** | 🟡 Внешние инструменты (Zoom, Google Meet), без платформенной интеграции | Интеграция live-событий с платформой: расписание, запись, ДЗ, токены за участие | 🟡 Создать интеграционный слой | **P3** |
| 29 | **Apps SDK & Маркетплейс** | ❌ Не существует (описан в экосистеме) | SDK для сторонних приложений + маркетплейс (Global Core + Local Edge) | 🔴 Создать | **P3** |
| 30 | **Revenue Sharing** | ❌ Не существует (формула описана: platform 30%, author 50%, instructor 15%, curator 5%) | Автоматическое распределение доходов по формуле | 🔴 Создать | **P3** |
| 31 | **Панель наставника / Управление потоками** | ❌ Не существует (потоки управляются вручную) | Панель наставника (табель, очередь ДЗ, аналитика группы, коммуникация). Управление потоками (создание, расписание, назначение наставников). SC-10, TM1–TM3 | 🔴 Создать | **P1** |

### Сводка Gap

| Тип gap | Количество | Подсистемы |
|---------|-----------|-----------|
| 🔴 Создать с нуля | 13 | Web App, Billing, CRM/Бэк-офис (T0), Loyalty, Activity Hub, Event Bus, Team Service, Notification Svc, Personal Guide Gen, ESG, Unified Search, Apps SDK, Revenue Sharing, Панель наставника/Потоки |
| 🟡 Доработать | 11 | ORY SSO, ЦД, Guides MCP, LMS API, Docs, ИИ-агенты, Monitoring, ДЗ-чекер, Certification, Рабочая тетрадь, Семинары |
| 🟢 Минимальный gap | 7 | Knowledge MCP, Composer MCP, TG Bot, Claude Code, Discourse, SystemsSchool Bot |

---

## Phase 1: Roadmap

### Фаза 0: Фундамент (март–апрель 2026, ~8 недель)

**Цель:** Web App MVP + ORY SSO + Event Bus skeleton

| # | Задача | Зависимости | Бюджет | Результат |
|---|--------|-------------|--------|-----------|
| 0.1 | **Web App scaffold** (Next.js, NextAuth + ORY, i18n, deploy на Vercel) | — | 20-30h | Рабочий каркас с авторизацией |
| 0.2 | **ORY SSO интеграция** для Web App | 0.1 | 10-15h | Единый вход: Web App + бот + digital-twin-mcp |
| 0.3 | **Guides MCP → Neon** миграция | — | 5-8h | Отказ от SurrealDB |
| 0.4 | **Docs publish → Neon** миграция | 0.3 | 5-8h | Единая БД |
| 0.5 | **Event Bus** (минимальный: Neon-based outbox pattern) | — | 8-12h | Async events между подсистемами |
| 0.6 | **ЦД Event Store** (WP-24 Phase 1) | 0.5 | 10-15h | user_events таблица, append-only, первая проекция (engagement) |

**Milestone:** Web App с SSO, дашборд с ЦД данными, SurrealDB полностью убран.

### Фаза 1: Core Product (май–июль 2026, ~12 недель)

**Цель:** Web App как рабочий продукт + Billing + ЦД проекции + Notifications

| # | Задача | Зависимости | Бюджет | Результат |
|---|--------|-------------|--------|-----------|
| 1.1 | **Web App: дашборд + ЦД** («банковское приложение»: баланс токенов, прогресс, маршрут) | Фаза 0 | 30-40h | Пользователь видит своё состояние развития |
| 1.2 | **Web App: обучение** (руководства + рабочая тетрадь + ДЗ-чекер) | 1.1 | 30-40h | SC-2 реализован в Web App |
| 1.3 | **Billing Service** (Stripe + подписки + feature gating) | 1.1, ORY | 20-30h | Платные функции, подписки |
| 1.4 | **ЦД: проекции** (skill_mastery BKT, memory_decay HLR) | Фаза 0.6 | 15-20h | Персонализация (SC-4) |
| 1.5 | **LMS API-слой** (обёртка для интеграции с Web App) | 1.2 | 15-20h | Рабочая тетрадь + ДЗ доступны через Web App |
| 1.6 | **CRM / Onboarding** (воронка, онбординг SC-1) | 1.1 | 10-15h | Управление конверсией T1→T5 |
| 1.7 | **Notification Service** (push/email/in-app) | 1.1, Event Bus | 10-15h | Ежедневные nudges, напоминания, инсайты из ЦД |
| 1.8 | **ДЗ-чекер как сервис** (выделить из LMS, ИИ-проверка) | 1.5, LMS API | 10-15h | ИИ-проверка ДЗ в Web App и боте |
| 1.9 | **Панель наставника / Управление потоками** (SC-10) | 1.2, 1.8 | 15-20h | Табель, очередь ДЗ, аналитика; создание потоков, назначение наставников |

**Milestone:** Платный продукт с «банковским» UX. Пользователь может: зарегистрироваться → онбординг → учиться → проверять ДЗ → платить → видеть прогресс → получать уведомления. Наставник может: видеть табель → проверять ДЗ → давать обратную связь. Администратор может: запускать потоки → назначать наставников.

### Фаза 2: Экосистема (август–декабрь 2026, ~20 недель)

**Цель:** Токены + ESG + команды + сертификация + полная экосистема

| # | Задача | Зависимости | Бюджет | Результат |
|---|--------|-------------|--------|-----------|
| 2.1 | **Эпистемический граф (ESG)** — граф знаний/компетенций | ЦД, Knowledge MCP | 20-30h | Основа для Proof-of-Impact и сертификации |
| 2.2 | **Loyalty / Proof-of-Impact** (токеновый движок) | Billing, Event Bus, ESG | 20-30h | SC-5 реализован |
| 2.3 | **Activity Hub** (агрегация событий) | Event Bus | 15-20h | Единый поток активности |
| 2.4 | **Certification System** (цифровые сертификаты, верификация) | ESG, ЦД | 15-20h | Подтверждение компетенций |
| 2.5 | **Генератор персонального руководства** (WP-58) | ЦД, Knowledge MCP | 15-20h | ИИ-генерация маршрута |
| 2.6 | **Unified Search** (кросс-системный поиск) | Knowledge MCP, Guides, ЦД | 10-15h | Единый поиск по всей платформе |
| 2.7 | **Team Service** (формирование команд SC-8) | Activity Hub, ЦД | 20-30h | Подбор, каналы, ИИ-агенты |
| 2.8 | **Discord интеграция** (каналы, боты-агенты) | Team Service | 15-20h | Командная работа |
| 2.9 | **Monitoring** (Grafana Cloud) | — | 8-12h | Observability для всех систем |
| 2.10 | **ЦД: LLM-экстракция + misconceptions** (WP-24 Phase 3) | 1.4 | 15-20h | Полная модель ЦД |
| 2.11 | **Web App: сообщество** (интеграция с Discourse SSO, deeplinks) | Фаза 1 | 10-15h | SC-6 в Web App |
| 2.12 | **ИИ-агенты → Web App** (API для отображения результатов агентов) | Фаза 1 | 10-15h | Агенты видны в Web App |

**Milestone:** Полноценная экосистема: обучение + токены + ESG + сертификация + команды + мониторинг.

### Фаза 3: Масштабирование (2027+)

| # | Задача | Зависимость |
|---|--------|-------------|
| 3.1 | **Kubernetes миграция** (Railway → K8s) | Фаза 2 |
| 3.2 | **Международная локализация** (EN → другие языки) | Web App |
| 3.3 | **Apps SDK / маркетплейс** (Global Core + Local Edge) | Event Bus, API Gateway |
| 3.4 | **Revenue Sharing** (автоматическое распределение) | Billing, Loyalty |
| 3.5 | **LMS декомпозиция** (замена Vaadin 8 монолита) | LMS API, Web App |
| 3.6 | **Семинары / Вебинары** (платформенная интеграция live-событий) | Web App, Notifications |
| 3.7 | **Mobile App** (нативное или PWA расширение) | Web App |
| 3.8 | **Рабочая тетрадь v2: Моделер** (симуляции, визуализации) | 1.2 Рабочая тетрадь |

### Timeline (визуальный)

```
2026      Mar    Apr    May    Jun    Jul    Aug    Sep    Oct    Nov    Dec    2027
          ├──────┤──────┤──────┤──────┤──────┤──────┤──────┤──────┤──────┤
          │ Фаза 0: Фундамент │                                          │
          │ Web App scaffold   │                                          │
          │ ORY SSO            │                                          │
          │ SurrealDB→Neon     │                                          │
          │ Event Bus skeleton │                                          │
          │ ЦД Event Store     │                                          │
          ├────────────────────┤                                          │
                               │ Фаза 1: Core Product                    │
                               │ «Банковский» дашборд + обучение         │
                               │ Billing (Stripe)                        │
                               │ ЦД проекции (BKT, HLR)                 │
                               │ Notification Service                    │
                               │ ДЗ-чекер как сервис                     │
                               │ LMS API + Рабочая тетрадь               │
                               │ CRM / Onboarding / Бэк-офис            │
                               │ Панель наставника / Потоки              │
                               ├────────────────────┤                    │
                                                    │ Фаза 2: Экосистема│
                                                    │ ESG (эпист. граф)  │
                                                    │ Proof-of-Impact    │
                                                    │ Certification      │
                                                    │ Personal Guide Gen │
                                                    │ Unified Search     │
                                                    │ Team Service       │
                                                    │ Discord            │
                                                    │ Monitoring         │
                                                    │ ЦД: LLM-экстракция│
                                                    ├────────────────────┤
                                                                    2027 → Фаза 3
                                                                    K8s, Apps SDK,
                                                                    Revenue Sharing,
                                                                    Семинары, Mobile
```

---

## ЭМОГССБ-оценка целевой архитектуры v2

> АрхГейт (CLAUDE.md §5): порог ≥8. Оценка общей архитектуры платформы, не отдельных компонентов.

| # | Характеристика | Оценка | Обоснование |
|---|---------------|--------|-------------|
| Э | **Эволюционируемость** | **9** | 12 принципов, модульность (30 подсистем → 57 сервисов), Event Bus для loose coupling, Strategy pattern для billing/PII, тиры T1→T5. Добавление нового сервиса не ломает существующие. Двух-юрисдикционная архитектура через адаптеры, не через fork кода. **Риск:** 30 подсистем — много зависимостей; без Event Bus первые фазы будут tight-coupled |
| М | **Масштабируемость** | **8** | При 10x: Neon autoscaling, CF Workers global edge, Vercel edge SSR, K8s в Фазе 3. Две ноды (RU + EU) для geo-distribution. pgvector для search. **Риск:** Neon free tier ограничен; репликация RU↔EU при 10x — сложная задача. Event Bus на pg_notify не масштабируется за ~1000 msg/sec |
| О | **Обучаемость** | **8** | 3-слойная архитектура (IPO), понятные тиры (T1→T5), ASCII-диаграммы, role-centric модель. CLAUDE.md + PACK как документация. **Риск:** 30 подсистем, 14 открытых вопросов, 57 сервисов — новому разработчику нужно ~2 дня на погружение. Двух-юрисдикционность добавляет когнитивную нагрузку |
| Г | **Генеративность** | **9** | Работает в шаблоне экзокортекса: FMT-exocortex-template → IWE → платформа. Создаёт платформу (не разовый продукт). Apps SDK + маркетплейс в Фазе 3 — возможность для сторонних. Global Core + Local Edge — масштабирование через локальных партнёров. Двойник + ESG + токены — замкнутый цикл роста |
| С | **Скорость** | **7** | Web App (Next.js SSR) <1s, бот <3s, MCP <500ms (CF Workers). **Риск:** Двойной деплой (RU + EU) увеличивает CI/CD pipeline. Event Bus на pg_notify — минимальная задержка, но нет гарантий доставки. Репликация RU↔EU добавляет latency для кросс-нодовых операций |
| С | **Современность** | **9** | Next.js 15 + AI SDK v6, MCP (Context Engineering SOTA.002), Event Sourcing для ЦД, Role-centric (DP.D.033), DDD Strategic (SOTA.001), Coupling Model (SOTA.011). Vercel + CF Workers — cloud-native. **Проверено по memory/sota-reference.md** |
| Б | **Безопасность** | **8** | ORY (OAuth2 PKCE), RLS в Neon, Knowledge≠UserData (P6), GDPR + 152-ФЗ compliance design. **Риск:** PII в двух юрисдикциях — увеличенная attack surface. ORY hosted = зависимость от третьей стороны. Нет WAF в текущей схеме. Санкционный compliance (Q11) не решён |

**Средний балл: 8.3/10** — проходит АрхГейт (порог ≥8).

**Сильные стороны:**
- Эволюционируемость и генеративность — архитектура создаёт платформу, а не продукт
- Современный стек с проверкой по SOTA
- Двух-юрисдикционность через адаптеры, без дублирования бизнес-логики

**Ключевые риски (управляемые):**
1. **Скорость CI/CD** при двойном деплое — решается единым Docker image + разные env
2. **Event Bus масштабируемость** — pg_notify → NATS/RabbitMQ при необходимости (Фаза 2-3)
3. **Репликация RU↔EU** — нужен чёткий data classification (Q13)
4. **30 подсистем** — управляемо через фазированный roadmap (P0→P3)

---

## ADR: Ключевые архитектурные решения

> Сводка всех принятых и предлагаемых решений. Статус: ✅ принято, 🔶 предлагается (требует согласования), ❓ открыто.

| # | Решение | Статус | Обоснование | Score |
|---|---------|--------|-------------|-------|
| ADR-001 | **Multi-surface с Web-ядром (Next.js)** | ✅ Принято | Международная аудитория, PWA, rich UI | 69/80 |
| ADR-002 | **Event Sourcing для ЦД** | ✅ Принято | Immutable events, 5 проекций, rollback | 52/60 (8.7) |
| ADR-003 | **Role-centric архитектура** | ✅ Принято | Роль ≠ исполнитель, замена без разрушения | 50/60 |
| ADR-004 | **Neon PostgreSQL как единая СУБД** | ✅ Принято | Отказ от SurrealDB, pgvector, RLS | — |
| ADR-005 | **Railway → Kubernetes** | ✅ Принято | Решение архитектора 19 фев | — |
| ADR-006 | **ORY Network для SSO** | ✅ Принято | PKCE flow, интеграция с LMS и MCP | — |
| ADR-007 | **Двойной деплой RU + EU (P12)** | 🔶 Предлагается | Два сайта, два набора серверов, единый бэкенд | ЭМОГССБ 8.3 |
| ADR-008 | **Billing через Strategy pattern** | 🔶 Предлагается | YooKassa (РФ) + Stripe (мир), единая логика | — |
| ADR-009 | **Event Bus: Outbox + pg_notify** | 🔶 Предлагается | Минимальные зависимости, масштабирование позже | Q4 |
| ADR-010 | **RLS для изоляции данных** | 🔶 Предлагается | Одна БД, фильтрация по user_id | Q1 |
| ADR-011 | **Discord для командной работы** | 🔶 Предлагается | Готовая инфра, боты, voice; позже → собственный | Q6 |
| ADR-012 | **LMS обёртка (API), не замена** | 🔶 Предлагается | Java 8 монолит; замена в Фазе 3 | Q7 |
| ADR-013 | **«Банковское приложение» UX** | 🔶 Предлагается | Привычка ежедневной проверки развития | WP-65 |
| ADR-014 | **Трёхосевая модель доступов + Позиции** (DP.D.034) | ✅ Принято | Permission = Entitlement ∩ Role ∩ Scope. Позиции = именованные бандлы. Zanzibar ReBAC | ЭМОГССБ 8.7 |

**Требуют юридического решения:** Q9 (152-ФЗ), Q11 (санкции), Q14 (юрлица).
**Требуют архитекторского согласования:** Q1, Q2, Q4, Q13.

### ADR-014: Трёхосевая модель доступов + Позиции (DP.D.034)

> **Статус:** ✅ Принято. **ЭМОГССБ:** 8.7/10. **Source-of-truth:** [`DP.D.034-access-control-model.md`](../../../PACK-digital-platform/pack/digital-platform/DP.D.034-access-control-model.md) в PACK-digital-platform.

#### Три оси доступа

Доступ на платформе определяется тремя ортогональными осями:

| Ось | Что определяет | Примеры |
|-----|---------------|---------|
| **Entitlement (Тир)** | Что ДОСТУПНО по подписке | T0–T5, TM1–TM3. Feature gating |
| **Role (Роль)** | Что можно ДЕЛАТЬ | 9 ролей: Участник, Автор, Администратор, Бухгалтер, Маркетолог, Наставник, Тех.оператор, Амбассадор, Владелец. «Шляпы», не подроли |
| **Scope (Область видимости)** | Над ЧЕМ | Привязка роли к ресурсу: `cohort:X`, `program:*`, `group:A` |

**Формула:** `Permission = Entitlement ∩ Role ∩ Scope`

**Ключевое:** «Администратор-1» и «Администратор-2» — это НЕ разные роли. Это одна роль **Администратор** с разным scope (`cohort:X` vs `program:*`).

#### Позиции (Position) — бандлы назначения

**Позиция** — именованный бандл из трёх осей, назначаемый одним действием.

> **Термин UL:** «Позиция» (не «должность» — у нас сообщество, не компания). В коде: `preset`.

| Позиция | Role | Tier | Scope | Кто назначает |
|---------|------|------|-------|---------------|
| **Наставник потока** | Наставник | TM2 | `cohort:X/group:Y` | Администратор |
| **Куратор программы** | Администратор + Автор | T0 | `program:Z` | Владелец |
| **Стажёр-наставник** | Наставник | TM1 | `cohort:X/group:Y` (read-only) | Старший наставник |
| **Амбассадор** | Амбассадор + Участник | T2+ | `referrals:*` | Владелец / автоматически |

**4 способа назначения доступов (по приоритету):**

| # | Способ | Когда | Пример |
|---|--------|-------|--------|
| 1 | **Auto-assignment** | Подписка, регистрация — автоматически | Оплатил T2 → feature gating обновлён |
| 2 | **Position** (основной) | Администратор назначает позицию | «Назначить Ивана Наставником потока W11» → система раскладывает в Role + Tier + Scope |
| 3 | **Group** | Для потоков, групп | Все участники cohort:X получают доступ к материалам потока |
| 4 | **Manual override** | Исключения | Владелец вручную даёт scope `program:*` конкретному администратору |

#### Реализация

- **ORY Kratos** — identity (кто ты)
- **JWT claims** — tier + roles (что тебе доступно и что можешь делать)
- **ORY Keto / Neon таблица** — scope как ReBAC-кортежи в стиле Google Zanzibar (над чем именно)
- **Positions** — таблица `positions` в Neon: `{id, name, preset_code, role_ids[], tier, scope_template}`. Назначение: `user_positions` (user_id, position_id, resolved_scope)

---

## Открытые вопросы для согласования с архитектором

| # | Вопрос | Контекст | Предпочтительный вариант |
|---|--------|----------|--------------------------|
| Q1 | Изоляция данных в Neon | DP.D.031, вопрос C5 | **RLS** (Row-Level Security). Одна БД, фильтрация по user_id |
| Q2 | ORY за границей | Данные в EU, ORY hosted глобально | Обсудить с Пашей: self-hosted vs hosted с DPA |
| Q3 | Web App hosting | Vercel vs Railway vs Cloudflare Pages | **Vercel** (SSR + Edge + AI SDK). Позже → K8s |
| Q4 | Event Bus реализация | Outbox pattern в Neon vs RabbitMQ vs NATS | **Outbox + pg_notify** (минимальный, без новых зависимостей) |
| Q5 | Discourse SSO | Discourse + ORY + Web App | DiscourseConnect + ORY (встроенный SSO протокол Discourse) |
| Q6 | Discord vs собственный чат | SC-8: реал-тайм команды | **Discord** (готовая инфра, боты, voice). Позже: собственный → Web App |
| Q7 | LMS замена vs обёртка | Java 8 монолит | **Обёртка (API)** на ближайшие 12 мес. Замена в Фазе 3 |
| Q8 | Redis vs CF KV для кеша | Latency, стоимость | **CF KV** для MCP, **Vercel KV** для Web App. Redis при необходимости в K8s |
| Q9 | **152-ФЗ: локализация ПД** | P12: граждане РФ, хранение ПД | Юр. консультация. Вариант A: PII-прокси (ФИО/email в РФ, остальное в EU) |
| Q10 | **Единый тариф в разных валютах** | P12: RUB/USD/EUR | Один тариф, конвертация по курсу? Или региональные цены? |
| Q11 | **Санкционный compliance** | P12: проверка при регистрации | Нужна ли автоматическая проверка? Юр. консультация |
| Q12 | **Серверы в РФ** | P12: PII-прокси или реплика | Hetzner Russia / VK Cloud / Selectel — для чего именно |
| Q13 | **Репликация данных RU↔EU** | P12: eventual consistency vs strong | Какие данные реплицировать? Какая задержка допустима? |
| Q14 | **Два юрлица или одно?** | P12: влияет на 152-ФЗ, договоры, оплату | РФ-юрлицо + международное? Или одно международное? |

---

## Следующие шаги

1. **Согласовать с архитектором:** Q1-Q14 (особенно Q1, Q2, Q4, Q9, Q13, Q14)
2. **Юридическая консультация:** Q9 (152-ФЗ), Q11 (санкции), Q14 (юрлица)
3. **Специфицировать Web App** (WP-65 → Phase 0.1): auth flow, страницы, API, двойной деплой (RU + World)
4. **Специфицировать Billing** (новый WP): тарифы, Stripe + YooKassa, feature gating, мультиюрисдикционность
5. **Запланировать SurrealDB миграцию** (guides-mcp + docs publish → Neon)
6. **Начать Phase 0.1** (Web App scaffold) параллельно с текущими WP
