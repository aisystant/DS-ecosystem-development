Выполни сценарий Evening Review для Strategist.

Источник сценария: ~/Github/PACK-digital-platform/pack/digital-platform/02-domain-entities/DP.AGENT.012-strategist/scenarios/on-demand/01-evening-review.md

## Контекст

- Планы: ~/Github/DS-ops/0.OPS/0.7.Plans-and-Meetings/current/

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
