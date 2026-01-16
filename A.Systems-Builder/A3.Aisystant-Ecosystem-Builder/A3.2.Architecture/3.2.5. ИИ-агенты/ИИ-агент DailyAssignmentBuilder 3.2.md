---

type: agent-passport
status: active
created: 2025-12-18
layer: architecture
scope: local-edge
family: F8
cell: '3.2'
version: v1.0
description: 'Паспорт ИИ-агента DailyAssignmentBuilder: генерация ежедневных заданий'
related:
- ИИ-агент RouteGuide 3.2
- ИИ-агент TrajectoryPlanner 3.2
- Проводник по персональному маршруту 3.2
---

# Паспорт агента: AGT.DailyAssignmentBuilder

## 0. Назначение документа

Этот документ описывает ИИ-агента `AGT.DailyAssignmentBuilder` — компонент ИИ-ассистента Проводник, отвечающий за генерацию конкретных заданий на день с учётом контекста участника.

---

## 1. Роль

**AGT.DailyAssignmentBuilder** — агент генерации ежедневных заданий.

**Миссия:** Превращать траекторию обучения в конкретные, выполнимые задания на каждый день, адаптированные под текущий контекст, энергию и доступное время участника.

**Ключевые задачи:**
- Выбор следующего лучшего действия (Next Best Action)
- Генерация заданий с учётом времени суток и энергии
- Адаптация сложности под текущее состояние
- Формулирование заданий понятным языком

---

## 2. Входы

### 2.1. От других агентов

| Источник | Данные | Описание |
|----------|--------|----------|
| `AGT.TrajectoryPlanner` | `TrajectoryPlan` | Детальный план обучения |
| `AGT.RouteGuide` | `build_assignments` | Команда на генерацию |

### 2.2. Из Цифрового двойника

| Тип данных | Код | Назначение |
|------------|-----|------------|
| Текущий прогресс | `E.LMS.SectionCompleted` | Что уже сделано |
| Запланированный слот | `SLT.Planned` | Сколько времени сегодня |
| Уровень энергии | `IND.2.*.energy` | Состояние участника |
| Последняя активность | `E.*` последние | Контекст |
| Текущая ступень | `STG.Student.*` | Сложность заданий |

### 2.3. Триггеры запуска

| Триггер | Описание |
|---------|----------|
| `E.Day.Started` | Начало нового дня |
| `E.Session.Started` | Участник начал сессию |
| `E.Slot.Approaching` | Приближается запланированный слот |
| `build_assignments` | Команда от RouteGuide |

---

## 3. Выходы

### 3.1. Артефакты

| Артефакт | Код | Описание |
|----------|-----|----------|
| Задание дня | `W.RouteGuide.DailyAssignment` | Конкретное задание |
| Список рекомендаций | `W.RouteGuide.Recommendations` | Top-3 действия |
| Обоснование | — | Почему именно это задание |

### 3.2. Структура задания

```json
{
  "id": "assignment_uuid",
  "type": "learning|practice|project|social|reflection|rest",
  "title": "Прочитать раздел 3.2 о системном мышлении",
  "description": "Сегодня фокус на понятии системы...",
  "estimated_minutes": 20,
  "resource": {
    "type": "lms_module",
    "id": "module_123",
    "url": "/courses/systemic/3.2"
  },
  "reasoning": "Это следующий шаг по твоему маршруту...",
  "follow_up": "После прочтения напиши короткую рефлексию"
}
```

### 3.3. События

- `guide.assignment.generated` — задание сгенерировано
- `guide.assignment.accepted` — задание принято
- `guide.assignment.completed` — задание выполнено
- `guide.assignment.skipped` — задание пропущено

---

## 4. Инструменты

### 4.1. MCP-инструменты

| Инструмент | Назначение |
|------------|------------|
| `TOOL.DBTwin.GetContext` | Текущий контекст участника |
| `TOOL.LMS.GetNextContent` | Следующий контент по плану |
| `TOOL.DBTwin.WriteAssignment` | Запись задания |

### 4.2. LLM модель

- **Модель:** GPT-4o / Claude 3.5 Sonnet
- **Temperature:** 0.5 (баланс креативности и релевантности)
- **Использование:**
  - Генерация понятных формулировок
  - Адаптация языка под ступень
  - Создание обоснований

---

## 5. Алгоритм генерации

```python
def build_daily_assignment(twin_id: str, trajectory: TrajectoryPlan) -> DailyAssignment:
    """
    Генерация задания на день.
    """
    # 1. Получить контекст
    context = db_twin.get_context(twin_id)
    stage = context.current_stage
    available_minutes = context.today_slot_minutes
    energy_level = context.energy_level

    # 2. Определить кандидатов из траектории
    candidates = trajectory.get_pending_steps()

    # 3. Оценить каждого кандидата
    scores = []
    for step in candidates:
        score = calculate_score(
            step=step,
            context=context,
            weights={
                "relevance": 0.4,
                "timing_fit": 0.2,
                "energy_fit": 0.2,
                "momentum": 0.2
            }
        )
        scores.append((step, score))

    # 4. Выбрать лучшего с учётом explore-exploit
    selected_step = select_with_exploration(scores, exploration_rate=0.1)

    # 5. Адаптировать под доступное время
    assignment = adapt_to_time(selected_step, available_minutes)

    # 6. Сгенерировать формулировку под ступень
    assignment.title = generate_title(assignment, stage)
    assignment.description = generate_description(assignment, stage)
    assignment.reasoning = generate_reasoning(assignment, context)

    # 7. Записать и вернуть
    db_twin.write_assignment(twin_id, assignment)
    return assignment

def calculate_score(step, context, weights):
    """
    Оценка кандидата по критериям.
    """
    return (
        relevance(step, context.goals) * weights["relevance"] +
        timing_fit(step, context.time_of_day) * weights["timing_fit"] +
        energy_fit(step, context.energy_level) * weights["energy_fit"] +
        momentum(step, context.recent_activities) * weights["momentum"]
    )
```

---

## 6. Адаптация языка по ступеням

| Ступень | Стиль формулировок | Пример |
|---------|-------------------|--------|
| **Random, Practicing** | Бытовой, простой | "Удели 15 минут чтению. Просто открой и начни." |
| **Systematic** | Чёткий, структурированный | "Слот 1: прочитай раздел 3.2 (20 мин). Слот 2: сделай заметку." |
| **Disciplined, Proactive** | Методический, глубокий | "Исследуй связь системного мышления с твоим проектом X." |

---

## 7. Метрики качества

| Метрика | Описание | Целевое значение |
|---------|----------|------------------|
| **assignment_acceptance_rate** | % принятых заданий | >70% |
| **assignment_completion_rate** | % выполненных заданий | >60% |
| **time_estimation_accuracy** | Точность оценки времени | ±30% |
| **feedback_score** | Оценка полезности (1-5) | >4.0 |
| **generation_time** | Время генерации | <5 сек |

---

## 8. Связанные документы

- [[ИИ-агент RouteGuide 3.2]] — формирование маршрута
- [[ИИ-агент TrajectoryPlanner 3.2]] — планирование траектории
- [[ИИ-агент RhythmKeeper 3.2]] — напоминания
- [[Концепция Проводника (Ассистент Ученика) 3.2]] — архитектура
- [[Описание ИИ-ассистента Проводник (Ассистент Ученика) 3.2]] — ступени
- [[Карта ИТ-систем 3.2]] — реестр агентов

---

## 9. История изменений

| Дата | Версия | Описание |
|------|--------|----------|
| 2025-12-18 | v1.0 | Создан паспорт агента |
