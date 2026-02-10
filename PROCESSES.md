---
type: process
status: active
created: 2026-02-10
updated: 2026-02-10
---

# Процессы экосистемы

> Межсистемные процессы (сценарии) экосистемы развития интеллекта.
> Внутренние процессы каждой системы → `<repo>/PROCESSES.md`.
> Различение: процесс = поток действий с ВДВ; сценарий = межсистемный процесс (синоним).

---

## 1. Пользовательские сценарии

### 1.1. Рабочая сессия Claude Code

> Тип: пользовательский сценарий
> Владелец: Claude Code (сессия)
> Участники: Пользователь, Claude Code, MEMORY.md, CLAUDE.md, memory/*.md, my-strategy, Pack-репо

**Вход:** Задание от пользователя

**Действие:**

1. **Open: WP Gate** — Claude проверяет РП в MEMORY.md → совпадает/СТОП
2. **Open: Ритуал** — Claude объявляет Работу/РП/Метод → пользователь согласует
3. **Work** — выполнение задачи + capture-to-pack на рубежах
4. **Close** — собрать captures → применить → обновить MEMORY.md → обновить my-strategy/Plan → backup memory/ → my-strategy/exocortex/ → коммит

**Выход:** Закоммиченный результат, обновлённый план, captures в Pack/CLAUDE.md/memory

**Данные:**

| Данные | Направление | Формат |
|--------|-------------|--------|
| MEMORY.md (таблица РП) | Вход → Claude | Markdown |
| CLAUDE.md (протоколы) | Вход → Claude | Markdown |
| memory/*.md (справочники) | Вход → Claude (по необходимости) | Markdown |
| Captures | Выход → Pack / CLAUDE.md / memory | Текст |
| Статусы РП | Выход → MEMORY.md, my-strategy/Plan | Таблица |

---

### 1.2. Стратегирование недели

> Тип: пользовательский сценарий
> Владелец: Пользователь + Стратег
> Участники: Пользователь, Стратег, my-strategy, все ~/Github/*/WORKPLAN.md, ~/Github/*/MAPSTRATEGIC.md

**Вход:** git log за прошлую неделю (все ~/Github/ репо), WeekPlan W{N-1}, WORKPLAN.md, MAPSTRATEGIC.md

**Действие:**

1. **Strategy Session (Фаза 1, авто)** — Стратег собирает коммиты за неделю, формирует итоги, создаёт draft WeekPlan
2. **Strategy Session (Фаза 2, интерактив)** — пользователь утверждает/корректирует
3. **Strategy-Cascade** — обновление всех WORKPLAN.md, Strategy.md, MEMORY.md

> Отдельный WeekReport НЕ нужен для стратегирования. Итоги прошлой недели — часть нового WeekPlan.
> WeekReport (`./scripts/strategist.sh week-review`) — опциональный, для публикации в клубе.

**Выход:** WeekPlan W{N} (confirmed), обновлённые WORKPLAN.md во всех репо, обновлённый MEMORY.md

**Данные:**

| Данные | Направление | Формат |
|--------|-------------|--------|
| git log за неделю (все репо) | Вход → Стратег | Git output |
| WeekPlan W{N-1} | Вход → Стратег | Markdown |
| ~/Github/*/WORKPLAN.md | Вход → Стратег | Markdown |
| ~/Github/*/MAPSTRATEGIC.md | Вход → Стратег | Markdown |
| WeekPlan W{N} | Выход → my-strategy/current/ | Markdown |
| MEMORY.md (новые РП) | Выход → memory/ | Markdown |

---

## 2. Платформенные сценарии

### 2.1. Day-Close

> Тип: платформенный сценарий
> Владелец: Стратег (ручной — по запросу пользователя)
> Участники: Стратег, все ~/Github/ репо, my-strategy, MEMORY.md, экзокортекс

**Вход:** Коммиты за день (git log по всем ~/Github/ репо)

**Действие:**

1. Сбор коммитов → группировка по репо и РП
2. Обновление WeekPlan W{N} (статусы, carry-over)
3. Синхронизация MEMORY.md (статусы РП)
4. Backup: memory/ + CLAUDE.md → my-strategy/exocortex/
5. Коммит

> Отдельный файл отчёта НЕ создаётся. Итоги дня войдут в DayPlan следующего утра.

**Выход:** Обновлённый WeekPlan, актуальный MEMORY.md, backup экзокортекса

**Данные:**

| Данные | Направление | Формат |
|--------|-------------|--------|
| git log (все репо) | Вход → Стратег | Git output |
| WeekPlan W{N} (обновлённый) | Выход → my-strategy/current/ | Markdown |
| MEMORY.md (обновлённый) | Выход → memory/ | Markdown |
| Exocortex backup | Выход → my-strategy/exocortex/ | Файлы |

---

### 2.2. Strategy-Cascade

> Тип: платформенный сценарий
> Владелец: Стратег (после strategy session, Фаза 2)
> Участники: Стратег, my-strategy, все ~/Github/*/WORKPLAN.md, все ~/Github/*/MAPSTRATEGIC.md

**Вход:** Утверждённый WeekPlan W{N} (status: confirmed)

**Действие:**

1. Прочитать утверждённый WeekPlan W{N}
2. Обновить Strategy.md (приоритеты, бюджеты)
3. Обновить все ~/Github/*/WORKPLAN.md
4. Обновить MAPSTRATEGIC.md (если изменились фазы)
5. Обновить MEMORY.md (новые РП)
7. Обновить Dissatisfactions.md
8. Коммит всех изменений

**Выход:** Обновлённая стратегия, новый план недели, актуальные WORKPLAN.md

---

### 2.3. Синхронизация экзокортекса (Backup)

> Тип: платформенный сценарий
> Владелец: Claude Code (Close) + Стратег (day-close)
> Участники: memory/*.md, ~/Github/CLAUDE.md, my-strategy/exocortex/

**Вход:** Изменённые файлы memory/*.md + CLAUDE.md

**Действие:** Копирование → my-strategy/exocortex/

**Выход:** Версионированная копия в git (my-strategy)

---

## 3. Формат описания процесса (шаблон)

```markdown
### Процесс: [Название]

> Тип: пользовательский сценарий | платформенный сценарий | внутренний процесс
> Владелец: [система]
> Участники: [системы]

**Вход:** [данные]
**Действие:** [шаги]
**Выход:** [данные]

**Данные:** (таблица ВДВ)
```

---

*Последнее обновление: 2026-02-10*
