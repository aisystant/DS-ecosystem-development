---
marp: true
theme: default
paginate: true
---

<style>
  /* === СВЕТЛАЯ подложка (белый фон, тёмный текст) === */
  section {
    font-family: 'Inter', 'Helvetica Neue', Arial, sans-serif;
    padding: 36px 50px;
    font-size: 0.88em;
    background-color: #ffffff !important;
    color: #1a1a2e !important;
  }
  h1 { color: #0f3460; font-weight: 800; font-size: 1.6em; margin-bottom: 0.3em; }
  h2 { color: #0f3460; font-weight: 700; font-size: 1.2em; margin-bottom: 0.2em; }
  h3 { color: #e94560; font-weight: 600; font-size: 1.0em; }
  strong { color: #e94560; }
  blockquote { border-left: 4px solid #e94560; background: #f5f5fa; padding: 12px 20px; border-radius: 0 6px 6px 0; font-size: 0.92em; color: #1a1a2e; }
  table { border-collapse: collapse; width: 100%; font-size: 0.82em; }
  th { background: #0f3460 !important; color: #fff !important; padding: 8px 12px; text-align: left; font-weight: 700; }
  td { padding: 6px 12px; border-bottom: 1px solid #e0e0e0; color: #1a1a2e; }
  tr:nth-child(even) td { background: #f9f9fc; }
  li { line-height: 1.6; }
  a { color: #e94560; }
  code { background: #f0f0f5; color: #1a1a2e; padding: 2px 6px; border-radius: 3px; font-size: 0.9em; }
  pre { background: #f0f0f5; color: #1a1a2e; padding: 16px; border-radius: 6px; font-size: 0.82em; line-height: 1.5; }
  section::after { color: #999 !important; }

  /* === ТЁМНАЯ подложка: title === */
  section.title {
    display: flex; flex-direction: column; justify-content: center; align-items: center; text-align: center;
    background: linear-gradient(135deg, #0f3460 0%, #1a1a2e 100%) !important;
    color: #eaeaea !important;
  }
  section.title h1 { color: #f5a623 !important; font-size: 2em; }
  section.title h2 { color: #eaeaea !important; font-weight: 400; font-size: 1.1em; }
  section.title h3 { color: #f5a623 !important; }
  section.title p { color: #eaeaea !important; }
  section.title strong { color: #f5a623 !important; }
  section.title em { color: #c0c0cc !important; font-style: normal; }
  section.title a { color: #f5a623 !important; }
  section.title li { color: #eaeaea !important; }
  section.title code { background: rgba(255,255,255,0.15) !important; color: #eaeaea !important; }
  section.title blockquote { background: rgba(255,255,255,0.1) !important; border-left-color: #f5a623 !important; color: #eaeaea !important; }
  section.title::after { color: rgba(255,255,255,0.4) !important; }

  /* === Блоки === */
  .ref { background: #f0f0f5; border: 1px solid #d0d0d8; border-radius: 6px; padding: 10px 16px; margin: 12px 0; font-size: 0.85em; color: #1a1a2e; }
  .note { background: #fff8e1; border-left: 4px solid #f5a623; padding: 10px 16px; border-radius: 0 6px 6px 0; font-size: 0.88em; margin: 12px 0; color: #1a1a2e; }
</style>

<!-- _class: title -->

# Раздаточный материал

## Семинар «От экзокортекса к интеллектуальной рабочей среде»
## 28 февраля 2026 | Церен Церенов

*Справочник: то, чего нет в презентации — шаблоны, протоколы, ссылки*

---

# Что вы забираете с семинара

| # | Артефакт | Ссылка |
|---|----------|--------|
| 1 | **Шаблон IWE** (GitHub) | https://github.com/TserenTserenov/FMT-exocortex-template |
| 2 | **Этот документ** (PDF) | Справочник: протоколы, шаблоны, ссылки |
| 3 | **LEARNING-PATH** (11 разделов) | https://github.com/TserenTserenov/FMT-exocortex-template/blob/main/docs/LEARNING-PATH.md |
| 4 | **Бот @aist_me_bot** | https://t.me/aist_me_bot |
| 5 | **MCP-сервер знаний** (5 400+ док.) | https://knowledge-mcp.aisystant.workers.dev/mcp |
| 6 | **MCP исходный код** (open source) | https://github.com/aisystant/knowledge-mcp |
| 7 | **Запись семинара** | Будет отправлена участникам |

### Документация в шаблоне:
- https://github.com/TserenTserenov/FMT-exocortex-template/blob/main/docs/SETUP-GUIDE.md — пошаговая установка
- https://github.com/TserenTserenov/FMT-exocortex-template/blob/main/docs/IWE-HELP.md — быстрая справка
- https://github.com/TserenTserenov/FMT-exocortex-template/blob/main/docs/LEARNING-PATH.md — руководство (11 разделов)

### Ключевые файлы шаблона:
- https://github.com/TserenTserenov/FMT-exocortex-template/blob/main/CLAUDE.md — корневой файл инструкций
- https://github.com/TserenTserenov/FMT-exocortex-template/blob/main/memory/MEMORY.md — шаблон памяти

---

# CLAUDE.md — файл инструкций для ИИ-агента

**CLAUDE.md** — текстовый файл, который ИИ-агент читает **автоматически** при каждом запуске. Без него каждая сессия — с нуля.

| Вопрос | Ответ |
|--------|-------|
| Где лежит? | В локальной папке `~/Github/CLAUDE.md` на вашем компьютере |
| Кто читает? | Claude Code — автоматически при старте |
| Кто пишет? | Вы (инженер среды) |
| Аналогия | Должностная инструкция + регламент на столе сотрудника |

<div class="ref">

**В шаблоне:** [FMT-exocortex-template/CLAUDE.md](https://github.com/TserenTserenov/FMT-exocortex-template/blob/main/CLAUDE.md)

</div>

---

# CLAUDE.md — пакет онбординга для ИИ-агента

Вы **нанимаете** выпускника (Claude), а не создаёте его. CLAUDE.md — всё, что новый сотрудник получает в первые недели:

| Аспект | Аналогия в компании | В CLAUDE.md |
|--------|---------------------|-------------|
| **Корпоративная культура** | «У нас так принято» | Принципы, ArchGate, Capture-to-Pack |
| **Должностная инструкция** | Роли, зоны ответственности | Каталог ролей, гейты |
| **СОПы / регламенты** | Стандартные процедуры | ОРЗ (Open→Work→Close), WP Gate |
| **Ubiquitous Language** | «У нас "спринт" значит вот это» | Термины: «сервис», «РП», различения |
| **Оргструктура** | Кто кому, где что лежит | Иерархия репо (Base→Pack→DS) |
| **Система качества** | ISO, чеклисты перед релизом | ЭМОГССБ (7 характеристик, 10-балльная шкала, средняя ≥8) |
| **Институциональная память** | «Мы пробовали X — не работает» | memory/*.md, уроки |

---

# Структура CLAUDE.md (из шаблона)

| § | Секция | Что описывает |
|---|--------|---------------|
| 1 | **Архитектура репозиториев** | 3 типа репо (Base, Pack, DS), fallback chain, иерархия принципов |
| 2 | **Стадии сессии — ОРЗ** | Открытие → Работа → Закрытие, блокирующие правила, Capture-to-Pack |
| 3 | **Описания методов** | Что такое сервис, процесс, сценарий; когда нужен PROCESSES.md |
| 4 | **Memory (Слой 3)** | Навигация по справочным файлам, политика лимитов |
| 5 | **АрхГейт** | Оценка архитектурных решений по 7 характеристикам (10-балльная шкала, средняя ≥8) |
| 6 | **Обновление** | Куда писать новые правила |

> Это **slim-ядро**: триггеры и правила. Детали протоколов — в `memory/protocol-*.md` (подгружаются по триггеру, не занимают контекст постоянно).

**Без CLAUDE.md:** «Напиши код» → пишет → забыл.
**С CLAUDE.md:** «Напиши код» → проверил план → объявил роль → работает → фиксирует знания → обновляет память.

---

# Три слоя памяти экзокортекса

| Слой | Файл | Что хранит | Загрузка | Лимит |
|------|------|-----------|----------|-------|
| **1** | `MEMORY.md` | «Что на столе» — задачи, статусы, уроки | **Всегда** | ≤100 строк |
| **2** | `CLAUDE.md` | «Как я работаю» — правила, протоколы | **Всегда** | ≤150 строк |
| **3** | `memory/*.md` | «Справочники» — различения, SOTA, протоколы | **По триггеру** | ≤10 файлов |

> Каждая сессия = **первый рабочий день нового сотрудника**. Он компетентен, но не знает ваш проект. Память — то, что лежит на его столе.

| | **CLAUDE.md** (регламент) | **MEMORY.md** (памятка) |
|---|---|---|
| **Горизонт** | Постоянно | Неделя-день |
| **Кто меняет** | Редко, осознанно | Каждую сессию |
| **Пример** | «У нас код-ревью обязательно» | «На этой неделе — семинар 28 фев» |
| **Хранится** | Git (в репо) | `.claude/` (локально) |

---

# Шаблон MEMORY.md (скопируйте и заполните)

```markdown
# Оперативная память

> **Инструкции:** `~/Github/CLAUDE.md` | **Настройте под свою экосистему**

## БЛОКИРУЮЩИЕ (проверяй ВСЕГДА)

1. **WP Gate:** Задание → проверь РП в таблице ниже → нет = СТОП
2. **Close:** push ≠ закрытие → capture + подтверждение + backup
3. **ArchGate ≥8:** Предлагать ТОЛЬКО решения с оценкой ≥8

## ВАЖНЫЕ (проверяй на рубежах)

3. **Capture:** На рубеже → «Capture: X → Y»
4. **Отчёты:** ВСЕ репо в ~/Github/
5. **Процессы:** Нельзя реализовывать без PROCESSES.md

## РП текущей недели (W{N}: DD–DD мес)

| # | РП | Бюджет | Статус | Дедлайн |
|---|-----|--------|--------|---------|
| 1 | Первая стратегическая сессия | 1h | pending | — |

## Уроки

- (записывайте здесь то, что узнали о своём подходе к работе)
```

<div class="note">

**РП формулируется существительным:** документ, схема, стандарт, набор правил.
Не «анализ», не «исследование». Тест: можно распечатать?

</div>

---

# Справочные файлы memory/

Файлы в `memory/` загружаются **по триггеру** — когда Claude видит, что они нужны:

| Файл | Когда нужен | Что содержит |
|------|------------|-------------|
| `protocol-open.md` | Любое задание | WP Gate + Ритуал согласования |
| `protocol-work.md` | Во время работы | Capture-to-Pack, Pre-action Gates |
| `protocol-close.md` | «Закрывай» | Алгоритм Close, чеклист, шаблон отчёта |
| `hard-distinctions.md` | Терминология | 24 жёстких различения |
| `fpf-reference.md` | Принципы | Навигация по FPF |
| `sota-reference.md` | Архитектурные решения | 18 SOTA-практик |
| `repo-type-rules.md` | Работа с Pack | Правила для типов репо |
| `checklists.md` | Создание документа | Чеклисты корректности |
| `navigation.md` | Поиск файлов/репо | Навигационная таблица |

---

# Протокол ОРЗ: обзор

**ОРЗ** — цикл каждой рабочей сессии. Три стадии, три протокола.

| Стадия | Зачем | Триггер |
|--------|-------|---------|
| **Открытие** | Проверить план, согласовать работу | Любое задание |
| **Работа** | Фиксировать знания на лету | После Открытия |
| **Закрытие** | Зафиксировать результат, обновить память | «Закрывай» |

> **Пропуск Открытия** = незапланированная работа. **Пропуск Закрытия** = незафиксированный результат.

<div class="ref">

**Полные протоколы:** `memory/protocol-open.md`, `memory/protocol-work.md`, `memory/protocol-close.md`

</div>

---

# Открытие: WP Gate + Ритуал

### WP Gate (блокирующая проверка):

1. Прочитать MEMORY.md → секция «РП текущей недели»
2. Задание совпадает с РП? → **Да:** продолжить. **Нет:** СТОП.
3. Если не совпадает → спросить: артефакт, формулировка, репо, бюджет → записать в три места (MEMORY.md + WeekPlan + context file)

**Исключения:** задачи ≤15 мин, вопросы без изменений файлов, экстренные баг-фиксы.

### Ритуал согласования:

После WP Gate Claude **объявляет** и ждёт подтверждения:

> *«**Роль:** [из каталога]. **Работа:** [что]. **РП:** [артефакт]. **Метод:** [как]. **Оценка:** [~Xh]. **Модель:** [текущая] — рекомендую [модель] ([причина]).»*

| Модель | Когда |
|--------|-------|
| **Opus** | Архитектура, сложный код, стратегия |
| **Sonnet** | Типовые задачи, контент |
| **Haiku** | Быстрые поиски, простые вопросы |

---

# Работа: Capture-to-Pack + Gates

### Capture-to-Pack

На каждом рубеже Claude проверяет: **есть ли знание для записи?**

| Тип знания | Куда | Когда |
|------------|------|-------|
| Правило для всех репо | `~/Github/CLAUDE.md` | Сразу |
| Правило для одного репо | `<repo>/CLAUDE.md` | Сразу |
| Доменное (архитектура, паттерны) | Соответствующий Pack | При Close |
| Различение, метод, РП | Соответствующий Pack | При Close |
| Крупный урок | `memory/<topic>.md` | При Close |

Формат: *«Capture: [что] → [куда]»*

### Pre-action Gates

| Перед чем | Что проверить |
|-----------|--------------|
| Началом работы | Какие сервисы затронуты? |
| Ответом на доменный вопрос | Поиск по базе знаний (MCP) |
| `git commit` | Прочитать CLAUDE.md репо |
| Архитектурным предложением | АрхГейт: ЭМОГССБ, 10-балльная шкала, средняя ≥8 |

---

# Закрытие: алгоритм Close

При слове **«закрывай»** Claude выполняет 8 шагов:

| # | Шаг | Что делает |
|---|-----|-----------|
| 0 | **Pull** | `git pull --rebase` в DS-strategy |
| 1 | **Извлечение знаний** | Собрать captures → классифицировать → применить |
| 2 | **MEMORY.md** | Обновить статусы РП |
| 3 | **Фиксация** | Записать что сделано, что осталось |
| 4 | **Git commit** | Закоммитить (с подтверждением) |
| 5 | **План** | Обновить DS-strategy/current/Plan |
| 6 | **Backup** | `memory/ + CLAUDE.md → DS-strategy/exocortex/` |
| 7 | **WP Context** | done → архив. in_progress → обновить |
| 8 | **Остатки** | Недоделки → context file. Идеи → MAPSTRATEGIC |

### Чеклист Close:
- [ ] Все изменения закоммичены и запушены
- [ ] MEMORY.md обновлён (статусы РП)
- [ ] Captures применены
- [ ] Backup → DS-strategy/exocortex/ синхронизирован
- [ ] Отчёт Close сформирован

---

# Шаблон отчёта Close

```
**РП:** #N — [название]
**Статус:** done / in_progress

**Исполнитель:** Claude Code (модель: Opus / Sonnet / Haiku)
**Роли в сессии:**
- Кодировщик: [что сделал]
- Архитектор: [АрхГейт / не активирован]
- Экстрактор: [N кандидатов → куда / не активирован]
- Стратег: [что обновил / не активирован]

**Сделано:** [итог]
**Captures:** [N → куда]
**Git:** закоммичено + запушено ✅
**Осталось:** ничего / [что]
```

---

# Дерево файлов шаблона IWE

```
FMT-exocortex-template/
├── CLAUDE.md                    ← Правила для ИИ (Слой 2)
├── memory/
│   ├── MEMORY.md                ← Оперативная память (Слой 1)
│   ├── protocol-open.md         ← Протокол Открытия
│   ├── protocol-work.md         ← Протокол Работы
│   ├── protocol-close.md        ← Протокол Закрытия
│   ├── hard-distinctions.md     ← 24 жёстких различения
│   ├── fpf-reference.md         ← Навигация по FPF
│   ├── sota-reference.md        ← SOTA-практики
│   ├── repo-type-rules.md       ← Правила для типов репо
│   ├── checklists.md            ← Чеклисты корректности
│   └── navigation.md            ← Навигация по файлам
├── roles/
│   ├── strategist/              ← Стратег (R1)
│   ├── extractor/               ← Извлекатель (R2)
│   └── synchronizer/            ← Синхронизатор (R8)
├── docs/
│   ├── LEARNING-PATH.md         ← Руководство (11 разделов)
│   ├── SETUP-GUIDE.md           ← Инструкция по установке
│   └── IWE-HELP.md              ← Быстрая справка
└── seed/
    └── strategy/                ← Шаблон DS-strategy (отделяется при setup)
```

**Три зоны:** PLATFORM (авто-обновляется) | PERSONAL (`MEMORY.md` — ваше, не затрагивается) | SEED (→ отдельный репо)

---

# LEARNING-PATH: оглавление

https://github.com/TserenTserenov/FMT-exocortex-template/blob/main/docs/LEARNING-PATH.md — самостоятельное руководство:

| # | Раздел | Что узнаете |
|---|--------|------------|
| 1 | **Что такое IWE** | 4 архитектурных вида: системы, описания, роли, артефакты |
| 2 | **Архитектура** | 4 контура (L1 экосистема → L4 ваша IWE) |
| 3 | **Фундамент мышления** | Система, роль, описание, знание, РП |
| 4 | **Репозитории и проекты** | Base, Pack, DS — типы и правила |
| 5 | **Повседневная работа** | Цикл ОРЗ, WP Gate, Capture |
| 6 | **Знания: Pack и экстракция** | Формализация знаний, source-of-truth |
| 7 | **Роли и ИИ-агенты** | Промпты, оркестрация |
| 8 | **Качество и архитектура** | АрхГейт, ЭМОГССБ, SOTA-практики |
| 9 | **Платформа: бот и тиры** | Тиры доступа T1–T5, возможности бота |
| 10 | **Рост и развитие** | Масштабирование, свои Pack, свои роли |
| 11 | **Быстрый справочник** | Таблицы, шпаргалки, навигация |

**Новичок:** разделы 1–2 (~1 час). **Первая неделя:** 3–5. **Работающий:** 6–8. **Справочник:** 11.

---

# Три условия для ИИ-агента

| # | Условие | Аналогия |
|---|---------|----------|
| 1 | **Железо** — сервер с GPU | Тело: без него действие невозможно |
| 2 | **Модель** — файл весов (описание) | Знания выпускника школы: есть, но сами не действуют |
| 3 | **Обвязка** — код, промпты, инструменты, память | Рабочее место: офис, в котором всё подключено |

Агент возникает, когда **запущен процесс**: модель работает внутри обвязки на железе.

<div class="ref">

Нет процесса — нет агента. Есть только артефакты: файл, текст, конфигурация.

</div>

---

# Три состояния одной модели

| Состояние | Что это | Пример |
|-----------|---------|--------|
| **Описание** | Файл весов. Ничего не делает. | Claude на диске |
| **Система** | Запущена, принимает запросы. Без цели. | Claude на сервере Anthropic |
| **Агент** | Настроена с целью и автономией. Действует. | Claude внутри IWE |

<div class="note">

Одна и та же модель. Разница — в обвязке и цели.

</div>

---

# Все ссылки

| Что | Ссылка |
|-----|--------|
| **Шаблон IWE** | [github.com/TserenTserenov/FMT-exocortex-template](https://github.com/TserenTserenov/FMT-exocortex-template) |
| **Бот** | [@aist_me_bot](https://t.me/aist_me_bot) |
| **MCP-сервер** | `https://knowledge-mcp.aisystant.workers.dev/mcp` |
| **MCP исходный код** | [github.com/aisystant/knowledge-mcp](https://github.com/aisystant/knowledge-mcp) |
| **Claude Code** | [claude.ai](https://claude.ai) |
| **VS Code** | [code.visualstudio.com](https://code.visualstudio.com) |
| **LEARNING-PATH** | https://github.com/TserenTserenov/FMT-exocortex-template/blob/main/docs/LEARNING-PATH.md |
| **SETUP-GUIDE** | https://github.com/TserenTserenov/FMT-exocortex-template/blob/main/docs/SETUP-GUIDE.md |
| **IWE-HELP** | https://github.com/TserenTserenov/FMT-exocortex-template/blob/main/docs/IWE-HELP.md |
| **CLAUDE.md** (шаблон) | https://github.com/TserenTserenov/FMT-exocortex-template/blob/main/CLAUDE.md |
| **MEMORY.md** (шаблон) | https://github.com/TserenTserenov/FMT-exocortex-template/blob/main/memory/MEMORY.md |
| **Клуб** | [systemsworld.club](https://systemsworld.club) |
| **Telegram-канал** | [@systemsthinkinglife](https://t.me/systemsthinkinglife) |
| **Курс «Личное развитие»** | [aisystant.com](https://aisystant.com) |

---

# Глоссарий аббревиатур (1/2)

| Аббревиатура | Расшифровка | Пояснение |
|-------------|------------|-----------|
| **IWE** | Intellectual Working Environment | Интеллектуальная рабочая среда |
| **IDE** | Integrated Development Environment | Среда разработки (VS Code, Cursor и т.п.) |
| **ОРЗ** | Открытие → Работа → Закрытие | Протокол трёх стадий рабочей сессии |
| **РП** | Рабочий продукт | Измеримый артефакт (документ, схема, код) |
| **WP** | Work Product | = РП, англоязычный синоним |
| **MCP** | Model Context Protocol | Открытый стандарт подключения данных к ИИ |
| **ЦД** | Цифровой двойник | События → Состояние → Прогнозы |
| **Pack** | Паспорт предметной области | Репозиторий доменных знаний |
| **DS** | Downstream | Репо с кодом, контентом, планами |
| **FPF** | First Principles Framework | Фреймворк первых принципов (Aisystant) |
| **ZP** | Zero Principles | Нулевые принципы (базовый уровень) |
| **SPF** | Second Principles Framework | Фреймворк вторых принципов |

---

# Глоссарий аббревиатур (2/2)

| Аббревиатура | Расшифровка | Пояснение |
|-------------|------------|-----------|
| **ЭМОГССБ** | Э-М-О-Г-С-С-Б | 7 характеристик АрхГейта: Эволюционируемость, Масштабируемость, Обучаемость, Генеративность, Скорость, Современность, Безопасность |
| **SOTA** | State of the Art | Лучшие современные практики |
| **СОП (SOP)** | Стандартная операционная процедура | Регламент «как делать» |
| **KPI** | Key Performance Indicators | Ключевые показатели эффективности |
| **HR** | Human Resources | Управление персоналом |
| **Marp** | Markdown Presentation Ecosystem | Инструмент: Markdown → слайды (PDF/HTML) |
| **PDF** | Portable Document Format | Формат документов |
| **GPU** | Graphics Processing Unit | Вычислительное устройство для ИИ |
| **WP Gate** | Work Product Gate | Блокирующая проверка: задача есть в плане? |
| **АрхГейт (ArchGate)** | Architectural Gate | Оценка архитектурных решений (ЭМОГССБ ≥8) |
| **Capture-to-Pack** | — | Извлечение знаний из работы в Pack-репозиторий |
| **UL** | Ubiquitous Language | Единый язык команды (термин из DDD) |
| **DDD** | Domain-Driven Design | Проектирование на основе предметной области |

---

<!-- _class: title -->

# Ваш контур — в ваших руках

## Среда — рядом.

*Семинар «От экзокортекса к интеллектуальной рабочей среде» | 28 февраля 2026*
