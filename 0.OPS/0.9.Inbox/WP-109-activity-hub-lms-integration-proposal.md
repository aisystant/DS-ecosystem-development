---
type: proposal
wp: 109
title: "Activity Hub: интеграция LMS → ЦД + начисление баллов"
status: approved
created: 2026-03-17
author: architect
related:
  - WP-85 (ЦД в Neon — done)
  - WP-109 (Обогащение ЦД данными из IWE)
  - WP-121 (Правила начисления баллов)
---

# Activity Hub: интеграция источников данных в ЦД

> **Статус:** approved (18 мар 2026). Сервисный аккаунт LMS получен. Блокер снят.
> **Зависимости:** WP-85 (ЦД в Neon), WP-121 (баллы за активность).

<details open>
<summary><b>1. Контекст</b></summary>

ЦД получает данные из 4 источников: бот, LMS Aisystant, клуб (Discourse), IWE. Сейчас только бот пишет в `development.user_events` (через `log_event()`). Остальные источники не подключены.

**Зачем:** данные из всех источников нужны для начисления баллов за активность. Баллы = скидки на сервисы платформы = деньги. Поэтому критичны **точность, безопасность и достоверность**.

**Масштаб:** десятки тысяч пользователей.

</details>
<details open>
<summary><b>2. Решение: Activity Hub</b></summary>

**Activity Hub** — отдельная система (`DS-IT-systems/activity-hub/`), единственная точка записи в `development.user_events`. Все источники (включая бот) пишут через Hub.

### Архитектура

```
┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐
│ LMS API  │  │ Club API │  │ IWE files│  │   Бот    │
└────┬─────┘  └────┬─────┘  └────┬─────┘  └────┬─────┘
     │             │             │              │
     ▼             ▼             ▼              ▼
┌─────────┐  ┌─────────┐  ┌─────────┐   ┌──────────┐
│ LMS     │  │ Club    │  │ IWE     │   │ Bot      │
│ Adapter │  │ Adapter │  │ Adapter │   │ Adapter  │
│ (cron)  │  │ (cron)  │  │ (cron)  │   │ (import) │
└────┬─────┘  └────┬────┘  └────┬────┘   └────┬─────┘
     │             │            │              │
     ▼             ▼            ▼              ▼
┌─────────────────────────────────────────────────────┐
│              ACTIVITY HUB CORE                       │
│                                                     │
│  ┌─────────────────┐  ┌──────────────────────────┐  │
│  │ Identity        │  │ Integrity Pipeline       │  │
│  │ Resolver        │  │                          │  │
│  │ ───────────     │  │ 1. Schema validation     │  │
│  │ tg_id      ─┐   │  │ 2. Timestamp sanity      │  │
│  │ lms_user_id ─┼──►│  │ 3. Rate limit check      │  │
│  │ club_id    ─┘   │  │ 4. Dedup (source+ext_id) │  │
│  │ ory_uuid  ◄─────│  │ 5. Write (append-only)   │  │
│  └─────────────────┘  │ 6. Quarantine (rejected) │  │
│                        └──────────────────────────┘  │
│                                                     │
│  ┌──────────────────────────────────────────────┐   │
│  │ Reconciliation Engine (еженедельно)          │   │
│  │ Сверка totals per source. >3% → ALERT +      │   │
│  │ блокировка начисления до ручного разбора     │   │
│  └──────────────────────────────────────────────┘   │
│                                                     │
│  ┌──────────────────────────────────────────────┐   │
│  │ Audit Trail                                   │   │
│  │ Каждый event: source, external_id,            │   │
│  │ ingested_at, adapter_version                  │   │
│  │ Каждый балл → event_id → можно проверить      │   │
│  └──────────────────────────────────────────────┘   │
└──────────────────────────┬──────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────┐
│  Neon: development.user_events (append-only)         │
│  → engagement view → sync_to_dt → digital_twins      │
│  → finance.point_* (начисление баллов) [WP-121]      │
└─────────────────────────────────────────────────────┘
```

### Контракт: Adapter → Hub Core

