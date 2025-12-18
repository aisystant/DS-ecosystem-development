---

type: agent-passport
status: active
created: 2025-12-18
layer: architecture
scope: local-edge
family: F8
cell: '3.2'
version: v1.0
description: 'Паспорт ИИ-агента RouteGuide: формирование персонального маршрута развития'
related:
- Проводник по персональному маршруту 3.2
- Описание цифрового двойника 3.2
- ИИ-агент TrajectoryPlanner 3.2
- ИИ-агент DailyAssignmentBuilder 3.2
---

# Паспорт агента: AGT.RouteGuide

## 0. Назначение документа

Этот документ описывает ИИ-агента `AGT.RouteGuide` — ключевой компонент ИИ-ассистента Проводник (Ассистент Ученика), отвечающий за формирование и корректировку персонального маршрута развития.

---

## 1. Роль

**AGT.RouteGuide** — агент формирования персонального маршрута развития участника.

**Миссия:** Превращать размытые намерения человека в конкретный, измеримый, адаптивный план действий по саморазвитию.

**Ключевые задачи:**
- Диагностика текущей ступени роли Ученика (`STG.Student.*`)
- Формирование персонального маршрута (`PTH.Student.PersonalRoute`)
- Корректировка маршрута при изменении обстоятельств
- Передача задач агентам `AGT.TrajectoryPlanner` и `AGT.DailyAssignmentBuilder`

**Взаимодействие с Проводником:**
- RouteGuide — это "мозг" Проводника, отвечающий за стратегию развития
- Проводник (ИИ-ассистент) использует RouteGuide для построения диалога с человеком

---

## 2. Входы

### 2.1. Данные из Цифрового двойника

| Тип данных | Код | Назначение |
|------------|-----|------------|
| Профиль участника | `PRS.Twin` | Цели, предпочтения, контекст |
| Текущая ступень | `STG.Student.*` | Определение уровня |
| Показатели регулярности | `IND.2.1.*` | Часы/неделю, индекс регулярности |
| Показатели мастерства | `IND.2.2.*` | Прогресс по навыкам |
| История слотов | `SLT.*` | Паттерны активности |
| Рабочие продукты | `W.*` | Достижения участника |

### 2.2. Внешние данные

- **Методика ступеней** — описания `STG.Student.Random` → `STG.Student.Proactive`
- **Каталог курсов** из LMS — доступные модули и уроки
- **Каталог проектов** из Case Management — доступные кейсы
- **Запросы человека** — через интерфейс Проводника

### 2.3. Триггеры запуска

| Триггер | Описание |
|---------|----------|
| `E.Session.Started` | Человек начал сессию с Проводником |
| `E.Stage.TransitionRequested` | Запрос на переход между ступенями |
| `E.Route.ReplanRequested` | Запрос на перепланировку маршрута |
| `E.Weekly.ReviewDue` | Плановый еженедельный ревью |
| `E.Activity.Anomaly` | Обнаружена аномалия в активности |

---

## 3. Выходы

### 3.1. Записи в Цифровой двойник

| Артефакт | Код | Описание |
|----------|-----|----------|
| Оценка ступени | `STGA.StudentStageAssigned` | Присвоение/подтверждение ступени |
| Персональный маршрут | `PTH.Student.PersonalRoute` | Структурированный план развития |
| Рекомендации | `W.RouteGuide.Recommendations` | Список рекомендованных действий |

### 3.2. Команды другим агентам

| Агент | Команда | Описание |
|-------|---------|----------|
| `AGT.TrajectoryPlanner` | `plan_trajectory` | Детализировать маршрут на период |
| `AGT.DailyAssignmentBuilder` | `build_assignments` | Сформировать задания дня |
| `AGT.RhythmKeeper` | `set_nudges` | Настроить напоминания |
| `AGT.ProgressAnalyst` | `analyze_progress` | Запросить анализ прогресса |

### 3.3. События

- `guide.route.created` — маршрут создан
- `guide.route.updated` — маршрут обновлён
- `guide.stage.evaluated` — ступень оценена
- `guide.stage.transitioned` — переход на новую ступень

---

## 4. Инструменты

### 4.1. MCP-инструменты

| Инструмент | Назначение |
|------------|------------|
| `TOOL.DBTwin.GetContext` | Получение полного контекста участника |
| `TOOL.DBTwin.QueryMetrics` | Чтение показателей `IND.*`, `MET.*` |
| `TOOL.DBTwin.UpdateStage` | Обновление ступени `STG.Student.*` |
| `TOOL.LMS.GetCourses` | Получение каталога курсов |
| `TOOL.Cases.GetProjects` | Получение каталога проектов |

