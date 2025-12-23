---

type: agent-passport
status: active
created: 2025-12-18
layer: architecture
scope: local-edge
family: F8
cell: '3.2'
version: v1.0
description: 'Паспорт ИИ-агента RhythmKeeper: мониторинг ритма и напоминания'
related:
- ИИ-агент RouteGuide 3.2
- Проводник по персональному маршруту 3.2
- Описание цифрового двойника 3.2
---

# Паспорт агента: AGT.RhythmKeeper

## 0. Назначение документа

Этот документ описывает ИИ-агента `AGT.RhythmKeeper` — компонент ИИ-ассистента Проводник, отвечающий за мониторинг ритма саморазвития участника и отправку мягких напоминаний (nudges).

---

## 1. Роль

**AGT.RhythmKeeper** — агент мониторинга ритма и напоминаний.

**Миссия:** Помочь участнику выстроить и удержать устойчивый ритм саморазвития через мягкие, персонализированные напоминания в нужное время.

**Ключевые задачи:**
- Мониторинг регулярности слотов саморазвития
- Выбор оптимального времени для nudges
- Персонализация сообщений под ступень и контекст
- Предупреждение о рисках (burnout, goal drift)
- Празднование достижений

---

## 2. Входы

### 2.1. Из Цифрового двойника

| Тип данных | Код | Назначение |
|------------|-----|------------|
| Паттерны активности | `E.*` последние 4 недели | Когда участник обычно активен |
| Запланированные слоты | `SLT.Planned` | Когда ожидается активность |
| Фактические слоты | `SLT.Actual` | Что реально происходило |
| Индекс регулярности | `IND.2.1.6` | Устойчивость ритма |
| Текущая ступень | `STG.Student.*` | Стиль общения |
| Предпочтения | `PRS.Twin.preferences.notifications` | Каналы и частота |

### 2.2. От других агентов

| Источник | Команда | Описание |
|----------|---------|----------|
| `AGT.RouteGuide` | `set_nudges` | Настройка напоминаний |
| `AGT.ProgressAnalyst` | `alert_anomaly` | Обнаружена аномалия |

### 2.3. Триггеры запуска

| Триггер | Описание |
|---------|----------|
| `E.Slot.Approaching` | Приближается запланированный слот |
| `E.Slot.Missed` | Пропущен слот |
| `E.Milestone.Reached` | Достигнута веха |
| `E.Activity.Declining` | Снижение активности |
| `CRON.Daily` | Ежедневная проверка |

---

## 3. Выходы

### 3.1. Nudges (мягкие напоминания)

| Тип nudge | Когда | Пример |
|-----------|-------|--------|
| **Reminder** | За 15 мин до слота | "Через 15 минут твой слот развития" |
| **Encouragement** | При снижении активности | "Заметил паузу. Всё в порядке?" |
| **Celebration** | При достижении вехи | "Поздравляю! Ты прошёл 4 недели подряд" |
| **Warning** | При риске burnout | "Ты много работал. Может, отдохнуть?" |
| **Opportunity** | Новая возможность | "Открылся новый курс по твоей теме" |

### 3.2. Каналы доставки

| Канал | Приоритет | Когда использовать |
|-------|-----------|-------------------|
| **In-app** | Высокий | Когда участник в системе |
| **Push** | Средний | Для напоминаний |
| **Telegram** | Средний | Быстрая коммуникация |
| **Email** | Низкий | Еженедельные сводки |

### 3.3. События

- `guide.nudge.sent` — nudge отправлен
- `guide.nudge.opened` — nudge прочитан
- `guide.nudge.clicked` — участник отреагировал
- `guide.rhythm.stable` — ритм стабилен
- `guide.rhythm.declining` — ритм снижается

---

## 4. Инструменты

### 4.1. MCP-инструменты

| Инструмент | Назначение |
|------------|------------|
| `TOOL.DBTwin.GetActivityPatterns` | Паттерны активности |
| `TOOL.Notifications.Send` | Отправка уведомлений |
| `TOOL.CRM.GetChannels` | Доступные каналы |

### 4.2. LLM модель

- **Модель:** GPT-4o / Claude 3.5 Sonnet
- **Temperature:** 0.6 (немного вариативности в формулировках)
- **Использование:** Персонализация текста nudges

---

## 5. Алгоритм работы

### 5.1. Мониторинг ритма

