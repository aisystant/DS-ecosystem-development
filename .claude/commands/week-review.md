Выполни сценарий Week Review для StrategicPlanner.

Источник сценария: ~/Github/spf-digital-platform-pack/pack/digital-platform/02-domain-entities/DP.AGENT.012-strategic-planner/scenarios/scheduled/03-week-review.md

## Контекст

- Планы: ~/Github/ecosystem-development/0.OPS/0.7.Plans-and-Meetings/
- Шаблон: ~/Github/spf-digital-platform-pack/pack/digital-platform/02-domain-entities/DP.AGENT.012-strategic-planner/templates/reviews/weekly-review.md

## Алгоритм

1. **Сбор данных:**
   - Загрузи weekly-plan.md
   - Загрузи все daily/*.md за неделю
   - Получи коммиты за неделю (git log --since="1 week ago")

2. **Статистика:**
   - РП: запланировано / завершено / %
   - Коммитов всего
   - Активных дней
   - По репозиториям
   - По областям

3. **Инсайты:**
   - Что получилось
   - Что улучшить
   - Блокеры

4. **Формат для клуба:**
   - Используй шаблон weekly-review.md
   - Добавь хештеги

5. **Сохранение:**
   - Создай reviews/weekly/YYYY-WXX.md
   - Закоммить

Результат: итоги недели в формате для публикации в клубе.
