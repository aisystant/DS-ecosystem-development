---

type: doc
audience: mixed
edit_mode: manual
layer: service
scope: local-edge
security: internal
status: draft
version: 2.0
created: 2025-11-13
---


# Описание CRM

Система управления взаимоотношениями с участниками экосистемы — центральный хаб для работы с лидами, воронками продаж, сегментацией и коммуникациями. Поддерживает как автоматизированные розничные продажи (self-service онбординг), так и персональное ведение оптовых сделок (b2b: вузы, корпорации). Реализует принципы FPF: эволюционность через оптимизацию воронок, сквозную целостность от первого касания до retention, дидактическую прозрачность каждого взаимодействия.

## Назначение

CRM — это **единая точка управления жизненным циклом участников**: от первого интереса до долгосрочного engagement и advocacy.

### Ключевые функции

1. **Управление лидами и контактами**
   - Сбор лидов из всех каналов (сайт, события, рекомендации)
   - Квалификация и scoring лидов (готовность к конверсии)
   - Сегментация по характеристикам и поведению
   - Обогащение данных контактов
   - Управление дубликатами и merge

2. **Автоматизированные воронки продаж (b2c)**
   - Воронка регистрации (<30 минут от интереса до первого действия)
   - Воронка активации (first value, aha-moment)
   - Воронка конверсии (free → paid, trial → subscription)
   - Воронка retention (предотвращение churn)
   - Автоматические триггеры и email sequences

3. **Персональное ведение сделок (b2b)**
   - Pipeline для оптовых сделок (вузы, корпорации)
   - Tracking этапов сделки (lead → qualified → proposal → negotiation → closed)
   - Управление ставками и кастомными предложениями
   - Документооборот (contracts, NDA, invoices)
   - Координация с командой продаж

4. **Коммуникации и engagement**
   - Email campaigns (newsletters, drip campaigns)
   - In-app messaging и notifications
   - SMS и push notifications
   - Персонализированные touchpoints
   - Запись истории всех взаимодействий

5. **Аналитика и оптимизация**
   - Метрики воронок (conversion rates, drop-off points)
   - LTV, CAC, Payback period
   - Cohort analysis (retention curves)
   - A/B testing campaigns
   - Attribution (какой канал привел к конверсии)

### Роль в архитектуре

CRM координирует взаимодействие с участниками:
- Получает лиды из **Club** (события), **LMS** (trial sign-ups), внешних каналов (ads)
- Синхронизирует данные с **Digital Twin** (unified profile)
- Триггерит автоматизацию через **Activity Hub** (events)
- Интегрирует с **Billing** (подписки, платежи)
- Передаёт данные в **Guide** (онбординг маршруты)

## Архитектура

### Компоненты

#### 1. Lead Management (Управление лидами)

**Назначение:** Сбор, квалификация и распределение лидов.

**Функции:**
- **Lead Capture** — приём лидов из всех источников (web forms, events, referrals, imports)
- **Lead Enrichment** — обогащение данных (company info, social profiles, firmographic data)
- **Lead Scoring** — оценка качества лида (fit score, engagement score)
- **Lead Routing** — автоматическое распределение лидов (round-robin, territory-based)
- **Lead Nurturing** — подогрев лидов (drip campaigns, content marketing)

**Lead Sources:**
- **Organic** — прямые регистрации на сайте
- **Referral** — рекомендации от участников
- **Events** — встречи, вебинары, воркшопы (Club)
- **Content** — скачивание материалов, подписки на блог
- **Paid** — реклама (Google Ads, Facebook, LinkedIn)
- **Partnerships** — партнёрские каналы (вузы, корпорации)

**Scoring model:**
```python
def calculate_lead_score(lead):
    fit_score = (
        company_size_score(lead.company_size) * 0.3 +
        industry_match_score(lead.industry) * 0.2 +
        role_relevance_score(lead.job_title) * 0.2 +
        budget_indicator_score(lead.budget) * 0.3
    )

    engagement_score = (
        website_activity_score(lead.page_views) * 0.3 +
        content_downloads_score(lead.downloads) * 0.2 +
        email_engagement_score(lead.opens, lead.clicks) * 0.3 +
        event_attendance_score(lead.events) * 0.2
    )

    # Общий score (0-100)
    return (fit_score * 0.5 + engagement_score * 0.5) * 100
```

