---
type: process
status: active
created: 2026-02-10
updated: 2026-02-11
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
> Участники: Пользователь, Claude Code, MEMORY.md, CLAUDE.md, memory/*.md, DS-strategy, Pack-репо

**Вход:** Задание от пользователя

**Действие:**

1. **Open: WP Gate** — Claude проверяет РП в MEMORY.md → совпадает/СТОП
2. **Open: Ритуал** — Claude объявляет Работу/РП/Метод → пользователь согласует
3. **Work** — выполнение задачи + capture-to-pack на рубежах
4. **Close** — собрать captures → применить → обновить MEMORY.md → обновить DS-strategy/Plan → backup memory/ → DS-strategy/exocortex/ → обновить/создать WP Context File в inbox/ (если РП in_progress, ≥2 сессий) или архивировать (если done) → коммит

**Выход:** Закоммиченный результат, обновлённый план, captures в Pack/CLAUDE.md/memory

**Данные:**

| Данные | Направление | Формат |
|--------|-------------|--------|
| MEMORY.md (таблица РП) | Вход → Claude | Markdown |
| CLAUDE.md (протоколы) | Вход → Claude | Markdown |
| memory/*.md (справочники) | Вход → Claude (по необходимости) | Markdown |
| Captures | Выход → Pack / CLAUDE.md / memory | Текст |
| Статусы РП | Выход → MEMORY.md, DS-strategy/Plan | Таблица |
| WP Context File | Выход → DS-strategy/inbox/ (при Close) + Вход → Claude (при Open) | Markdown |

---

### 1.2. Стратегирование недели

> Тип: пользовательский сценарий
> Владелец: Пользователь + Стратег
> Участники: Пользователь, Стратег, DS-strategy, все ~/Github/*/WORKPLAN.md, ~/Github/*/MAPSTRATEGIC.md

**Вход:** WeekReport W{N-1} (создан week-review, Пн 00:00), WORKPLAN.md, MAPSTRATEGIC.md, docs/*, inbox/*

**Действие:**

1. **Week-Review (авто, Пн 00:00)** — Стратег собирает коммиты за неделю → WeekReport
2. **Session-Prep (авто, Пн 4:00)** — Стратег читает WeekReport + docs/ + inbox/ + MAPSTRATEGIC.md → обновляет Strategy.md → формирует draft WeekPlan с повесткой
3. **Strategy-Session (интерактив, вручную)** — пользователь утверждает/корректирует → синхронизация WORKPLAN.md, MEMORY.md, Strategy.md, очистка inbox

> Бывший Strategy-Cascade поглощён session-prep (агрегация MAPSTRATEGIC) и strategy-session (синхронизация).

**Выход:** WeekReport (для клуба), WeekPlan W{N} (confirmed), обновлённые Strategy.md, WORKPLAN.md, MEMORY.md

**Данные:**

| Данные | Направление | Формат |
|--------|-------------|--------|
| WeekReport W{N-1} | Вход → Strategy | Markdown |
| ~/Github/*/WORKPLAN.md | Вход → Strategy | Markdown |
| ~/Github/*/MAPSTRATEGIC.md | Вход → Strategy | Markdown |
| WeekPlan W{N} | Выход → DS-strategy/current/ | Markdown |
| MEMORY.md (новые РП) | Выход → memory/ | Markdown |

---

### 1.3. Цикл работы с экзокортексом

> Тип: пользовательский сценарий
> Владелец: Пользователь
> Участники: Пользователь, Стратег, Синхронизатор, Claude Code, @aist_me_bot, Pack-репо, DS-strategy

**Вход:** Развёрнутый экзокортекс + текущие проекты пользователя

**Действие (дневной цикл):**

1. **Утро: Ориентация**
   - Стратег формирует DayPlan (авто, 4:00) → приоритеты дня из WeekPlan
   - Пользователь читает DayPlan → выбирает первый РП
   - @aist_me_bot: быстрый доступ к плану дня и знаниям из Pack

2. **День: Фокусная работа**
   - Рабочие сессии Claude Code (→ 1.1): экзокортекс проверяет WP Gate, ведёт ритуал, фиксирует captures
   - Исчезающие заметки: пользователь фиксирует мысли/идеи → Claude Code формализует → маршрутизирует в Pack (capture-to-pack)
   - @aist_me_bot: быстрые вопросы по знаниям, навигация по Pack, статус РП
   - Пользователь не отвлекается на планирование (→ Стратег), трекинг (→ WP Gate), маршрутизацию знаний (→ Capture), backup (→ авто)

3. **Вечер: Фиксация**
   - Day-Close (→ 2.1): Стратег собирает итоги → обновляет WeekPlan → backup экзокортекса
   - Пользователь: только подтверждение (или авто-режим)

**Действие (недельный цикл):**

4. **Понедельник: Стратегирование**
   - Стратегирование недели (→ 1.2): Week-Review → Session-Prep → Strategy-Session
   - Пользователь: 30–60 мин на утверждение/корректировку плана

5. **В течение недели: Развитие Pack**
   - Captures из рабочих сессий накапливаются в Pack-репо
   - Новые паттерны, различения, методы формализуются по SPF
   - Pack растут органически за счёт проектной работы — без отдельных усилий

6. **Обновления экзокортекса**
   - Платформа публикует обновления → upstream FMT-exocortex
   - Пользователь: `git fetch upstream && git merge` (→ DS-exocortex-setup-agent, Сценарий 2)
   - Platform-space обновляется, User-space не затрагивается

**Выход:** Развивающаяся база знаний (Pack), актуальные планы, зафиксированные результаты

**Что автоматизирует экзокортекс (рутина → авто):**

| Рутина | Кто делает | Когда |
|--------|-----------|-------|
| Планирование дня | Стратег (авто) | Каждое утро, 4:00 |
| Проверка задачи в плане | Claude Code (WP Gate) | Начало сессии |
| Маршрутизация знаний (мелкие правила) | Claude Code (Capture-to-Pack, напрямую) | На рубежах |
| Формализация знаний (доменное) | Экстрактор (KE, DP.AISYS.013) | Close / Inbox-Check / по запросу |
| Итоги дня | Стратег (Day-Close) | Вечер / по запросу |
| Синхронизация файлов (remote → local) | Синхронизатор (file-sync) | Каждые 2 мин + boot |
| Backup экзокортекса | Claude Code + Стратег | Close + Day-Close |
| Обзор недели | Стратег (Week-Review) | Пн, 00:00 |
| Подготовка плана недели | Стратег (Session-Prep) | Пн, 4:00 |

**Что остаётся пользователю (фокус):**

| Действие | Частота |
|----------|---------|
| Утверждение плана недели | 30–60 мин / нед |
| Проектная работа (сессии Claude Code) | Основное время |
| Исчезающие заметки (мысли, идеи) | По ходу дня |
| Вопросы к боту | По необходимости |

**Данные:**

| Данные | Направление | Формат |
|--------|-------------|--------|
| DayPlan | Стратег → Пользователь | Markdown |
| Исчезающие заметки | Пользователь → Бот → inbox/captures.md → KE → Pack | Текст → Markdown |
| Captures (мелкие правила) | Claude Code → CLAUDE.md / memory/ (напрямую) | Markdown |
| Captures (доменное знание) | Claude Code → KE → Pack-репо (через формализацию) | Markdown |
| Статусы РП | Claude Code / Стратег → MEMORY.md | Таблица |
| WeekPlan / WeekReport | Стратег → DS-strategy | Markdown |
| Быстрые запросы | Пользователь ↔ @aist_me_bot | Telegram |
| Обновления экзокортекса | Платформа → upstream → пользователь | Git |

---

## 2. Платформенные сценарии

### 2.1. Day-Close

> Тип: платформенный сценарий
> Владелец: Стратег (ручной — по запросу пользователя)
> Участники: Стратег, все ~/Github/ репо, DS-strategy, MEMORY.md, экзокортекс

**Вход:** Коммиты за день (git log по всем ~/Github/ репо)

**Действие:**

1. Сбор коммитов → группировка по репо и РП
2. Обновление WeekPlan W{N} (статусы, carry-over)
3. Синхронизация MEMORY.md (статусы РП)
4. Backup: memory/ + CLAUDE.md → DS-strategy/exocortex/
5. Коммит

> Отдельный файл отчёта НЕ создаётся. Итоги дня войдут в DayPlan следующего утра.

**Выход:** Обновлённый WeekPlan, актуальный MEMORY.md, backup экзокортекса

**Данные:**

| Данные | Направление | Формат |
|--------|-------------|--------|
| git log (все репо) | Вход → Стратег | Git output |
| WeekPlan W{N} (обновлённый) | Выход → DS-strategy/current/ | Markdown |
| MEMORY.md (обновлённый) | Выход → memory/ | Markdown |
| Exocortex backup | Выход → DS-strategy/exocortex/ | Файлы |

---

### 2.2. Синхронизация экзокортекса (Backup)

> Тип: платформенный сценарий
> Владелец: Claude Code (Close) + Стратег (day-close)
> Участники: memory/*.md, ~/Github/CLAUDE.md, DS-strategy/exocortex/

**Вход:** Изменённые файлы memory/*.md + CLAUDE.md

**Действие:** Копирование → DS-strategy/exocortex/

**Выход:** Версионированная копия в git (DS-strategy)

---

### 2.3. Ontology Sync (синхронизация онтологий)

> Тип: платформенный сценарий
> Владелец: Knowledge Extractor (DS-extractor-agent)
> Участники: Pack ontology.md (все), DS-my-strategy/ontology.md (мастер), Downstream ontology.md

**Вход:** Изменение ontology.md в любом Pack / создание нового Pack

**Действие:**
1. Extractor сравнивает Pack-онтологии с мастер-онтологией
2. Находит расхождения (новые/изменённые/удалённые понятия)
3. Проверяет Downstream-ссылки
4. Формирует Ontology Sync Report
5. Применяет одобренные обновления

**Выход:** Обновлённая мастер-онтология + обновлённые Downstream ontology.md

**Данные:**

| Вход | Действие | Выход |
|------|----------|-------|
| Pack ontology.md (изменённый) | Сравнить с мастером | Ontology Sync Report |
| DS-my-strategy/ontology.md | Найти расхождения | Обновлённый мастер |
| Downstream ontology.md | Проверить актуальность | Обновлённые Downstream |

**Подробности:** `DS-extractor-agent/PROCESSES.md` → Process 7, `DS-extractor-agent/prompts/ontology-sync.md`

---

### 2.4. Синхронизация файлов экзокортекса (file-sync)

> Тип: платформенный сценарий
> Владелец: Синхронизатор (DS-synchronizer)
> Участники: Синхронизатор, DS-my-strategy (remote → local), любые репо по конфигу

**Вход:** Конфигурация watchers (config.yaml): список репо + файлов

**Действие:**

1. launchd запускает Синхронизатор каждые 2 мин + при boot
2. `git fetch` (fail-safe: нет сети → exit 0)
3. Для каждого файла: сравнить hash local vs remote
4. Если отличается → `git checkout origin/branch -- file`

**Выход:** Обновлённые локальные файлы (без полного pull, без затрагивания других файлов)

**Данные:**

| Данные | Направление | Формат |
|--------|-------------|--------|
| config.yaml (watchers) | Вход → Синхронизатор | YAML |
| Remote файлы (GitHub) | Вход → git fetch | Git objects |
| Локальные файлы | Выход → файловая система | Markdown |

---

### 2.5. Наблюдение и вызов агентов (watch → trigger) — будущее

> Тип: платформенный сценарий
> Владелец: Синхронизатор (DS-synchronizer)
> Участники: Синхронизатор → Экстрактор / Стратег

**Вход:** Конфигурация watchers (config.yaml): условия + действия

**Действие:**

1. Синхронизатор проверяет условие (новый контент / новые коммиты / расписание)
2. Условие выполнено → вызов соответствующего агента:
   - Новый контент в captures.md → trigger Экстрактор (inbox-check)
   - Коммит в Pack-репо → trigger Экстрактор (cross-repo-sync)
   - Расписание (4:00) → trigger Стратег (day-plan)

**Выход:** Запуск агента с нужным сценарием

### 2.6. Проецирование знаний из Pack в Downstream (pack-project)

> Тип: платформенный сценарий
> Владелец: Синхронизатор (DS-synchronizer)
> Участники: Синхронизатор, Pack-репо (source), Downstream-репо (target)

**Вход:** Конфигурация системы (configs/systems/<id>.yaml): source Pack + mapping + target repo

**Действие:**

1. Синхронизатор обнаруживает изменение в Pack-сущности (через code-scan или ручной trigger)
2. Читает mapping из конфига системы (какие секции Pack → какие поля проекции)
3. Извлекает секции из Pack-сущности
4. Валидирует: обязательные поля, формат, консистентность
5. Генерирует Projected Read Model (YAML-файл в Downstream-репо)
6. Коммитит в Downstream-репо (git add + commit + push)
7. При ошибках — уведомляет через notify.sh (успех = тишина)

**Выход:** Обновлённая проекция (read-only YAML) в Downstream-репо

**Данные:**

| Данные | Роль | Формат |
|--------|------|--------|
| configs/systems/<id>.yaml | Вход → конфигурация | YAML |
| Pack-сущность (DP.AISYS.014 и др.) | Вход → source-of-truth | Markdown |
| Projected Read Model | Выход → Downstream | YAML (read-only, auto-generated) |

**Архитектурный паттерн:** Single Writer (Pack) → Projected Read Model (CQRS-lite) → Conformist (Downstream). По Хононову (DDD): Anti-Corruption Layer между Bounded Contexts.

**Пример:** Pack (DP.AISYS.014 — бот) → Синхронизатор → `aist_bot/config/self_knowledge_projection.yaml` (identity, scenarios, FAQ). Бот читает только проекцию, не ходит в Pack.

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

*Последнее обновление: 2026-02-11*
