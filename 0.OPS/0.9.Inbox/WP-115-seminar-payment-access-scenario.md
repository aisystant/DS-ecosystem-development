---
type: scenario-proposal
wp: 115
title: "Рабочий сценарий: Оплата семинара → Доступ → Видео"
status: draft
created: 2026-03-17
author: Tseren + Claude (problem-framing)
related:
  - WP-73 (архитектура платформы, §2.9)
  - WP-85 (Neon, identity layer)
  - DP.D.034 (трёхосевая модель доступа)
  - S62 (Event Access Service)
discussion: true
---

# Рабочий сценарий: Оплата семинара → Доступ → Видео

> **Статус:** draft — для обсуждения с командой.
> **Источник:** WP-73 §2.9.1 (gaps), WP-115 (fulfillment), обсуждение 17 мар 2026.

<details open>
<summary><b>1. Обзор и ключевые решения</b></summary>

## 1.1. Что проектируем

End-to-end сценарий: от маркетинга семинара до доступа к видеозаписи.
Покрывает: семинары (Zoom / Я.Телемост) и потоки с наставниками.

## 1.2. Принятые решения

| # | Решение | Обоснование |
|---|---------|-------------|
| 1 | **Гибрид: Telegram-first + Ory lazy** | Мгновенный доступ для «последнего вагона» (0 сек). Ory — для видео (отложенно) |
| 2 | **Один бот (@aist_me_bot)** — и в чате, и в ЛС | Один бот = одна база. Семинар = точка входа в экосистему. Нет coordination cost (SOTA.006) |
| 3 | **TG-чат открыт для всех → cleanup после** | Маркетинговый рычаг: все видят обсуждение → стимул оплатить |
| 4 | **Email — обязательное поле при оплате** | Единственный guaranteed канал доставки для тех, кто не нажал /start |
| 5 | **ЮКасса (RU) + Stripe (foreign)** | Две юрисдикции (принцип P12) |
| 6 | **Видео на внешнем хостинге (Kinescope)** | JWT API, CDN, DRM. Вне LMS — независимый доступ |
| 7 | **Бот = админ чата семинара** | Видит `new_chat_members` → собирает telegram_id всех входящих |

## 1.3. Ограничения Telegram Bot API

| Факт | Следствие |
|------|-----------|
| Бот **не может** инициировать ЛС — только если пользователь нажал /start | Email = fallback для доставки Zoom-ссылки |
| Бот **не может** получить список всех участников supergroup (100+) | Собираем telegram_id через `new_chat_members` при входе |
| Бот **не может** получить телефон участника чата | Телефон не подходит для cleanup-сверки |
| `getChatMember(chat_id, user_id)` — работает для конкретного user_id | Cleanup возможен, если собрали telegram_id заранее |

</details>

<details open>
<summary><b>2. Сценарий (end-to-end)</b></summary>

## 2.1. Участники

| Участник | Роль в сценарии |
|----------|----------------|
| Пользователь | Покупатель семинара / потока |
| @aist_me_bot | Админ чата + ЛС-доставка + fulfillment |
| Aisystant LMS | Приём оплаты (ЮКасса/Stripe webhook) → webhook боту |
| Neon (PostgreSQL) | Хранение: оплаты, участники чата, маппинг |
| Kinescope | Хранение видео, JWT-доступ |
| Ory | Identity (lazy создание для доступа к видео) |

## 2.2. Фазы

### Фаза 0: Подготовка (за неделю)

```
Администратор:
  1. Создаёт семинар в системе:
     → event_id, название, дата, Zoom/Телемост link, цена
  2. Создаёт TG-чат семинара (supergroup)
  3. Добавляет @aist_me_bot как админа
  4. Публикует invite-ссылку на лендинге и в каналах

Бот (автоматически):
  → Начинает записывать new_chat_members → Neon:
     INSERT INTO chat_members (telegram_id, chat_id, event_id, joined_at)
```

### Фаза 1: Маркетинг (до семинара)