**Интеграции:**
- Digital Twin (4.11) — синхронизация профилей
- Activity Hub (4.6) — события захвата лидов
- Marketing automation tools (Mailchimp, SendGrid)

#### 2. Contact & Account Management (Управление контактами и аккаунтами)

**Назначение:** Управление базой контактов и организаций (accounts).

**Функции:**
- **Contact CRUD** — создание, чтение, обновление, удаление контактов
- **Account Management** — управление организациями (для b2b)
- **Relationship Mapping** — связи между контактами (influencer, decision maker, champion)
- **Duplicate Detection** — обнаружение и объединение дубликатов
- **Data Quality** — валидация и очистка данных

**Данные контакта:**
- Базовые (имя, email, телефон, роль)
- Демографические (возраст, локация, образование)
- Firmographic (компания, индустрия, размер, бюджет)
- Behavioral (история активности, engagement level)
- Lifecycle stage (lead, prospect, customer, advocate)

**Данные аккаунта (для b2b):**
- Название организации, тип (вуз, корпорация, НКО)
- Размер (количество сотрудников, студентов)
- Индустрия, география
- Контракты и история покупок
- Decision-making unit (DMU) — кто принимает решения

**Интеграции:**
- ORY (4.14) — identity синхронизация
- Digital Twin (4.11) — профили участников
- Billing (4.9) — история платежей

#### 3. Sales Pipeline (Воронки продаж)

**Назначение:** Управление сделками и стадиями продаж.

**Функции:**
- **Deal Tracking** — отслеживание сделок по стадиям
- **Stage Management** — управление этапами воронки
- **Forecasting** — прогнозирование выручки
- **Win/Loss Analysis** — анализ выигранных/проигранных сделок
- **Activity Logging** — логирование всех активностей по сделке

**Стадии воронки (b2c - автоматизированная):**
1. **Visitor** — посетитель сайта
2. **Lead** — оставил контакты
3. **Trial** — зарегистрировался на trial
4. **Activated** — совершил первое значимое действие
5. **Converted** — оплатил подписку
6. **Retained** — продлил подписку
7. **Advocate** — рекомендует другим

**Стадии воронки (b2b - персональная):**
1. **Lead** — первый контакт
2. **Qualified** — подтверждена заинтересованность и fit
3. **Meeting** — проведена встреча, выявлены потребности
4. **Proposal** — отправлено предложение
5. **Negotiation** — обсуждение условий
6. **Contract** — подписание договора
7. **Closed Won** — сделка завершена успешно
8. **Closed Lost** — сделка не состоялась

**Метрики:**
- **Conversion Rate** — доля переходов между стадиями
- **Velocity** — скорость продвижения по воронке
- **Deal Size** — средний чек
- **Win Rate** — доля выигранных сделок
- **Sales Cycle Length** — длительность цикла сделки

**Интеграции:**
- Billing (4.9) — создание подписок и инвойсов
- Activity Hub (4.6) — события по сделкам
- Guide (4.5) — онбординг после конверсии

#### 4. Marketing Automation (Маркетинговая автоматизация)

**Назначение:** Автоматизация коммуникаций и nurturing campaigns.

**Функции:**
- **Campaign Management** — создание и запуск campaigns
- **Email Automation** — автоматические email sequences (drip campaigns)
- **Segmentation** — сегментация аудитории для таргетинга
- **Personalization** — персонализация сообщений
- **Trigger-based actions** — триггеры на основе событий

**Типы campaigns:**
- **Onboarding** — приветственная серия для новых участников
- **Activation** — подталкивание к первому действию (trial → active)
- **Conversion** — конверсия в платящих (free → paid)
- **Retention** — предотвращение churn (win-back campaigns)
- **Upsell/Cross-sell** — продажа дополнительных услуг
- **Re-engagement** — возврат неактивных участников

