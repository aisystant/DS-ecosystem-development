---

type: agent-passport
status: active
created: 2025-12-18
layer: architecture
scope: local-edge
family: F8
cell: '3.2'
version: v1.0
description: 'Паспорт ИИ-агента ProgressAnalyst: анализ прогресса и инсайты'
related:
- ИИ-агент RouteGuide 3.2
- Проводник по персональному маршруту 3.2
- Описание цифрового двойника 3.2
---

# Паспорт агента: AGT.ProgressAnalyst

## 0. Назначение документа

Этот документ описывает ИИ-агента `AGT.ProgressAnalyst` — компонент ИИ-ассистента Проводник, отвечающий за анализ прогресса участника и генерацию инсайтов.

---

## 1. Роль

**AGT.ProgressAnalyst** — агент анализа прогресса и генерации инсайтов.

**Миссия:** Превращать данные об активности участника в понятные инсайты, выявлять паттерны успеха и блокеры, помогать Проводнику принимать решения.

**Ключевые задачи:**
- Анализ прогресса по маршруту и метрикам
- Выявление паттернов успеха и проблем
- Обнаружение блокеров и узких мест
- Генерация еженедельных/ежемесячных отчётов
- Подготовка данных для RouteGuide

---

## 2. Входы

### 2.1. Из Цифрового двойника

| Тип данных | Код | Назначение |
|------------|-----|------------|
| История событий | `E.*` | Все активности участника |
| Показатели | `IND.1.*`, `IND.2.*` | Первичные и производные |
| Маршрут и прогресс | `PTH.*` | Что запланировано и выполнено |
| Вехи | `Milestone.*` | Достигнутые и предстоящие |
| Рабочие продукты | `W.*` | Артефакты участника |

### 2.2. Триггеры запуска

| Триггер | Описание |
|---------|----------|
| `analyze_progress` от RouteGuide | Запрос анализа |
| `E.Week.Ended` | Еженедельный анализ |
| `E.Month.Ended` | Ежемесячный анализ |
| `E.Milestone.Approaching` | Анализ перед вехой |
| `E.Anomaly.Detected` | Обнаружена аномалия |

---

## 3. Выходы

### 3.1. Аналитические артефакты

| Артефакт | Код | Описание |
|----------|-----|----------|
| Недельный отчёт | `W.Analytics.WeeklyReport` | Сводка за неделю |
| Анализ прогресса | `W.Analytics.ProgressAnalysis` | Детальный анализ |
| Список блокеров | `W.Analytics.Blockers` | Выявленные препятствия |
| Инсайты | `W.Analytics.Insights` | Паттерны и рекомендации |

### 3.2. Структура недельного отчёта

```json
{
  "period": {"start": "2025-12-09", "end": "2025-12-15"},
  "summary": {
    "slots_planned": 7,
    "slots_completed": 5,
    "hours_total": 8.5,
    "completion_rate": 0.71,
    "streak_days": 12
  },
  "progress": {
    "modules_completed": 2,
    "assignments_done": 5,
    "milestones_reached": 1
  },
  "trends": {
    "regularity": "improving",
    "velocity": "stable",
    "engagement": "high"
  },
  "blockers": [
    {"type": "time_constraint", "description": "Понедельники заняты"}
  ],
  "insights": [
    "Лучшая продуктивность в утренние слоты",
    "Высокая вовлечённость в практические задания"
  ],
  "recommendations": [
    "Перенести понедельничный слот на вторник",
    "Добавить больше практических заданий"
  ]
}
```

### 3.3. Данные для RouteGuide

| Данные | Назначение |
|--------|------------|
| Готовность к переходу ступени | Критерии выполнены? |
| Профиль застревания | Тип проблемы (хаос, тупик, ...) |
| Тренды показателей | Улучшение/ухудшение |
| Рекомендации по корректировке | Что изменить в маршруте |

### 3.4. События

- `guide.analysis.completed` — анализ завершён
- `guide.blocker.detected` — обнаружен блокер
- `guide.insight.generated` — сгенерирован инсайт
- `guide.transition.ready` — готов к переходу ступени

---

## 4. Инструменты

### 4.1. MCP-инструменты

| Инструмент | Назначение |
|------------|------------|
| `TOOL.DBTwin.QueryMetrics` | Получение показателей |
| `TOOL.DBTwin.GetEvents` | История событий |
| `TOOL.Analytics.CalculateTrends` | Расчёт трендов |

### 4.2. ML-модели

| Модель | Назначение |
|--------|------------|
| **Time series forecasting** | Прогноз прогресса |
| **Anomaly detection** | Обнаружение аномалий |
| **Clustering** | Типизация паттернов |

### 4.3. LLM модель