```python
@dataclass
class RawEvent:
    source: str              # 'lms', 'bot', 'club', 'iwe'
    external_id: str         # уникальный ID из источника
    user_ref: dict           # {'lms_user_id': 123} или {'telegram_id': 456}
    event_type: str          # 'section_completed', 'answer_submitted', ...
    payload: dict            # произвольные данные
    confidence: float        # 0.0–1.0
    occurred_at: datetime    # когда произошло
```

Любой adapter возвращает `List[RawEvent]`. Hub не знает как adapter получил данные (HTTP API, SQL, webhook, файлы). При смене способа получения — меняется только adapter, Hub не меняется.

### Бот: чистовая интеграция

Бот импортирует Hub как библиотеку (не по HTTP → нет потери скорости):

```python
from activity_hub.core import ingest_event

await ingest_event(
    source='bot',
    external_id=f'bot-{event_id}',
    user_ref={'telegram_id': chat_id},
    event_type='ai_chat',
    payload={...},
    confidence=0.8
)
```

Текущий `log_event()` заменяется на `ingest_event()`. Единая точка записи, единая валидация, единый audit trail.

</details>
<details>
<summary><b>3. Фазы реализации и триггеры</b></summary>

### Фаза 0: MVP — Activity Hub + LMS Adapter v1

> **Триггер старта:** согласование этого proposal + получение сервисного аккаунта LMS
> **Длительность:** ~2 недели
> **Масштаб:** <500 активных пользователей LMS

**Что делаем:**
1. Создать репо `DS-IT-systems/activity-hub/` со структурой (adapters/, core/, runner.py)
2. Реализовать Hub Core: identity resolver, normalizer, writer, dedup
3. Реализовать LMS Adapter v1 (HTTP API, батчи по 100 user-ids)
4. Реализовать Bot Adapter (библиотека, замена `log_event()`)
5. Добавить `external_id` + unique index в `development.user_events`
6. Добавить `development.quarantined_events` и `development.sync_log`
7. Cron: ежедневный sync 04:00 MSK, retry 04:15/04:30 при ошибке
8. Reconciliation: еженедельная сверка totals

**Ключевые эндпоинты LMS API (уже существуют):**

| Эндпоинт | Что забираем |
|----------|-------------|
| `GET /courses/passing-actions?from=&to=&user-ids=` | Все действия пользователей за период |
| `GET /courses/courses-passing/progress` | Прогресс по курсам |
| `GET /courses/progress?user-ids=` | Прогресс по списку пользователей |
| `GET /profile/qualification-level` | Квалификация (для multiplier баллов) |
| `GET /api/gaming/learning-session-time` | Время прохождения |
| `GET /api/gaming/symbol-count?from=&to=` | Объём текстов |
| `GET /api/gaming/rewards` | Награды |
| `GET /profile/find-by-tg?tg-id=&s=` | Маппинг Telegram → LMS user |

**Redundancy:**
- 7-day window при каждом sync (overlap ловит пропуски)
- Idempotent writes: ON CONFLICT (source, external_id) DO NOTHING
- 3 попытки (04:00, 04:15, 04:30), при полном fail → alert + блокировка начисления

### Фаза 1: Scale — Bulk API

> **Триггер:** количество активных пользователей LMS > 500 ИЛИ sync > 5 минут
> **Что меняется:** только файл `adapters/lms.py`

**Что нужно от LMS-команды:**
- Новый эндпоинт: `GET /api/export/passing-actions?from=&to=` — все пользователи за период, без фильтра по user-ids
- Формат: NDJSON (streaming, по одной строке на событие)
- Один SQL-запрос с индексом по timestamp на стороне LMS

**Что НЕ меняется:** Hub Core, Neon-схема, бот, reconciliation, начисление баллов.

### Фаза 2: Production — Webhooks (Push)

> **Триггер:** количество активных пользователей LMS > 10 000 ИЛИ Bulk API становится узким местом ИЛИ нужен real-time
> **Вариант DB View убран** — невозможно без логики приложения (подтверждено разработчиком LMS 18 мар).

**Webhooks (LMS Push):**
- LMS при каждом действии шлёт POST на URL Hub API
- Real-time, нет batch-нагрузки
- Требует: endpoint на нашей стороне + webhook sender в LMS
- Разработчик LMS подтвердил возможность реализации