**Пример campaign (onboarding):**
```
Day 0: Приветственное письмо + quick start guide
Day 1: Напоминание о первом шаге (если не выполнен)
Day 3: Tips & tricks для эффективного использования
Day 7: Приглашение на webinar или event
Day 14: Предложение trial extension или discount
Day 21: Request for feedback + NPS survey
```

**Триггеры:**
- **Event-based** — действие участника (signup, first login, course completed)
- **Time-based** — по расписанию (7 дней после регистрации)
- **Score-based** — достижение порога (lead score > 80)
- **Lifecycle-based** — изменение стадии (lead → customer)

**Интеграции:**
- Activity Hub (4.6) — события для триггеров
- Digital Twin (4.11) — персонализация контента
- Email service providers (SendGrid, Mailchimp)

#### 5. Customer Success (Успех клиентов)

**Назначение:** Обеспечение успеха участников и предотвращение churn.

**Функции:**
- **Health Scoring** — оценка здоровья аккаунта (churn risk)
- **Proactive Outreach** — проактивное вмешательство при проблемах
- **Onboarding Tracking** — мониторинг онбординга
- **Usage Analytics** — анализ использования продукта
- **Renewals Management** — управление продлениями

**Health score indicators:**
- **Usage frequency** — как часто участник активен
- **Feature adoption** — какие фичи использует
- **Engagement level** — уровень вовлечённости
- **Support tickets** — количество и тип обращений
- **Sentiment** — настрой участника (NPS, feedback)

**Churn risk triggers:**
- Снижение активности (не заходил >14 дней)
- Негативный feedback или низкий NPS
- Много support tickets без resolution
- Не использует ключевые фичи
- Приближение renewal date без engagement

**Actions:**
- **Red flag:** Срочное вмешательство (personal call, special offer)
- **Yellow flag:** Nudge или targeted campaign
- **Green flag:** Upsell или advocacy program

**Интеграции:**
- Digital Twin (4.11) — health score и состояние
- Activity Hub (4.6) — мониторинг активности
- Guide (4.5) — adaptive intervention

#### 6. Reporting & Analytics (Отчётность и аналитика)

**Назначение:** Аналитика продаж, маркетинга и customer success.

**Функции:**
- **Dashboards** — дашборды для команд (sales, marketing, CS)
- **Funnel Analysis** — анализ воронок и конверсий
- **Cohort Analysis** — анализ когорт (retention curves)
- **Attribution** — attribution моделирование (first-touch, last-touch, multi-touch)
- **Forecasting** — прогнозирование выручки и churn

**Ключевые метрики:**
- **MRR/ARR** — месячная/годовая recurring revenue
- **LTV** — lifetime value клиента
- **CAC** — customer acquisition cost
- **Payback Period** — срок окупаемости CAC
- **Churn Rate** — процент ушедших клиентов
- **NRR** — net revenue retention (с учётом upsell/downgrades)
- **NPS** — net promoter score

**Отчёты:**
- Sales pipeline report (по стадиям)
- Campaign performance report
- Lead source effectiveness
- Customer health report
- Churn analysis report

**Интеграции:**
- Billing (4.9) — финансовые данные
- Activity Hub (4.6) — данные активности
- BI tools (Metabase, Superset, Tableau)

### Технологический стек

**Backend:**
- Python/Django или Node.js для API
- PostgreSQL для structured data
- Redis для caching и queues
- Celery для background jobs (email sending, scoring updates)

**CRM Platform:**
- Custom-built на Django/FastAPI
- Альтернатива: интеграция с HubSpot, Salesforce (с кастомизацией)

**Marketing Automation:**
- SendGrid/Mailchimp для email
- Twilio для SMS
- OneSignal для push notifications
- Intercom для in-app messaging

**Analytics:**
- Mixpanel/Amplitude для product analytics
- Metabase для внутренних дашбордов
- Google Analytics для web tracking

**Инфраструктура:**
- Kubernetes
- Kafka для events (интеграция с Activity Hub)
- Airflow для ETL jobs

## Процессы

### П1. Онбординг нового лида (b2c)