```python
def monitor_rhythm(twin_id: str) -> RhythmStatus:
    """
    Ежедневный мониторинг ритма участника.
    """
    # 1. Получить паттерны за 4 недели
    patterns = db_twin.get_activity_patterns(twin_id, weeks=4)

    # 2. Рассчитать показатели
    regularity_index = calculate_regularity(patterns)
    trend = calculate_trend(patterns)  # improving, stable, declining
    streak = calculate_streak(patterns)  # дней подряд

    # 3. Определить статус
    if regularity_index >= 0.8 and trend in ["improving", "stable"]:
        status = RhythmStatus.STABLE
    elif trend == "declining" or regularity_index < 0.3:
        status = RhythmStatus.AT_RISK
    else:
        status = RhythmStatus.BUILDING

    return RhythmStatus(
        status=status,
        regularity_index=regularity_index,
        trend=trend,
        streak=streak,
        recommended_nudges=get_recommended_nudges(status)
    )
```

### 5.2. Генерация nudge

```python
def generate_nudge(twin_id: str, nudge_type: NudgeType) -> Nudge:
    """
    Генерация персонализированного nudge.
    """
    # 1. Получить контекст
    context = db_twin.get_context(twin_id)
    stage = context.current_stage
    preferences = context.preferences.notifications

    # 2. Определить оптимальное время
    best_time = calculate_optimal_time(
        activity_patterns=context.activity_patterns,
        slot_time=context.next_slot_time
    )

    # 3. Выбрать канал
    channel = select_channel(preferences, nudge_type)

    # 4. Сгенерировать текст под ступень
    message = generate_message(
        nudge_type=nudge_type,
        stage=stage,
        context=context,
        tone=preferences.tone  # formal, friendly, minimal
    )

    # 5. Проверить частоту (не спамить)
    if not check_frequency_limit(twin_id, nudge_type):
        return None

    return Nudge(
        twin_id=twin_id,
        type=nudge_type,
        message=message,
        channel=channel,
        scheduled_at=best_time
    )
```

### 5.3. Адаптация под ступень

```python
NUDGE_TEMPLATES = {
    "reminder": {
        StudentStage.RANDOM: "Привет! Есть 15 минут? Давай продолжим.",
        StudentStage.PRACTICING: "Скоро твой слот. Готов?",
        StudentStage.SYSTEMATIC: "Слот через 15 мин. Тема: {topic}.",
        StudentStage.DISCIPLINED: "15:00 — слот саморазвития.",
        StudentStage.PROACTIVE: None  # не нужны напоминания
    },
    "encouragement": {
        StudentStage.RANDOM: "Заметил, что давно не заходил. Всё хорошо? Даже 10 минут — это много.",
        StudentStage.PRACTICING: "Пауза — это нормально. Готов вернуться?",
        StudentStage.SYSTEMATIC: "Сбой ритма. Что помешало? Давай разберёмся.",
        StudentStage.DISCIPLINED: "Заметил паузу. Нужна помощь с перепланированием?",
        StudentStage.PROACTIVE: "Всё в порядке? Напиши, если нужна поддержка."
    }
}
```

---

## 6. Метрики качества

| Метрика | Описание | Целевое значение |
|---------|----------|------------------|
| **nudge_open_rate** | % прочитанных nudges | >50% |
| **nudge_action_rate** | % с действием после nudge | >30% |
| **rhythm_improvement** | Улучшение регулярности после nudges | +15% |
| **opt_out_rate** | % отписок от nudges | <5% |
| **timing_accuracy** | Nudge в нужное время | >80% |

---

## 7. Границы ответственности

### Что делает RhythmKeeper

- Мониторит ритм и отправляет nudges
- Выбирает оптимальное время и канал
- Адаптирует тон под ступень
- Празднует достижения

### Что RhythmKeeper НЕ делает

- НЕ определяет ступень (это RouteGuide)
- НЕ генерирует задания (это DailyAssignmentBuilder)
- НЕ анализирует прогресс (это ProgressAnalyst)
- НЕ ведёт диалог (это Проводник)

---

## 8. Связанные документы

- [[ИИ-агент RouteGuide 3.2]] — формирование маршрута
- [[ИИ-агент ProgressAnalyst 3.2]] — анализ прогресса
- [[Концепция Проводника (Ассистент Ученика) 3.2]] — Nudge Engine
- [[Описание CRM 3.2]] — каналы коммуникации
- [[Карта ИТ-систем 3.2]] — реестр агентов

---

## 9. История изменений

| Дата | Версия | Описание |
|------|--------|----------|
| 2025-12-18 | v1.0 | Создан паспорт агента |