- **Модель:** GPT-4o / Claude 3.5 Sonnet
- **Temperature:** 0.3 (аналитические задачи)
- **Использование:**
  - Генерация текстовых инсайтов
  - Интерпретация паттернов
  - Формулирование рекомендаций

---

## 5. Алгоритмы анализа

### 5.1. Еженедельный анализ

```python
def weekly_analysis(twin_id: str, week_number: int) -> WeeklyReport:
    """
    Еженедельный анализ прогресса.
    """
    # 1. Получить данные за неделю
    events = db_twin.get_events(twin_id, week=week_number)
    metrics = db_twin.get_metrics(twin_id, week=week_number)
    route = db_twin.get_route(twin_id)

    # 2. Рассчитать показатели
    summary = calculate_summary(events, metrics)
    progress = calculate_progress(events, route)
    trends = calculate_trends(metrics, history_weeks=4)

    # 3. Выявить блокеры
    blockers = detect_blockers(events, metrics, route)

    # 4. Сгенерировать инсайты
    insights = generate_insights(summary, trends, blockers)

    # 5. Сформулировать рекомендации
    recommendations = generate_recommendations(insights, route)

    return WeeklyReport(
        twin_id=twin_id,
        week=week_number,
        summary=summary,
        progress=progress,
        trends=trends,
        blockers=blockers,
        insights=insights,
        recommendations=recommendations
    )
```

### 5.2. Обнаружение блокеров

```python
def detect_blockers(events, metrics, route) -> List[Blocker]:
    """
    Выявление блокеров прогресса.
    """
    blockers = []

    # 1. Временные ограничения
    if metrics.get("slots_missed_rate", 0) > 0.3:
        days_with_misses = find_problematic_days(events)
        blockers.append(Blocker(
            type="time_constraint",
            description=f"Регулярные пропуски в дни: {days_with_misses}",
            severity="medium"
        ))

    # 2. Застревание на шаге
    stuck_steps = find_stuck_steps(route, threshold_days=14)
    for step in stuck_steps:
        blockers.append(Blocker(
            type="stuck_on_step",
            description=f"Застревание на шаге: {step.title}",
            step_id=step.id,
            severity="high"
        ))

    # 3. Снижение вовлечённости
    if metrics.get("engagement_trend") == "declining":
        blockers.append(Blocker(
            type="engagement_drop",
            description="Снижение вовлечённости за последние 2 недели",
            severity="medium"
        ))

    # 4. Риск burnout
    if metrics.get("hours_per_week", 0) > 15 and metrics.get("completion_rate", 1) < 0.5:
        blockers.append(Blocker(
            type="burnout_risk",
            description="Высокая нагрузка при низком завершении — риск выгорания",
            severity="high"
        ))

    return blockers
```

### 5.3. Генерация инсайтов

```python
def generate_insights(summary, trends, blockers) -> List[str]:
    """
    Генерация инсайтов на основе данных.
    """
    insights = []

    # 1. Паттерны продуктивности
    if summary.best_time_of_day:
        insights.append(f"Лучшая продуктивность в {summary.best_time_of_day} слоты")

    # 2. Предпочтения по типам заданий
    if summary.preferred_task_type:
        insights.append(f"Высокая вовлечённость в {summary.preferred_task_type} задания")

    # 3. Тренды
    if trends.regularity == "improving":
        insights.append("Регулярность улучшается — ритм укрепляется")
    elif trends.regularity == "declining":
        insights.append("Регулярность снижается — нужно внимание")

    # 4. Достижения
    if summary.streak_days >= 7:
        insights.append(f"Отличная серия: {summary.streak_days} дней подряд!")

    # 5. Готовность к переходу ступени
    if check_transition_ready(summary, trends):
        insights.append("Показатели соответствуют критериям следующей ступени")

    return insights
```

---

## 6. Метрики качества

| Метрика | Описание | Целевое значение |
|---------|----------|------------------|
| **insight_relevance** | Релевантность инсайтов (feedback) | >4.0/5.0 |
| **blocker_detection_rate** | % обнаруженных реальных блокеров | >80% |
| **forecast_accuracy** | Точность прогнозов | >70% |
| **analysis_time** | Время выполнения анализа | <30 сек |
| **report_usefulness** | Полезность отчётов (feedback) | >4.0/5.0 |

---

## 7. Связанные документы

- [[ИИ-агент RouteGuide 3.2]] — использует анализ для решений
- [[ИИ-агент RhythmKeeper 3.2]] — получает алерты об аномалиях
- [[Концепция Проводника (Ассистент Ученика) 3.2]] — Progress Tracker
- [[Описание цифрового двойника 3.2]] — источник данных
- [[Карта ИТ-систем 3.2]] — реестр агентов

---

## 8. История изменений

| Дата | Версия | Описание |
|------|--------|----------|
| 2025-12-18 | v1.0 | Создан паспорт агента |
