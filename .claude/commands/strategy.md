Выполни сценарий Strategy Session для агента Стратег.

Источник сценария: ~/IWE/PACK-digital-platform/pack/digital-platform/02-domain-entities/DP.AGENT.012-strategist/scenarios/scheduled/01-strategy-session.md

## Контекст

- **HUB (личные планы):** ~/IWE/DS-strategy/current/
- **SPOKE (планы репо):** ~/IWE/*/WORKPLAN.md
- **Неудовлетворённости:** ~/IWE/DS-strategy/dissatisfactions/current.md
- Шаблоны: ~/IWE/PACK-digital-platform/pack/digital-platform/02-domain-entities/DP.AGENT.012-strategist/templates/

## Структура current/

Недельные планы: `current/weeks/YYYY-MM-DD--DD.md` (один файл на неделю).
Приоритеты месяца включены в файл недели (секция "Приоритеты месяца").
Новые недели — сверху (сортировка по дате, от новых к старым).

## Алгоритм

1. **Анализ прошлой недели:**
   - Найди последний файл недели в DS-strategy/current/weeks/
   - Загрузи его
   - Получи коммиты за прошлую неделю из ВСЕХ репо в ~/IWE/
   - Рассчитай completion rate

2. **Обход WORKPLAN.md (Hub-and-Spoke):**
   - Прочитай ~/IWE/*/WORKPLAN.md из каждого репо
   - Собери все РП со статусом pending/in-progress
   - Выяви расхождения с HUB-планом

3. **Сдвиг месячного окна:**
   - Приоритеты месяца — в секции файла прошлой недели
   - Учти неудовлетворённости из dissatisfactions/current.md
   - Предложи обновления

4. **План на неделю:**
   - Выбери РП из месячных приоритетов + WORKPLAN.md
   - Сформируй таблицу с бюджетом

5. **Запрос на подтверждение:**
   - Покажи итоги прошлой недели
   - Покажи предложение плана
   - Спроси о корректировках

6. **После подтверждения:**
   - Создай current/weeks/YYYY-MM-DD--DD.md
   - Обнови WORKPLAN.md в целевых репо (обратная синхронизация)
   - Закоммить изменения в DS-strategy
   - Закоммить изменения в затронутых репо
   - Зафиксируй сессию в DS-strategy/sessions/YYYY-MM-DD.md

Результат: новый файл недели в current/weeks/, синхронизированные WORKPLAN.md.
