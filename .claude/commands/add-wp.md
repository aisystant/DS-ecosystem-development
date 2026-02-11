Выполни сценарий Add Work Product для Strategist.

Источник сценария: ~/Github/PACK-digital-platform/pack/digital-platform/02-domain-entities/DP.AGENT.012-strategist/scenarios/on-demand/04-add-workproduct.md

## Рабочий продукт: $ARGUMENTS

## Контекст

- Планы: ~/Github/DS-ops/0.OPS/0.7.Plans-and-Meetings/current/

## Алгоритм

1. **Сбор информации:**
   Запроси или определи:
   - name: название РП
   - area: область (digital-platform, personal, ecosystem, governance)
   - kernel: ядро (A, B, C, 0.OPS)
   - repo: целевой репозиторий
   - budget: бюджет времени (часы)
   - priority: приоритет (P1, P2, P3)
   - criteria: критерии готовности

2. **Проверка бюджета:**
   - Текущий бюджет недели
   - После добавления
   - Предупреди если превышение

3. **Добавление:**
   - Найди последний файл недели в DS-strategy/current/weeks/
   - Добавь в него (секция "Рабочие продукты")
   - Обнови MEMORY.md → секция «РП текущей недели»
   - Обнови итоговый бюджет
   - Закоммить

Результат: РП добавлен в план недели.