**Назначение:** Автоматизированный путь от первого касания до активного участника.

**Этапы:**
1. **Lead Capture** — заполнение формы на сайте (email, имя, интересы)
2. **Welcome Email** — приветственное письмо с ссылкой на активацию
3. **Account Creation** — создание аккаунта через ORY
4. **Profile Setup** — заполнение профиля (цели, навыки) → Digital Twin
5. **First Path** — генерация персонального маршрута (Guide)
6. **First Action** — выполнение первого шага (aha-moment)
7. **Activation Confirmed** — участник активирован

**Автоматизация:**
- Все шаги автоматизированы
- Nudges если застрял (не завершил профиль >24 часа)
- Personal assistance если сильно застрял (>3 дня без активности)

**Метрики:**
- Time to Activation (<30 минут целевое)
- Activation Rate (>60%)
- Drop-off points (где теряем людей)

**Интеграции:**
- ORY (4.14) — создание identity
- Digital Twin (4.11) — инициализация профиля
- Guide (4.5) — первый маршрут
- Activity Hub (4.6) — tracking событий

### П2. Ведение b2b сделки (вуз/корпорация)

**Назначение:** Персональное ведение оптовой сделки.

**Этапы:**
1. **Inbound Lead** — заявка с сайта или рекомендация
2. **Qualification Call** — звонок для квалификации (fit, budget, timeline)
3. **Discovery Meeting** — встреча для выявления потребностей
4. **Proposal Preparation** — подготовка кастомного предложения
5. **Proposal Presentation** — презентация предложения
6. **Negotiation** — обсуждение условий и pricing
7. **Contract Signing** — подписание договора
8. **Onboarding** — онбординг команды клиента
9. **Implementation** — внедрение и обучение
10. **Ongoing Support** — поддержка и customer success

**Роли:**
- **Sales Rep** — ведёт сделку
- **Solution Engineer** — technical demos
- **Customer Success Manager** — onboarding и поддержка

**Документы:**
- Proposal/Commercial offer
- NDA (если нужно)
- Contract/MSA
- SOW (Statement of Work)
- Invoices

**Интеграции:**
- Billing (4.9) — создание кастомных тарифов
- Case Management (4.13) — проекты для клиента
- Document management (DocuSign, PandaDoc)

### П3. Retention campaign (предотвращение churn)

**Назначение:** Удержание участников с высоким risk of churn.

**Триггеры:**
- Health score < 50 (красная зона)
- Не заходил >14 дней
- Негативный feedback (NPS < 6)
- Approaching renewal без активности

**Действия:**
1. **Identify at-risk users** — автоматическая идентификация
2. **Segment** — сегментация по причинам риска
3. **Personalized Outreach** — персонализированная коммуникация
   - Email: "Мы заметили, что вы давно не заходили..."
   - In-app: Banner с предложением помощи
   - Personal call (для high-value customers)
4. **Offer Intervention** — предложение помощи (personal coaching, discount, extended trial)
5. **Track Response** — отслеживание реакции
6. **Re-engage or Churn** — либо re-engagement, либо churn

**Tactics:**
- Win-back campaigns для churned users
- Special offers (discount, bonus content)
- Feature highlights (что нового)
- Success stories (социальное доказательство)

**Интеграции:**
- Digital Twin (4.11) — health score
- Guide (4.5) — adaptive intervention
- Activity Hub (4.6) — мониторинг активности

### П4. Upsell/Cross-sell campaign

**Назначение:** Продажа дополнительных услуг существующим клиентам.

**Сегменты:**
- **High-value users** — активные, high LTV, готовы платить больше
- **Power users** — использующие advanced фичи, нужен premium
- **Teams** — одиночные пользователи, которым нужны team plans

**Offers:**
- **Upsell:** Upgrade с базового на premium план
- **Cross-sell:** Дополнительные модули, сервисы (личный ментор, групповые программы)
- **Add-ons:** Compute credits, storage, custom features

**Механика:**
- In-app upsell prompts (при достижении лимитов)
- Email campaigns с предложениями
- Personal outreach для high-value accounts