```
TG-чат семинара — ОТКРЫТ для всех:
  → Любой заходит по invite-ссылке
  → Бот записывает telegram_id (new_chat_members)
  → Бот периодически постит:
    «📌 Оплатите участие и получите ссылку на семинар:
     → Через бота: /seminar
     → На сайте: [лендинг]
     После оплаты ссылка придёт мгновенно.»
```

### Фаза 2: Оплата (в любой момент, включая «последний вагон»)

```
КАНАЛ 1: Через бота
  Пользователь → /seminar → выбор семинара → /pay
    → Бот знает telegram_id (автоматически)
    → Бот создаёт платёж:
       ЮКасса (RU-карты) или Stripe (foreign)
       через Aisystant API
    → Пользователь оплачивает
    → Webhook: ЮКасса/Stripe → Aisystant LMS → Webhook → Бот
    → [Fulfillment — см. Фаза 2b]

КАНАЛ 2: Через лендинг (сайт)
  Пользователь → лендинг → «Оплатить» → email (обязательно)
    → Платёж (ЮКасса / Stripe)
    → Webhook → Aisystant LMS → Webhook → Бот
    → Бот: есть telegram_id для этого email?
       ДА → [Fulfillment в ЛС]
       НЕТ → [Fulfillment по email + deeplink]
```

### Фаза 2b: Fulfillment (мгновенный, при любом канале оплаты)

```
Бот получает webhook об успешной оплате:

1. Записать в Neon:
   INSERT INTO payments (telegram_id, email, event_id, paid, paid_at)

2. Определить канал доставки:

   ЕСЛИ telegram_id известен И пользователь писал /start:
     → Отправить в ЛС бота:
       «✅ Оплата прошла!
        Семинар: [название]
        Дата: [дата, время MSK]
        Ссылка: [Zoom / Я.Телемост]
        Чат семинара: [ссылка]»

   ЕСЛИ telegram_id известен, НО не писал /start:
     → Отправить email с Zoom-ссылкой
     → Написать в чат семинара (mention если есть @username):
       «@username, ссылка на семинар отправлена на email.
        Или нажмите /start у @aist_me_bot для мгновенного доступа.»

   ЕСЛИ telegram_id НЕ известен (оплата через сайт):
     → Отправить email с Zoom-ссылкой
     → В email: «Получите ссылку в Telegram: t.me/aist_me_bot?start=sem_{event_id}_{hash}»

3. Обновить whitelist (для cleanup):
   UPDATE chat_members SET paid = true WHERE telegram_id = X AND event_id = Y
```

**Время fulfillment:** 3-5 секунд от оплаты до получения ссылки.

### Фаза 3: Семинар (день X)

```
Бот в чате семинара:
  За 30 мин: «Семинар начинается через 30 минут!
              Оплатившие — ссылка в ЛС бота.
              Не получили? → напишите /start боту @aist_me_bot»

  За 5 мин: «Семинар через 5 минут! Ссылка в ЛС бота.»

Бот в ЛС (повторно):
  За 15 мин: повторная отправка Zoom-ссылки всем оплатившим

«Последний вагон» (оплата за 1-5 мин до начала):
  → Тот же Fulfillment (Фаза 2b) — работает в любой момент
  → Пользователь получает ссылку через 3-5 сек после оплаты

Оплата ВО ВРЕМЯ семинара:
  → Fulfillment + сообщение: «Семинар уже идёт, присоединяйтесь!»
```

### Фаза 4: После семинара (видео)

