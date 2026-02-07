Выполни сценарий Evening Review для StrategicPlanner.

Источник сценария: ~/Github/spf-digital-platform-pack/pack/digital-platform/02-domain-entities/DP.AGENT.012-strategic-planner/scenarios/on-demand/01-evening-review.md

## Контекст

- Планы: ~/Github/ecosystem-development/0.OPS/0.7.Plans-and-Meetings/current/

## Алгоритм

1. **Сбор данных:**
   - Загрузи план на сегодня
   - Получи коммиты за сегодня (git log --since="today")

2. **Сопоставление:**
   - Сравни запланированные РП с коммитами
   - Отметь статусы: done, partial, not started

3. **Статистика:**
   - Запланировано: X РП
   - Завершено: Y РП
   - Коммитов: Z

4. **Carry-over:**
   - Отметь что переносится на завтра

5. **Обновление:**
   - Обнови статусы в плане дня
   - Закоммить

Результат: итоги дня с обновлёнными статусами.
