---
type: doc
status: active
created: 2025-01-15
updated: 2025-01-15
family: F0
scope: repository
---

# 0.4. FPF Integration

> **Для ИИ-агентов:** Этот раздел содержит интеграцию с First Principles Framework (FPF) — эпистемологическим фундаментом S2R. Используйте FPF-паттерны для структурирования мышления при работе с репозиторием.

Интеграция с **First Principles Framework (FPF)** — эпистемологическим фундаментом S2R.

---

## Что такое FPF?

**First Principles Framework (FPF)** — это "операционная система для мышления", архитектура трансдисциплинарного рассуждения. FPF не методология, а **эпистема метода** — структурированная спецификация того, как думать.

**Источник:** [github.com/ailev/FPF](https://github.com/ailev/FPF)

---

## Содержимое

| Документ | Описание |
|----------|----------|
| [fpf-integration.md](fpf-integration.md) | Как S2R использует FPF |
| [fpf-patterns-map.md](fpf-patterns-map.md) | Карта паттернов FPF в S2R |
| [fpf/](fpf/) | Копия FPF-спецификации |

## Файлы FPF

```
fpf/
├── INDEX.md          # Локальные принципы проекта (~250 строк)
├── FPF-Spec.md       # Полная спецификация FPF (~43K строк)
└── FPF-Readme.md     # Обзор фреймворка
```

---

## Версия FPF

| Параметр | Значение |
|----------|----------|
| **Версия** | Актуальная на момент создания репозитория |
| **Источник** | https://github.com/ailev/FPF |
| **Обновление** | По необходимости вручную |

### Как обновить FPF

```bash
curl -sL "https://raw.githubusercontent.com/ailev/FPF/main/FPF-Spec.md" \
  -o 0.OPS/0.4.FPF-Integration/fpf/FPF-Spec.md
```

---

## Связь S2R и FPF

S2R **строится на основе FPF**, заимствуя:

| Концепция S2R | FPF-паттерн | Описание |
|---------------|-------------|----------|
| Ядро как холон | A.1 | Каждое ядро — целое и часть одновременно |
| Локальная онтология | A.1.1 | Bounded Context — термины локальны |
| Три системы | A.3 | System Triad: Suprasystem, SoI, Constructor |
| Строгое различение | A.7 | Роль ≠ Человек, Документ ≠ Система |
| Доверие | B.3 | F-G-R кортеж оценки информации |
| I/D/S дисциплина | E.10.D2 | Intension, Description, Specification |

---

## Стратегия работы с FPF

### Для обычных задач

Используй `fpf/INDEX.md` — локальные принципы проекта.

### Для глубокого анализа

Запрашивай конкретные части `FPF-Spec.md`:

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

---

## См. также

- [fpf-integration.md](fpf-integration.md) — детали интеграции
- [../0.1.Knowledge-Logic/04-ontology.md](../0.1.Knowledge-Logic/04-ontology.md) — общая онтология
- [../0.3.Roles-Matrix-3x3/](../0.3.Roles-Matrix-3x3/) — матрица ролей 3×3
- [CLAUDE.md](../../CLAUDE.md) — инструкции для ИИ-агентов
