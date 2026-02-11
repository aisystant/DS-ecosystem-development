Выполни сценарий Day Plan для агента Стратег.

Источник сценария: ~/Github/PACK-digital-platform/pack/digital-platform/02-domain-entities/DP.AGENT.012-strategist/scenarios/scheduled/02-day-plan.md

## Контекст

- **HUB (личные планы):** ~/Github/DS-strategy/current/
- **SPOKE (планы репо):** ~/Github/*/WORKPLAN.md
- Шаблоны: ~/Github/PACK-digital-platform/pack/digital-platform/02-domain-entities/DP.AGENT.012-strategist/templates/

## Алгоритм

1. **Апдейт о вчера:**
   - Загрузи план вчера из DS-strategy/current/daily/ (если есть)
   - Получи коммиты за вчера из ВСЕХ репо в ~/Github/
   - Сопоставь РП и коммиты
   - Покажи статистику

2. **Контекст недели:**
   - Найди последний файл недели в DS-strategy/current/weeks/
   - Загрузи его
   - Рассчитай прогресс по неделе

3. **План на сегодня:**
   - Выбери 2-4 РП из недельного плана
   - Учти carry-over со вчера
   - Учти дедлайны из WORKPLAN.md
   - Ограничь по дневному бюджету (4-6h)

4. **Рекомендация:**
   - Предложи с чего начать и почему

5. **Сохранение:**
   - Создай DS-strategy/current/daily/YYYY-MM-DD.md
   - Закоммить в DS-strategy

Результат: план на день с апдейтом о вчера и рекомендацией.