```
Администратор:
  1. Загружает видео на Kinescope
  2. Получает video_id
  3. Регистрирует в системе: event_id → video_id

Бот (автоматически или по триггеру):
  Для каждого оплатившего:

  ЕСЛИ есть ory_id (уже зарегистрирован):
    → Генерирует JWT: { sub: ory_id, scope: event:seminar-{id}, exp: +365d }
    → Персональная ссылка на Kinescope
    → Отправляет в ЛС: «Видео семинара готово! [ссылка] (доступ 1 год)»

  ЕСЛИ нет ory_id, НО есть telegram_id:
    → Генерирует временный JWT: { sub: tg:{telegram_id}, exp: +7d }
    → Отправляет в ЛС:
      «Видео семинара готово! [ссылка] (доступ 7 дней)
       Для постоянного доступа (1 год): /register»
    → /register: email → magic link → Ory identity → привязка → новый JWT на год

  ЕСЛИ нет telegram_id (только email):
    → Генерирует временный JWT по email: { sub: email:X, exp: +7d }
    → Отправляет на email: ссылка + «Зарегистрируйтесь для постоянного доступа»
```

### Фаза 5: Cleanup (через 24-48ч после семинара)

```
Бот:
  1. Берёт из Neon всех участников чата, которые НЕ оплатили:
     SELECT telegram_id FROM chat_members
     WHERE event_id = 'seminar-X'
       AND left_at IS NULL
       AND telegram_id NOT IN (
         SELECT telegram_id FROM payments
         WHERE event_id = 'seminar-X' AND paid = true
       )

  2. Для каждого неоплатившего:
     → banChatMember(chat_id, telegram_id)  — kick
     → unbanChatMember(chat_id, telegram_id) — снять бан (мягкий kick)

     Rate limit: ~30 req/sec → при 70 kicks ≈ 2-3 сек

  3. За 1 час до cleanup — предупреждение в чате:
     «⏰ Через 1 час чат будет закрыт для неоплативших.
      Оплатить: /seminar или [лендинг]
      Запись семинара будет доступна оплатившим.»

  4. После cleanup — сообщение в чате:
     «Чат закрыт для новых участников.
      Запись семинара доступна оплатившим.»

  5. Отзыв invite-ссылки (revokeChatInviteLink) — чат закрыт.
```

</details>

<details>
<summary><b>3. Потоки с наставниками</b></summary>

Тот же паттерн, но с отличиями:

| Параметр | Семинар | Поток с наставником |
|----------|---------|---------------------|
| Длительность | 1-3 часа | 2-3 месяца |
| TG-чат | Временный (cleanup через 24-48ч) | Постоянный (на весь поток) |
| Cleanup | Однократный после семинара | При старте потока + периодический |
| Видео | Одна запись | Серия записей (еженедельно) |
| Наставник | — | Role:Наставник + Scope:cohort:X (DP.D.034) |
| Доступ | Entitlement ∩ Scope:event:sem-X | Entitlement ∩ Role:Участник ∩ Scope:cohort:X |

### Flow потока

```
Старт потока:
  1. Создаётся TG-чат потока (закрытый с join requests)
  2. @aist_me_bot — админ
  3. Оплатившие → approveChatJoinRequest()
  4. Неоплатившие → declineChatJoinRequest() + «Оплатите для доступа»

Во время потока:
  → Новая оплата → бот добавляет через createChatInviteLink(member_limit=1)
  → Каждое занятие → видео на Kinescope → JWT-ссылка в ЛС

Завершение потока:
  → Чат остаётся (архив обсуждений)
  → Видео доступны по JWT (1 год)
```

</details>

<details>
<summary><b>4. Модель данных (Neon)</b></summary>

