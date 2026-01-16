---

type: agent-passport
status: active
created: 2025-12-18
layer: architecture
scope: local-edge
family: F8
cell: '3.2'
version: v1.0
description: 'Паспорт ИИ-агента TrajectoryPlanner: планирование траектории обучения'
related:
- ИИ-агент RouteGuide 3.2
- Проводник по персональному маршруту 3.2
- Описание цифрового двойника 3.2
---

# Паспорт агента: AGT.TrajectoryPlanner

## 0. Назначение документа

Этот документ описывает ИИ-агента `AGT.TrajectoryPlanner` — компонент ИИ-ассистента Проводник, отвечающий за детализацию траектории обучения и оптимизацию пути к целям.

---

## 1. Роль

**AGT.TrajectoryPlanner** — агент планирования траектории обучения.

**Миссия:** Преобразовать стратегический маршрут от `AGT.RouteGuide` в детальный план с учётом зависимостей между навыками, доступного времени и оптимального порядка изучения.

**Ключевые задачи:**
- Декомпозиция маршрута на конкретные шаги (курсы, модули, практики)
- Разрешение зависимостей между навыками (prerequisites)
- Оптимизация последовательности шагов
- Распределение шагов по времени (timeline planning)
- Адаптация плана под изменения

---

## 2. Входы

### 2.1. От агента RouteGuide

| Данные | Описание |
|--------|----------|
| `PTH.Student.PersonalRoute` | Стратегический маршрут развития |
| Целевая ступень | `STG.Student.*` к которой стремимся |
| Критерии перехода | Что нужно достичь для перехода |

### 2.2. Из Цифрового двойника

| Тип данных | Код | Назначение |
|------------|-----|------------|
| Текущие навыки | `IND.2.2.*` | Базовый уровень |
| Доступное время | `SLT.Planned` | Сколько времени в неделю |
| История обучения | `E.LMS.*` | Что уже пройдено |
| Предпочтения | `PRS.Twin.preferences` | Стиль обучения |

### 2.3. Внешние источники

- **Граф навыков** — зависимости между навыками (skill dependency graph)
- **Каталог курсов LMS** — модули, уроки, оценки времени
- **Каталог проектов** — практические кейсы

### 2.4. Триггеры запуска

| Триггер | Описание |
|---------|----------|
| `plan_trajectory` от RouteGuide | Команда на планирование |
| `E.Route.Updated` | Маршрут обновлён |
| `E.Schedule.Changed` | Изменилось доступное время |
| `E.Skill.Acquired` | Освоен новый навык |

---

## 3. Выходы

### 3.1. Артефакты

| Артефакт | Код | Описание |
|----------|-----|----------|
| Детальный план | `W.RouteGuide.TrajectoryPlan` | Список шагов с timeline |
| Граф зависимостей | — | Визуализация пути |
| Оценка времени | — | Сколько займёт достижение цели |

### 3.2. Команды

| Агент | Команда | Описание |
|-------|---------|----------|
| `AGT.DailyAssignmentBuilder` | `build_week_assignments` | План на неделю |
| `AGT.ContentPersonalizer` | `personalize_content` | Адаптировать контент |

### 3.3. События

- `guide.trajectory.planned` — траектория спланирована
- `guide.trajectory.optimized` — траектория оптимизирована
- `guide.dependency.resolved` — зависимости разрешены

---

## 4. Инструменты

### 4.1. MCP-инструменты

| Инструмент | Назначение |
|------------|------------|
| `TOOL.SkillGraph.Query` | Запрос графа зависимостей навыков |
| `TOOL.LMS.GetModules` | Получение модулей курсов |
| `TOOL.DBTwin.QueryMetrics` | Текущий уровень навыков |

### 4.2. Алгоритмы

- **Shortest path** — поиск кратчайшего пути в графе навыков
- **Topological sort** — определение порядка с учётом зависимостей
- **Constraint satisfaction** — учёт ограничений по времени
- **OR-Tools** — оптимизация расписания

### 4.3. LLM модель

- **Модель:** GPT-4o / Claude 3.5 Sonnet
- **Temperature:** 0.2 (детерминированное планирование)
- **Использование:** Генерация объяснений плана, адаптация под контекст

---

## 5. Алгоритм планирования

```python
def plan_trajectory(route: PersonalRoute, twin_context: TwinContext) -> TrajectoryPlan:
    """
    Детализация маршрута в конкретную траекторию обучения.
    """
    # 1. Извлечь целевые навыки из маршрута
    target_skills = route.get_target_skills()
    current_skills = twin_context.get_current_skills()

    # 2. Найти разрыв (skill gap)
    skill_gap = target_skills - current_skills

    # 3. Построить граф зависимостей
    dependency_graph = skill_graph.get_subgraph(skill_gap)

    # 4. Топологическая сортировка — определить порядок
    ordered_skills = topological_sort(dependency_graph)

    # 5. Подобрать ресурсы для каждого навыка
    steps = []
    for skill in ordered_skills:
        resources = find_resources(skill, twin_context.preferences)
        step = TrajectoryStep(
            skill=skill,
            resources=resources,
            estimated_hours=estimate_time(resources),
            prerequisites=[s.id for s in dependency_graph.predecessors(skill)]
        )
        steps.append(step)

    # 6. Распределить по времени
    weekly_hours = twin_context.available_hours_per_week
    timeline = schedule_steps(steps, weekly_hours)

    # 7. Сформировать план
    plan = TrajectoryPlan(
        route_id=route.id,
        steps=steps,
        timeline=timeline,
        total_hours=sum(s.estimated_hours for s in steps),
        estimated_weeks=calculate_weeks(steps, weekly_hours)
    )

    return plan
```

---

## 6. Метрики качества

| Метрика | Описание | Целевое значение |
|---------|----------|------------------|
| **plan_optimality** | Оптимальность пути (vs baseline) | >85% |
| **dependency_violations** | Нарушения зависимостей | 0 |
| **time_accuracy** | Точность оценки времени | ±20% |
| **plan_completion_rate** | % выполненных планов | >70% |
| **replan_frequency** | Частота перепланирования | <2/месяц |

---

## 7. Связанные документы

- [[ИИ-агент RouteGuide 3.2]] — формирование маршрута
- [[ИИ-агент DailyAssignmentBuilder 3.2]] — генерация заданий
- [[Концепция Проводника (Ассистент Ученика) 3.2]] — архитектура
- [[Описание платформы обучения 3.2]] — каталог курсов
- [[Карта ИТ-систем 3.2]] — реестр агентов

---

## 8. История изменений

| Дата | Версия | Описание |
|------|--------|----------|
| 2025-12-18 | v1.0 | Создан паспорт агента |