**Что НЕ меняется:** Hub Core, Neon-схема, бот, reconciliation, начисление баллов. Только `adapters/lms.py`.

### Фаза 3: IWE + Клуб (обновлено 19 мар 2026)

> **Триггер:** Фаза 0 в production + данные IWE/клуба нужны для ЦД
> **Scope:** для ВСЕХ пользователей IWE, тестируем на Tseren первым
> **Что делаем:** добавляем `adapters/iwe.py` и `adapters/club.py`
> **Принцип:** Activity Hub записывает факт состоявшегося события. Баллы = WP-121 (отдельно)

**IWE-адаптер** (`adapters/iwe.py`) — cron-скрипт, ежедневно собирает факты из IWE пользователя:

| event_type | Факт | Источник | confidence |
|------------|------|---------|-----------|
| `day_open` | DayPlan создан | git log | 1.0 |
| `day_close` | День закрыт | git log | 1.0 |
| `week_plan_created` | WeekPlan создан | git log | 1.0 |
| `note_to_capture` | Заметка → capture (конверсия) | git diff captures.md | 0.9 |
| `coding_time` | Время в VS Code | WakaTime API | 1.0 |
| `commit_created` | Коммит | git log по всем репо | 1.0 |
| `wp_completed` | РП закрыт | git diff WP-REGISTRY | 1.0 |
| `content_published` | Публикация | git log DS-Knowledge-Index | 0.9 |
| `knowledge_extracted` | KE в Pack | git log PACK-* | 1.0 |
| `distinction_added` | Различение добавлено | git diff hard-distinctions | 0.9 |
| `method_described` | Метод описан | git log PACK-*/06-methods/ | 0.9 |
| `fmt_commit_merged` | Одобренный коммит в FMT | GitHub API: merged PR | 1.0 |

**Клуб (Discourse):** `GET /user_actions.json`, `GET /directory_items.json`. Dep: DE-36 для Ory-интеграции.

| event_type | Факт | confidence |
|------------|------|-----------|
| `community_help` | Ответ на чужую тему | 0.9 |
| `post_created` | Тема/пост создан | 1.0 |
| `like_given` | Лайк | 1.0 |

</details>
<details>
<summary><b>4. Что нужно от разработчика LMS (для старта Фазы 0)</b></summary>

### Обязательно

1. ✅ **Сервисный аккаунт:** tech2@aisystant.com, Basic Authorization. Только тестовый сервер. Переход на JWT от Ory — когда Ory будет готов.

2. ✅ **Доступ к эндпоинтам** подтверждён. Ограничить только GET сложно на стороне LMS, но мы гарантируем только чтение.

3. ✅ **Dedup key:** `(actionType, actionId)` — actionId уникален в рамках одного actionType. Используем `f"{actionType}:{actionId}"` как external_id.

4. ✅ **Тестовый сервер** (188.73.162.175:8064) доступен. Не 100% uptime (разработка, обновления). Дамп с прода — по потребности.

### На перспективу (не сейчас)

5. **Фаза 1 (>500 users):** Bulk-эндпоинт — возможно, сначала проверят обычный JSON vs NDJSON.

6. **Фаза 2 (>10K users):** Webhook sender (push-модель) — возможно. Read-only VIEW невозможно (убран из планов).

### Гарантии с нашей стороны

- Только GET-запросы (чтение), данные в LMS НЕ изменяем
- 1 batch в день (04:00 MSK), не чаще
- Не храним пароли пользователей LMS (только сервисный аккаунт)
- Connection string к нашей БД НЕ даём и НЕ просим — каждая система отвечает за свои данные

</details>
<details>
<summary><b>5. Достоверность и безопасность (Integrity Pipeline)</b></summary>

Баллы = скидки = деньги. Hub гарантирует:

| Этап | Что проверяется | При ошибке |
|------|----------------|-----------|
| **Schema validation** | event_type ∈ known_types, confidence 0.0–1.0 | → quarantine |
| **Timestamp sanity** | Не из будущего, не старше 30 дней | → quarantine |
| **Rate limit** | >100 events/user/day | → flag + alert |
| **User exists** | user_uuid найден в public.users | → quarantine |
| **Dedup** | (source, external_id) уникален | → skip (idempotent) |
| **Reconciliation** | LMS totals vs COUNT(source='lms') | >3% → ALERT + блокировка начисления |
| **Audit trail** | Каждый балл → event_id → source + external_id | Всегда можно ответить: «откуда эти баллы?» |

### Новые таблицы Neon

```sql
-- Расширение user_events
ALTER TABLE development.user_events ADD COLUMN external_id TEXT;
ALTER TABLE development.user_events ADD COLUMN ingested_at TIMESTAMPTZ DEFAULT NOW();
CREATE UNIQUE INDEX idx_events_source_external
  ON development.user_events (source, external_id)
  WHERE external_id IS NOT NULL;

-- Карантин
CREATE TABLE development.quarantined_events (
    id BIGSERIAL PRIMARY KEY,
    source TEXT NOT NULL,
    external_id TEXT,
    user_ref JSONB,
    event_type TEXT,
    payload JSONB,
    reason TEXT NOT NULL,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Лог синхронизации
CREATE TABLE development.sync_log (
    id BIGSERIAL PRIMARY KEY,
    source TEXT NOT NULL,
    started_at TIMESTAMPTZ,
    finished_at TIMESTAMPTZ,
    events_fetched INTEGER,
    events_written INTEGER,
    events_skipped INTEGER,
    events_quarantined INTEGER,
    status TEXT,        -- 'success', 'partial', 'failed'
    error_message TEXT,
    reconciliation JSONB
);
```

</details>
<details>
<summary><b>6. АрхГейт (ЭМОГССБ)</b></summary>

| Характеристика | Оценка | Обоснование |
|----------------|--------|-------------|
| Эволюционируемость | 9 | Новый источник = новый adapter (один файл). Смена способа получения (API→SQL→webhook) = замена adapter, Hub не меняется |
| Масштабируемость | 9 | Фаза 0: <500 users. Фаза 1: bulk API, <10K. Фаза 2: DB view/webhooks, 50K+. Переход между фазами — без переделок |
| Обучаемость | 8 | Adapter pattern, единый контракт RawEvent, три таблицы |
| Генеративность | 9 | Единый event store → любые проекции, A/B-тестирование правил, ретроспективный replay |
| Скорость | 8 | Бот: import (0ms overhead). Внешние: batch 04:00 (<5 мин при Фаза 0) |
| Современность | 9 | Event Sourcing, Adapter Pattern, Idempotent ETL, Reconciliation. Без overengineering (нет Kafka при 1K events/day) |
| Безопасность | 9 | Integrity Pipeline (6 этапов), RLS, audit trail, quarantine, блокировка начисления при расхождении |
| **Сумма** | **61/70 (8.7)** | **Проходит (порог ≥8)** |

</details>
<details>
<summary><b>7. С чего начинаем</b></summary>

**Шаг 1 (сейчас):** Согласовать этот proposal.

**Шаг 2:** Отправить запрос разработчику LMS (§4 — обязательные пункты 1-4).

**Шаг 3:** Пока ждём аккаунт — создать репо `activity-hub/`, реализовать Hub Core + Bot Adapter. Бот переключается на `ingest_event()`.

**Шаг 4:** Получили аккаунт → реализовать LMS Adapter v1, тестировать на `188.73.162.175:8064`.

**Шаг 5:** Запуск в production. Мониторинг sync_log. Reconciliation.

**Шаг 6:** WP-121 — правила начисления баллов (отдельный РП, после Шага 5).

</details>
<details>
<summary><b>8. Вопросы для согласования</b></summary>

1. Согласуете Activity Hub как отдельную систему (`DS-IT-systems/activity-hub/`)?
2. Согласуете переключение бота с `log_event()` на `ingest_event()` через Hub?
3. Текст для разработчика LMS (§4) — корректировки нужны?
4. Приоритет: начинаем с Фазы 0 на этой/следующей неделе?

</details>

*Создан: 2026-03-17. Автор: Architect (Claude Opus). РП: WP-109, WP-121.*