```sql
-- Семинары / события
CREATE TABLE events (
  event_id TEXT PRIMARY KEY,
  title TEXT NOT NULL,
  event_type TEXT NOT NULL CHECK (event_type IN ('seminar', 'cohort', 'workshop')),
  event_date TIMESTAMPTZ,
  duration_minutes INT,
  zoom_link TEXT,
  video_id TEXT,                          -- Kinescope video_id (после загрузки)
  chat_id BIGINT,                         -- TG-чат семинара
  price_rub INT,
  price_usd INT,
  status TEXT DEFAULT 'upcoming'          -- upcoming, live, completed, archived
);

-- Оплаты
CREATE TABLE payments (
  id SERIAL PRIMARY KEY,
  event_id TEXT REFERENCES events(event_id),
  telegram_id BIGINT,                     -- NULL если оплата через сайт без привязки
  email TEXT NOT NULL,                    -- Обязательное поле
  ory_id TEXT,                            -- NULL если нет аккаунта Ory
  paid BOOLEAN DEFAULT false,
  paid_at TIMESTAMPTZ,
  payment_provider TEXT CHECK (payment_provider IN ('yookassa', 'stripe')),
  payment_id TEXT,                        -- ID транзакции у провайдера
  amount INT,
  currency TEXT DEFAULT 'RUB',
  UNIQUE (event_id, email)
);

-- Участники чатов (собираются через new_chat_members)
CREATE TABLE chat_members (
  telegram_id BIGINT NOT NULL,
  chat_id BIGINT NOT NULL,
  event_id TEXT REFERENCES events(event_id),
  joined_at TIMESTAMPTZ DEFAULT now(),
  left_at TIMESTAMPTZ,                    -- NULL = ещё в чате
  kicked_at TIMESTAMPTZ,                  -- NULL = не кикали
  PRIMARY KEY (telegram_id, chat_id, event_id)
);

-- Привязка telegram_id ↔ email ↔ ory_id
-- (используется существующая таблица users или расширяется)
-- telegram_id → email: при оплате через бота
-- email → telegram_id: при deeplink после оплаты на сайте
-- telegram_id → ory_id: при /register

-- JWT-доступы к видео (аудит)
CREATE TABLE video_access (
  id SERIAL PRIMARY KEY,
  event_id TEXT REFERENCES events(event_id),
  user_identifier TEXT NOT NULL,          -- ory_id, tg:{id}, или email
  jwt_issued_at TIMESTAMPTZ DEFAULT now(),
  jwt_expires_at TIMESTAMPTZ NOT NULL,
  access_type TEXT CHECK (access_type IN ('permanent', 'temporary'))
);
```

</details>

<details>
<summary><b>5. Матрица доставки</b></summary>

| Оплатил через | Писал боту /start? | Есть telegram_id? | Доставка Zoom | Доставка видео |
|---|---|---|---|---|
| Бота | Да (автоматически) | Да | ЛС бота (мгновенно) | ЛС бота (JWT) |
| Сайт + deeplink | Да (по deeplink) | Да | ЛС бота (мгновенно) | ЛС бота (JWT) |
| Сайт без deeplink, но был в чате | Нет | Да (из chat_members) | Email + mention в чате | Email (JWT 7 дней) |
| Сайт без deeplink, не в чате | Нет | Нет | Email (3-5 сек) | Email (JWT 7 дней) |

**Конверсия в полный доступ:** Временный JWT (7 дней) → /register → Ory identity → постоянный JWT (365 дней).

</details>

<details>
<summary><b>6. Интеграции</b></summary>

### 6.1. Aisystant LMS → Бот (webhook)

**Требуется доработка LMS:** При успешной оплате Aisystant отправляет POST на бот:

```json
POST https://aistmebot-production.up.railway.app/api/payment-webhook
{
  "event": "payment_success",
  "payment_id": "...",
  "product_type": "seminar",
  "product_id": "seminar-2026-04-15",
  "email": "user@example.com",
  "amount": 5000,
  "currency": "RUB",
  "provider": "yookassa",
  "timestamp": "2026-04-15T09:30:00Z"
}
```

**Альтернатива (если webhook невозможен):** Polling — бот проверяет `check_payment()` каждые 30 сек после инициации платежа (до 10 мин). Менее надёжно, задержка до 30 сек.

### 6.2. Kinescope (видеохостинг)

| Параметр | Значение |
|----------|----------|
| JWT API | Генерация персональных ссылок по video_id + claims |
| DRM | Widevine / FairPlay (опционально) |
| CDN | Встроенный (РФ + глобальный) |
| Цена | От ₽3000/мес (100 видео, 1 ТБ) |

### 6.3. Ory (Identity)

Lazy-создание: пользователь регистрируется только когда хочет постоянный доступ к видео.

