Выполни сценарий Strategy Session для StrategicPlanner.

Источник сценария: ~/Github/spf-digital-platform-pack/pack/digital-platform/02-domain-entities/DP.AGENT.012-strategic-planner/scenarios/scheduled/01-strategy-session.md

## Контекст

- Планы: ~/Github/ecosystem-development/0.OPS/0.7.Plans-and-Meetings/current/
- Шаблоны: ~/Github/spf-digital-platform-pack/pack/digital-platform/02-domain-entities/DP.AGENT.012-strategic-planner/templates/

## Алгоритм

1. **Анализ прошлой недели:**
   - Загрузи текущий weekly-plan.md
   - Получи коммиты за прошлую неделю (git log --since="1 week ago")
   - Рассчитай completion rate

2. **Сдвиг месячного окна:**
   - Загрузи monthly-priorities.md
   - Предложи обновления

3. **План на неделю:**
   - Выбери РП из месячных приоритетов
   - Сформируй таблицу с бюджетом

4. **Запрос на подтверждение:**
   - Покажи итоги прошлой недели
   - Покажи предложение плана
   - Спроси о корректировках

5. **После подтверждения:**
   - Сохрани новый weekly-plan.md
   - Обнови monthly-priorities.md
   - Закоммить изменения
   - Выполни /day-plan для сегодня

Результат: обновлённый план недели и месячные приоритеты.
