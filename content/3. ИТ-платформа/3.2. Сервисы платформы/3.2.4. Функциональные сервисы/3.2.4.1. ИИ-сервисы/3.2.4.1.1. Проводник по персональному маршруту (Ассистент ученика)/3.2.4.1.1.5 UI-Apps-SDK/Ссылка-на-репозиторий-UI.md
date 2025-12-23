# Ссылка на репозиторий UI

## Расположение кода

**Вариант А (монорепо):**
```
ecosystem-development/
  apps/
    assistant-uchenika-ui/
      ...
```

**Вариант Б (отдельный репозиторий):**
```
https://github.com/aisystant/assistant-uchenika-ui
```

---

## Текущий статус

| Параметр | Значение |
|----------|----------|
| Репозиторий | ⬜ Не создан |
| Структура | ⬜ Не инициализирована |
| Сборка | ⬜ Не настроена |

---

## Что должно быть в репозитории

```
assistant-uchenika-ui/
  src/
    components/
      WeekSummary.tsx       # Экран "Моя неделя"
      SlotStatus.tsx        # Слот саморазвития
      WeekProducts.tsx      # Рабочие продукты
      Recommendation.tsx    # Карточка рекомендации
      ErrorState.tsx        # Состояние ошибки
      LoadingState.tsx      # Состояние загрузки
    api/
      mcp.ts                # Вызовы MCP-инструментов
    hooks/
      useWeekData.ts        # Хук для данных недели
    App.tsx
    index.tsx
  public/
  package.json
  README.md
```

---

## Как запустить локально

```bash
# Установить зависимости
npm install

# Запустить dev-сервер
npm run dev

# Собрать для публикации
npm run build
```

---

## Связанные документы

- [[Карта-экранов-и-состояний]]
- [[Соответствие-экранов-и-инструментов-MCP]]

---

**Последнее обновление:** 2025-12-23