**Интеграции:**
- Billing (4.9) — управление апгрейдами
- Activity Hub (4.6) — триггеры на основе usage

## Интеграции

### Входящие интеграции

Источники лидов и данных:

- [[4.3. Клуб]] — лиды с событий, участники сообщества
- [[4.4. Платформа обучения]] — trial sign-ups, free course registrations
- [[4.14. Система идентификации и доступа (ORY)]] — identity данные
- [[4.11. Цифровой двойник]] — профили и цели участников
- [[4.6. Система учета активностей (хаб активностей)]] — события активности
- Web forms — захват лидов с сайта
- External sources — импорт лидов, API интеграции

### Исходящие интеграции

Использование данных CRM:

- [[4.9. Биллинг]] — создание подписок и инвойсов
- [[4.5. Проводник по персональному маршруту]] — онбординг маршруты
- [[4.11. Цифровой двойник]] — синхронизация профилей
- [[4.6. Система учета активностей (хаб активностей)]] — события CRM (deal created, email sent)
- [[Система баллов и лояльности 3.1]] — начисления за рекомендации
- Email/SMS/Push providers — отправка сообщений

## API и контракты

### Основные эндпоинты

**Leads:**
```
POST /crm/leads                         # Создать лид
GET  /crm/leads/:id                     # Получить лид
PUT  /crm/leads/:id                     # Обновить лид
GET  /crm/leads                         # Список лидов (с фильтрами)
POST /crm/leads/:id/convert             # Конвертировать в контакт/сделку
GET  /crm/leads/:id/score               # Lead score
```

**Contacts & Accounts:**
```
POST /crm/contacts                      # Создать контакт
GET  /crm/contacts/:id                  # Получить контакт
PUT  /crm/contacts/:id                  # Обновить контакт
GET  /crm/contacts                      # Список контактов
POST /crm/accounts                      # Создать аккаунт (b2b)
GET  /crm/accounts/:id                  # Получить аккаунт
```

**Deals (Sales Pipeline):**
```
POST /crm/deals                         # Создать сделку
GET  /crm/deals/:id                     # Получить сделку
PUT  /crm/deals/:id                     # Обновить сделку
POST /crm/deals/:id/move                # Переместить на следующую стадию
GET  /crm/deals/:id/activities          # Активности по сделке
GET  /crm/pipeline                      # Pipeline overview
```

**Campaigns:**
```
POST /crm/campaigns                     # Создать campaign
GET  /crm/campaigns/:id                 # Получить campaign
PUT  /crm/campaigns/:id                 # Обновить campaign
POST /crm/campaigns/:id/send            # Запустить campaign
GET  /crm/campaigns/:id/stats           # Статистика campaign
```

**Segmentation:**
```
POST /crm/segments                      # Создать сегмент
GET  /crm/segments/:id                  # Получить сегмент
GET  /crm/segments/:id/members          # Участники сегмента
```

**Analytics:**
```
GET  /crm/metrics/funnel                # Метрики воронки
GET  /crm/metrics/cohorts               # Cohort analysis
GET  /crm/metrics/attribution           # Attribution report
GET  /crm/metrics/health                # Health scores
```

### События

**Lead Events:**
- `crm.lead.created` — лид создан
- `crm.lead.scored` — lead score рассчитан
- `crm.lead.qualified` — лид квалифицирован
- `crm.lead.converted` — лид конвертирован

**Deal Events:**
- `crm.deal.created` — сделка создана
- `crm.deal.stage_changed` — стадия сделки изменена
- `crm.deal.won` — сделка выиграна
- `crm.deal.lost` — сделка проиграна

**Campaign Events:**
- `crm.campaign.sent` — campaign отправлен
- `crm.email.opened` — email открыт
- `crm.email.clicked` — ссылка в email кликнута
- `crm.unsubscribe` — отписка от рассылки

**Customer Success Events:**
- `crm.health.changed` — health score изменился
- `crm.churn_risk.detected` — обнаружен риск churn
- `crm.renewal.approaching` — приближается renewal

## Хранилище данных

### Схема данных