### 4.2. LLM модель и параметры

- **Модель:** GPT-4o / Claude 3.5 Sonnet
- **Temperature:** 0.3 (консервативная генерация для стратегических решений)
- **Max tokens:** 4000
- **System prompt:** Содержит методику ступеней, критерии переходов, стратегии общения

### 4.3. Внешние сервисы

- **ОС ИИ-платформы** — для оркестрации вызовов
- **Activity Hub** — для логирования событий

---

## 5. Алгоритмы

### 5.1. Диагностика ступени Ученика

```python
def diagnose_student_stage(twin_id: str) -> StudentStage:
    """
    Диагностика текущей ступени роли Ученика.
    """
    # 1. Получить показатели за 4-8 недель
    metrics = db_twin.query_metrics(
        twin_id=twin_id,
        codes=["IND.2.1.*", "IND.2.2.*"],
        period_weeks=8
    )

    # 2. Проверить критерии каждой ступени
    regularity_index = metrics.get("IND.2.1.6", 0)
    hours_per_week = metrics.get("IND.2.1.1", 0)
    stability_weeks = calculate_stability(metrics)

    # 3. Определить ступень
    if regularity_index < 0.3:
        return StudentStage.RANDOM
    elif stability_weeks < 4:
        return StudentStage.PRACTICING
    elif hours_per_week < 10 or stability_weeks < 12:
        return StudentStage.SYSTEMATIC
    elif not has_proactive_indicators(metrics):
        return StudentStage.DISCIPLINED
    else:
        return StudentStage.PROACTIVE
```

### 5.2. Формирование маршрута

```python
def create_personal_route(twin_id: str, stage: StudentStage) -> PersonalRoute:
    """
    Создание персонального маршрута развития.
    """
    # 1. Определить профиль застревания (для Random)
    if stage == StudentStage.RANDOM:
        stuck_profile = diagnose_stuck_profile(twin_id)
        return create_unstuck_route(stuck_profile)

    # 2. Определить цели перехода на следующую ступень
    transition_criteria = get_transition_criteria(stage)

    # 3. Подобрать ресурсы (курсы, проекты)
    resources = match_resources(twin_id, transition_criteria)

    # 4. Сформировать маршрут
    route = PersonalRoute(
        twin_id=twin_id,
        current_stage=stage,
        target_stage=stage.next(),
        milestones=create_milestones(transition_criteria),
        steps=create_steps(resources),
        timeline=estimate_timeline(stage)
    )

    # 5. Записать в цифровой двойник
    db_twin.write_route(route)

    return route
```

---

## 6. Метрики качества

| Метрика | Описание | Целевое значение |
|---------|----------|------------------|
| **stage_accuracy** | Точность диагностики ступени | >90% |
| **route_acceptance_rate** | % маршрутов, принятых участником | >80% |
| **transition_success_rate** | % успешных переходов между ступенями | >70% |
| **time_to_route** | Время формирования маршрута | <30 сек |
| **route_relevance** | Оценка релевантности (feedback) | >4.0/5.0 |

---

## 7. Границы ответственности

### Что делает RouteGuide

- Диагностирует ступень и формирует стратегию развития
- Определяет критерии перехода между ступенями
- Координирует работу других агентов группы "Обучение и развитие"
- Записывает стратегические решения в цифровой двойник

### Что RouteGuide НЕ делает

- НЕ генерирует конкретные задания дня (это `AGT.DailyAssignmentBuilder`)
- НЕ детализирует траекторию (это `AGT.TrajectoryPlanner`)
- НЕ отправляет напоминания (это `AGT.RhythmKeeper`)
- НЕ ведёт диалог напрямую с человеком (это ИИ-ассистент Проводник)

---

## 8. Связанные документы

- [[Описание ИИ-ассистента Проводник (Ассистент Ученика) 3.2]] — методология ступеней
- [[Концепция Проводника (Ассистент Ученика) 3.2]] — техническая архитектура
- [[Описание цифрового двойника 3.2]] — модель данных
- [[ИИ-агент TrajectoryPlanner 3.2]] — детализация траекторий
- [[ИИ-агент DailyAssignmentBuilder 3.2]] — генерация заданий
- [[ИИ-агент RhythmKeeper 3.2]] — мониторинг ритма
- [[Карта ИТ-систем 3.2]] — реестр всех агентов

---

## 9. История изменений

| Дата | Версия | Описание |
|------|--------|----------|
| 2025-12-18 | v1.0 | Создан паспорт агента на основе архитектуры Проводника |
