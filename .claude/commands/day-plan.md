Выполни сценарий Day Plan для StrategicPlanner.

Источник сценария: ~/Github/spf-digital-platform-pack/pack/digital-platform/02-domain-entities/DP.AGENT.012-strategic-planner/scenarios/scheduled/02-day-plan.md

## Контекст

- Планы: ~/Github/ecosystem-development/0.OPS/0.7.Plans-and-Meetings/current/
- Шаблоны: ~/Github/spf-digital-platform-pack/pack/digital-platform/02-domain-entities/DP.AGENT.012-strategic-planner/templates/

## Алгоритм

1. **Апдейт о вчера:**
   - Загрузи план вчера (если есть)
   - Получи коммиты за вчера (git log --since="yesterday" --until="today")
   - Сопоставь РП и коммиты
   - Покажи статистику

2. **Контекст недели:**
   - Загрузи weekly-plan.md
   - Рассчитай прогресс по неделе

3. **План на сегодня:**
   - Выбери 2-4 РП из недельного плана
   - Учти carry-over со вчера
   - Ограничь по дневному бюджету (4-6h)

4. **Рекомендация:**
   - Предложи с чего начать и почему

5. **Сохранение:**
   - Создай daily/YYYY-MM-DD.md
   - Закоммить

Результат: план на день с апдейтом о вчера и рекомендацией.