**Таблицы (PostgreSQL):**

```sql
-- Лиды
CREATE TABLE Lead (
  id UUID PRIMARY KEY,
  first_name VARCHAR,
  last_name VARCHAR,
  email VARCHAR UNIQUE NOT NULL,
  phone VARCHAR,
  company VARCHAR,
  job_title VARCHAR,
  source VARCHAR,  -- organic, referral, event, paid, etc
  status VARCHAR,  -- new, qualified, converted, disqualified
  score INT,  -- lead score (0-100)
  assigned_to UUID,  -- sales rep ID
  created_at TIMESTAMP,
  updated_at TIMESTAMP,
  metadata JSONB
);

-- Контакты
CREATE TABLE Contact (
  id UUID PRIMARY KEY,
  user_id UUID UNIQUE,  -- link to ORY identity
  account_id UUID REFERENCES Account(id),
  first_name VARCHAR,
  last_name VARCHAR,
  email VARCHAR,
  phone VARCHAR,
  role VARCHAR,  -- decision_maker, influencer, user, etc
  lifecycle_stage VARCHAR,  -- lead, prospect, customer, advocate
  created_at TIMESTAMP,
  updated_at TIMESTAMP
);

-- Аккаунты (для b2b)
CREATE TABLE Account (
  id UUID PRIMARY KEY,
  name VARCHAR NOT NULL,
  type VARCHAR,  -- university, corporation, ngo
  industry VARCHAR,
  size VARCHAR,  -- employees or students count range
  website VARCHAR,
  billing_address JSONB,
  created_at TIMESTAMP,
  updated_at TIMESTAMP
);

-- Сделки
CREATE TABLE Deal (
  id UUID PRIMARY KEY,
  account_id UUID REFERENCES Account(id),
  contact_id UUID REFERENCES Contact(id),
  title VARCHAR NOT NULL,
  amount DECIMAL,
  currency VARCHAR DEFAULT 'USD',
  stage VARCHAR NOT NULL,  -- lead, qualified, proposal, negotiation, closed_won, closed_lost
  probability INT,  -- 0-100
  expected_close_date DATE,
  actual_close_date DATE,
  owner_id UUID,  -- sales rep ID
  created_at TIMESTAMP,
  updated_at TIMESTAMP,
  lost_reason VARCHAR,
  metadata JSONB
);

-- Активности (логи взаимодействий)
CREATE TABLE Activity (
  id UUID PRIMARY KEY,
  type VARCHAR,  -- email, call, meeting, note, task
  subject VARCHAR,
  description TEXT,
  contact_id UUID REFERENCES Contact(id),
  deal_id UUID REFERENCES Deal(id),
  user_id UUID,  -- кто совершил активность
  completed BOOLEAN DEFAULT false,
  due_date TIMESTAMP,
  completed_at TIMESTAMP,
  created_at TIMESTAMP
);

-- Campaigns
CREATE TABLE Campaign (
  id UUID PRIMARY KEY,
  name VARCHAR NOT NULL,
  type VARCHAR,  -- email, sms, push
  status VARCHAR,  -- draft, scheduled, running, completed, paused
  segment_id UUID,  -- target segment
  template_id UUID,
  scheduled_at TIMESTAMP,
  sent_at TIMESTAMP,
  stats JSONB,  -- sent, opened, clicked, converted
  created_at TIMESTAMP,
  updated_at TIMESTAMP
);

-- Сегменты
CREATE TABLE Segment (
  id UUID PRIMARY KEY,
  name VARCHAR NOT NULL,
  description TEXT,
  filters JSONB,  -- условия фильтрации
  member_count INT,
  last_updated TIMESTAMP,
  created_at TIMESTAMP
);

-- Health Scores (для customer success)
CREATE TABLE HealthScore (
  id UUID PRIMARY KEY,
  user_id UUID NOT NULL,
  score INT,  -- 0-100
  risk_level VARCHAR,  -- green, yellow, red
  factors JSONB,  -- факторы, влияющие на score
  computed_at TIMESTAMP
);
```

### Retention policy

