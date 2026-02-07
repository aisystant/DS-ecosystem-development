Выполни сценарий Check Plan для StrategicPlanner.

Источник сценария: ~/Github/spf-digital-platform-pack/pack/digital-platform/02-domain-entities/DP.AGENT.012-strategic-planner/scenarios/on-demand/02-check-plan.md

## Задача для проверки: $ARGUMENTS

## Контекст

- Планы: ~/Github/ecosystem-development/0.OPS/0.7.Plans-and-Meetings/current/

## Алгоритм

1. **Анализ задачи:**
   - Что нужно сделать?
   - Оценка бюджета времени
   - Определи область/репозиторий

2. **Сверка с планом:**
   - Загрузи daily plan, weekly plan, monthly priorities
   - Есть ли эта задача в плане?
   - Соответствует ли приоритетам?

3. **Классификация:**
   - `in-plan` — уже в плане
   - `aligned` — соответствует приоритетам
   - `unplanned` — не в приоритетах
   - `urgent` — срочно

4. **Рекомендация:**
   - in-plan → покажи где, предложи начать
   - aligned → предложи добавить в план
   - unplanned → предупреди о смене фокуса
   - urgent → предложи обновить приоритеты

Результат: рекомендация как поступить с задачей.
