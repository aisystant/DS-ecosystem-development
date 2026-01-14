# FPF Спецификация

> **Примечание:** Полные файлы FPF (INDEX.md, FPF-Spec.md, FPF-Readme.md) не включены в репозиторий для уменьшения размера.

## Как получить файлы FPF

### Автоматически

Выполни команду из корня репозитория:

```bash
# Скачать INDEX.md (локальные принципы, ~250 строк)
curl -sL "https://raw.githubusercontent.com/ailev/FPF/main/INDEX.md" \
  -o 0.OPS/0.4.FPF-Integration/fpf/INDEX.md

# Скачать FPF-Spec.md (полная спецификация, ~43K строк)
curl -sL "https://raw.githubusercontent.com/ailev/FPF/main/FPF-Spec.md" \
  -o 0.OPS/0.4.FPF-Integration/fpf/FPF-Spec.md

# Скачать FPF-Readme.md (обзор фреймворка)
curl -sL "https://raw.githubusercontent.com/ailev/FPF/main/README.md" \
  -o 0.OPS/0.4.FPF-Integration/fpf/FPF-Readme.md
```

### Вручную

1. Перейди на https://github.com/ailev/FPF
2. Скачай нужные файлы:
   - `INDEX.md` — локальные принципы (~250 строк)
   - `FPF-Spec.md` — полная спецификация (~43K строк, ~200K токенов)
   - `README.md` → сохрани как `FPF-Readme.md`
3. Помести их в эту папку (`0.OPS/0.4.FPF-Integration/fpf/`)

## Структура файлов FPF

После скачивания структура будет:

```
fpf/
├── INDEX.md          # Локальные принципы проекта (~250 строк)
├── FPF-Spec.md       # Полная спецификация FPF (~43K строк)
└── FPF-Readme.md     # Обзор фреймворка
```

## Зачем нужны эти файлы?

### INDEX.md
Краткий справочник локальных принципов FPF для проекта. Используй для повседневных задач.

**Когда использовать:**
- При создании документов
- При анализе структуры
- При разрешении простых вопросов

### FPF-Spec.md
Полная спецификация First Principles Framework. Содержит все паттерны, определения и примеры.

**Когда использовать:**
- При глубоком анализе
- При необходимости точных определений
- При изучении конкретных паттернов

**Внимание:** Файл большой (~200K токенов), не загружай весь в контекст LLM. Запрашивай конкретные части.

### FPF-Readme.md
Обзор фреймворка, введение в FPF.

**Когда использовать:**
- При первом знакомстве с FPF
- Для понимания общей структуры
- Как отправная точка для изучения

## Навигация по FPF-Spec.md

Файл структурирован по частям:

| Часть | Строки | Тема |
|-------|--------|------|
| Preface | 1-500 | Введение, OS-метафора |
| Part A | 500-8000 | Kernel: Holon, Role, Transformer |
| Part B | 8000-15000 | Trans-disciplinary: Trust, Evolution |
| Part C | 15000-25000 | Calculi: Sys, KD, NQD |
| Part D | 25000-28000 | Ethics & Conflict |
| Part E | 28000-33000 | Constitution & Authoring |
| Part F | 33000-38000 | Unification: Bridges |
| Part G | 38000-43000 | SoTA Kit |

## Версионирование

| Параметр | Значение |
|----------|----------|
| **Источник** | https://github.com/ailev/FPF |
| **Версия** | Актуальная на момент скачивания |
| **Обновление** | Вручную, по необходимости |

## См. также

- [../fpf-integration.md](../fpf-integration.md) — как S2R использует FPF
- [../fpf-patterns-map.md](../fpf-patterns-map.md) — карта паттернов FPF в S2R
- [../README.md](../README.md) — обзор раздела 0.4