- **Leads:** 2 года неактивные
- **Contacts:** Бессрочно (пока активны)
- **Deals:** Бессрочно
- **Activities:** 3 года
- **Campaigns:** 1 год детальная статистика, бессрочно агрегаты
- **Health Scores:** 6 месяцев история

## Метрики и мониторинг

### Ключевые метрики

| Метрика | Целевое значение | Текущее |
|---------|------------------|---------|
| Lead-to-Customer Conversion Rate | >15% | — |
| Average Deal Size (b2b) | [целевое] | — |
| Sales Cycle Length (b2b) | <60 дней | — |
| CAC (Customer Acquisition Cost) | <$X | — |
| LTV (Lifetime Value) | >$Y | — |
| LTV:CAC Ratio | >3:1 | — |
| Payback Period | <12 месяцев | — |
| MRR Growth Rate | >10% MoM | — |
| Churn Rate (monthly) | <5% | — |
| NRR (Net Revenue Retention) | >100% | — |
| Time to First Value (activation) | <30 минут | — |

### Алерты

**Критические:**
- CRM database unavailable
- Email sending service down
- Lead routing failures
- Integration sync errors (ORY, Billing)

**Предупреждения:**
- High churn risk cohort (>20% of active users)
- Low conversion rate trend (<10%)
- Campaign delivery failures (>5%)
- Lead scoring service slow (>5 sec)
- Deal slipping (overdue by >14 days)

## Roadmap

### v1.0 (MVP)

- [ ] Базовое управление лидами (CRUD, scoring)
- [ ] Contact и Account management
- [ ] Простая b2c воронка (signup → activation)
- [ ] B2b pipeline (manual tracking)
- [ ] Email automation (welcome series)
- [ ] Интеграция с ORY (4.14) для identity
- [ ] Интеграция с Billing (4.9) для subscriptions
- [ ] Базовая аналитика (funnel, conversion rates)
- [ ] Dashboard для команды

### v1.1

- [ ] Advanced lead scoring (ML-based)
- [ ] Automated lead nurturing (drip campaigns)
- [ ] Segmentation engine
- [ ] Health scoring для customer success
- [ ] Churn prediction model
- [ ] Multi-channel campaigns (email + SMS + push)
- [ ] A/B testing framework
- [ ] Attribution modeling
- [ ] Cohort analysis
- [ ] Интеграция с Activity Hub (4.6) для events

### v2.0

- [ ] AI-powered lead routing
- [ ] Predictive deal scoring
- [ ] Conversational AI for lead qualification (chatbot)
- [ ] Advanced personalization (1-to-1 campaigns)
- [ ] Customer data platform (CDP) capabilities
- [ ] Multi-touch attribution
- [ ] Revenue intelligence (Gong-like insights)
- [ ] Integrations marketplace (Zapier-like)
- [ ] Mobile app для sales team
- [ ] Advanced forecasting (ML-based pipeline predictions)

## Связанные документы

- [[4.1. Список подсистем]] — реестр всех систем
- [[4.11. Цифровой двойник]] — профили участников
- [[4.9. Биллинг]] — подписки и платежи
- [[4.3. Клуб]] — события и сообщество
- [[4.5. Проводник по персональному маршруту]] — онбординг маршруты
- [[4.6. Система учета активностей (хаб активностей)]] — события CRM
- [[4.14. Система идентификации и доступа (ORY)]] — identity management
- [[Система баллов и лояльности 3.1]] — вознаграждения за рекомендации
- [[1.4. Концепция функционирования экосистемы для ЦА]] — концепция с FPF
- [[4.0. Информация]] — обзор раздела Системы
- [[0.7. Классификация документов и теги]] — Frontmatter

## История изменений

| Дата | Версия | Описание |
|------|--------|----------|
| 2025-11-13 | 2.0 | Полное переписывание: управление лидами, воронки b2c/b2b, marketing automation, customer success, FPF интеграция |
| [ранее] | 1.0 | Первоначальная заглушка |

---

**Status:** 🟡 Draft
**Owner:** Sales & Marketing Team
**Last Updated:** 2025-11-13