```
/register → email → magic link → Ory identity создан
  → Привязка: telegram_id ↔ ory_id в Neon
  → Новый JWT с sub: ory_id, exp: +365d
```

</details>

<details>
<summary><b>7. Вопросы для обсуждения с командой</b></summary>

### Блокирующие

1. **Webhook от Aisystant:** Можно ли добавить POST-запрос боту при успешной оплате? Если нет — переходим на polling (задержка до 30 сек).
2. **Kinescope или альтернатива:** Согласовать видеохостинг. Критерии: JWT API, CDN в РФ, DRM, цена.
3. **Zoom: один meeting или персональные ссылки?** При 100+ обычно один meeting (проще). Персональные — безопаснее, но нужен Zoom API.

### Архитектурные

4. **Deeplink-привязка:** Формат `t.me/aist_me_bot?start=sem_{event_id}_{hash}` — hash нужен для безопасности (чтобы нельзя было подделать оплату). Какой алгоритм? HMAC-SHA256 от event_id + email?
5. **Cleanup timing:** 24 часа или 48 часов после семинара? Нужно дать время оплатить запись.
6. **Предупреждение перед cleanup:** За сколько предупреждать? Предложение: за 1 час.
7. **Invite-ссылка:** Отзывать сразу после cleanup или оставить (чтобы оплатившие позже могли войти)?

### Организационные

8. **Кто загружает видео на Kinescope?** Автоматически (Zoom API → Kinescope API) или вручную?
9. **Стоимость:** Kinescope ~₽3000/мес. Stripe комиссия ~2.9% + $0.30. ЮКасса ~2.8%.
10. **Потоки с наставниками:** Тот же паттерн или отдельный сценарий? Ключевое отличие: закрытый чат с join requests вместо открытого.

</details>

<details>
<summary><b>8. Связь с архитектурой (WP-73)</b></summary>

### Затронутые сервисы (MAP.002)

| Сервис | Статус | Что нужно |
|--------|--------|-----------|
| S45: Billing Check | ★ Новый | Проверка оплаты, маппинг продукт → ресурсы |
| S51: Notification Service | ★ Новый | Доставка Zoom-ссылок и видео (ЛС бота + email) |
| S62: Event Access Service | ★ Новый | JWT-генерация для видео, управление доступом |
| Бот: payment handler | Доработка | Webhook приём, fulfillment логика |
| Бот: chat member tracker | ★ Новый | Запись new_chat_members → Neon |
| Бот: cleanup job | ★ Новый | Kick неоплативших по расписанию |
| Aisystant LMS | Доработка | Webhook при успешной оплате |

### Соответствие принципам (DP.ARCH.001 §7)

| Принцип | Соблюдается? | Комментарий |
|---------|:---:|-------------|
| #2 Слабая связанность | ✅ | Бот ↔ Aisystant через webhook. Бот ↔ Kinescope через JWT API |
| #5 Evolvability-first | ✅ | Kinescope заменяем (любой JWT-совместимый хостинг). Zoom заменяем |
| #8 Знания публичны, данные приватны | ✅ | Оплаты и telegram_id — приватные (Neon). Видео — за JWT |
| #13 UI-agnostic | ✅ | Fulfillment работает через бот И email. Не привязан к одному UI |
| #15 Multi-surface | ✅ | Доставка: ЛС бота + email + чат. Видео: web (Kinescope player) |
| #17 Три оси доступа | ✅ | Permission = Entitlement(T2+) ∩ Role(Участник) ∩ Scope(event:sem-X) |
| #20 Integrate SOTA | ✅ | Kinescope, Ory, JWT — готовые решения, не своё |

### Трёхосевая модель (DP.D.034)

```
Участник семинара:
  Entitlement: T2+ (оплативший)
  Role: Участник сообщества
  Scope: event:seminar-{id}

Наставник потока:
  Entitlement: TM2
  Role: Наставник
  Scope: cohort:spring-2026/group:A
```

</details>

---

*Создан: 2026-03-17. Источник: WP-115 + WP-73. Для обсуждения с командой.*
