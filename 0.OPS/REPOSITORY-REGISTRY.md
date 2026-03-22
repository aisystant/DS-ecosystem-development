# Реестр репозиториев экосистемы

> **Source-of-truth** для списка репозиториев экосистемы развития интеллекта.
> Обновляется при создании/удалении репозиториев.

## Типы репозиториев (3 типа)

| Тип | Подтип | Что содержит | Source-of-truth | Кто создаёт |
|-----|--------|-------------|-----------------|-------------|
| **Base** | Принципы | ZP, FPF, SPF — принципы и фреймворки корректности | Да | Платформа |
| **Base** | Форматы | FMT-* — протоколы структуры репо | Да (для формата) | Платформа |
| **Pack** | — | Паспорт предметной области (вторые принципы) | Да | Пользователь |
| **DS** | instrument | Код, боты, агенты, MCP | Нет | Пользователь |
| **DS** | governance | Планы, реестры, координация | Нет | Пользователь |
| **DS** | surface | Курсы, гайды, публикации | Нет | Пользователь |

> Base = платформа выдаёт. Pack и DS = пользователь создаёт.
> Pack = вторые принципы. DS = третьи принципы. Подробно: `ZP/README.md`

---

## 4D-классификация (сводная таблица)

> 4 измерения: **Тип** / **Система (SoI)** / **Содержание** / **Для кого**

| # | Репозиторий | Тип | Система | Содержание | Для кого | SoT | Статус |
|---|-------------|-----|---------|------------|----------|-----|--------|
| 0 | [ZP](https://github.com/TserenTserenov/ZP) | Base/Принципы | cross-cutting | text-description | public | yes | Active |
| 1 | [FPF](https://github.com/ailev/FPF) | Base/Принципы | cross-cutting | text-description | public | yes | External |
| 2 | [SPF](https://github.com/TserenTserenov/SPF) | Base/Принципы | cross-cutting | text-description | public | yes | Active |
| 3 | [FMT-S2R](https://github.com/TserenTserenov/FMT-S2R) | Base/Форматы | cross-cutting | text-description | public | yes | Active |
| 14 | [FMT-exocortex-template](https://github.com/TserenTserenov/FMT-exocortex-template) | Base/Форматы | cross-cutting | text-description | public | yes | Active |
| 4 | [PACK-personal](https://github.com/aisystant/PACK-personal) | Pack | Созидатель | text-description | team | yes | Active |
| 5 | [PACK-ecosystem](https://github.com/TserenTserenov/PACK-ecosystem) | Pack | Экосистема | text-description | team | yes | Active |
| 6 | [PACK-digital-platform](https://github.com/TserenTserenov/PACK-digital-platform) | Pack | ИТ-платформа | text-description | team | yes | Active |
| 20 | [PACK-MIM](https://github.com/TserenTserenov/PACK-MIM) | Pack | МИМ (мастерская) | text-description | team | yes | Active |
| ~~24~~ | ~~[PACK-education](https://github.com/TserenTserenov/PACK-education)~~ | ~~Pack~~ | ~~Методика обучения~~ | ~~—~~ | ~~—~~ | ~~—~~ | Archived → PACK-MIM (WP-154) |
| 25 | [PACK-verification](https://github.com/TserenTserenov/PACK-verification) | Pack | Верификация и приёмка | text-description | team | yes | Active |
| 27 | [PACK-autonomous-agents](https://github.com/TserenTserenov/PACK-autonomous-agents) | Pack | Автономные агенты | text-description | team | yes | Active |
| — | ~~DS-twin~~ | — | — | — | — | — | Archived → digital-twin-mcp (#18) |
| 9 | [DS-Knowledge-Index-Tseren](https://github.com/TserenTserenov/DS-Knowledge-Index-Tseren) | DS/instrument | Созидатель | code | personal | no | Active |
| 10 | [DS-ecosystem-development](https://github.com/aisystant/DS-ecosystem-development) | DS/governance | Экосистема | text-governance | team | no | Active |
| 11 | [DS-my-strategy](https://github.com/TserenTserenov/DS-my-strategy) | DS/governance | Созидатель | text-governance | personal | no | Active |
| 12 | [docs](https://github.com/aisystant/docs) | DS/surface | Экосистема | text-publication | public | no | Active |
| 13 | [DS-marathon-v2-tseren](https://github.com/TserenTserenov/DS-marathon-v2-tseren) | DS/surface | Экосистема | text-publication | team | no | Active |
| 23 | [DS-principles-curriculum](https://github.com/aisystant/DS-principles-curriculum) | DS/surface | Экосистема | text-publication | team | no | Active |
| 15 | [DS-ai-systems](https://github.com/TserenTserenov/DS-ai-systems) | DS/instrument | ИТ-платформа | code | personal | no | Active |
| 18 | [digital-twin-mcp](https://github.com/aisystant/digital-twin-mcp) | DS/instrument | ИТ-платформа | code | team | no | Active |
| 19 | [aist_bot_newarchitecture](https://github.com/aisystant/aist_bot_newarchitecture) | DS/instrument | Бот Aist | code | team | no | Active |
| 21 | [aisystant](https://github.com/aisystant/aisystant) | DS/instrument | Экосистема | code | team | no | External |
| 22 | [SystemsSchool_bot](https://github.com/aisystant/SystemsSchool_bot) | DS/instrument | Экосистема | code | team | no | External |
| 26 | [activity-hub](https://github.com/aisystant/activity-hub) | DS/instrument | ИТ-платформа | code | team | no | Active |
| 28 | [DS-autonomous-agents](https://github.com/TserenTserenov/DS-autonomous-agents) | DS/instrument | Автономные агенты | code | personal | no | Active |
| 30 | [DS-agent-workspace](https://github.com/TserenTserenov/DS-agent-workspace) | DS/governance | Автономные агенты | agent-outputs | personal | no | Active |
| 29 | [knowledge-mcp](https://github.com/aisystant/knowledge-mcp) | DS/instrument | ИТ-платформа | code | team | no | Active |
| 31 | [guides-mcp](https://github.com/aisystant/guides-mcp) | DS/instrument | ИТ-платформа | code | team | no | Active |
| 32 | [fsm-mcp](https://github.com/aisystant/fsm-mcp) | DS/instrument | ИТ-платформа | code | team | no | Active |
| — | ~~DS-aist-bot~~ | — | — | — | — | — | Archived → aist_bot_newarchitecture |
| — | ~~DS-synchronizer~~ | — | — | — | — | — | Archived → DS-ai-systems |
| — | ~~DS-fixer-agent~~ | — | — | — | — | — | Archived → DS-ai-systems |
| — | ~~DS-pulse-agent~~ | — | — | — | — | — | Archived → DS-ai-systems |

---

## По типам (детали)

### Base/Принципы

| Репозиторий | Роль | Владелец |
|-------------|------|----------|
| [ZP](https://github.com/TserenTserenov/ZP) | Zeroth Principles (6 мета-ограничений + карта иерархии 0→1→2→3) | TserenTserenov |
| [FPF](https://github.com/ailev/FPF) | First Principles Framework | ailev |
| [SPF](https://github.com/TserenTserenov/SPF) | Second Principles Framework | TserenTserenov |

### Base/Форматы

| Репозиторий | Роль | Владелец |
|-------------|------|----------|
| [FMT-S2R](https://github.com/TserenTserenov/FMT-S2R) | Structured Second-level Repository | TserenTserenov |
| [FMT-exocortex-template](https://github.com/TserenTserenov/FMT-exocortex-template) | Exocortex template (fork & deploy) | TserenTserenov |

### Pack (Source-of-truth)

| Репозиторий | Область | Upstream | Владелец |
|-------------|---------|----------|----------|
| [PACK-personal](https://github.com/aisystant/PACK-personal) | Созидатель (персональное развитие) | SPF, FPF | aisystant |
| [PACK-ecosystem](https://github.com/TserenTserenov/PACK-ecosystem) | Экосистема развития интеллекта (чёрный ящик + подсистемы) | SPF, FPF | TserenTserenov |
| [PACK-digital-platform](https://github.com/TserenTserenov/PACK-digital-platform) | ИТ-платформа и цифровой двойник | SPF, FPF, PACK-personal | TserenTserenov |
| [PACK-MIM](https://github.com/TserenTserenov/PACK-MIM) | Мастерская: форматы, программы, организация развития | SPF, FPF | TserenTserenov |
| ~~[PACK-education](https://github.com/TserenTserenov/PACK-education)~~ | ~~Archived → PACK-MIM (WP-154). Методика обучения расформирована в MIM.~~ | ~~—~~ | ~~—~~ |
| [PACK-verification](https://github.com/TserenTserenov/PACK-verification) | Верификация и приёмка: методы проверки, эталоны, критерии приёмки (трансдоменный) | SPF, FPF | TserenTserenov |

### DS/instrument

| Репозиторий | Назначение | Upstream pack | Владелец |
|-------------|------------|---------------|----------|
| [DS-Knowledge-Index-Tseren](https://github.com/TserenTserenov/DS-Knowledge-Index-Tseren) | Персональный индекс знаний + публичные посты (`posts/`) | PACK-personal | TserenTserenov |
| [DS-ai-systems](https://github.com/TserenTserenov/DS-ai-systems) | Монорепо ИИ-систем (7 систем: стратег, экстрактор, синхронизатор, наладчик, статистик, оценщик, шаблонизатор) | PACK-digital-platform, PACK-personal | TserenTserenov |
| [digital-twin-mcp](https://github.com/aisystant/digital-twin-mcp) | MCP-сервер цифрового двойника | PACK-digital-platform, PACK-personal | aisystant |
| [aist_bot_newarchitecture](https://github.com/aisystant/aist_bot_newarchitecture) | Telegram-бот (new architecture, State Machine) | PACK-personal | aisystant |
| [aisystant](https://github.com/aisystant/aisystant) | LMS Aisystant (SYS.004) | PACK-ecosystem | aisystant (external) |
| [SystemsSchool_bot](https://github.com/aisystant/SystemsSchool_bot) | Telegram-бот стажировок и расписания | PACK-ecosystem | aisystant (external) |
| [activity-hub](https://github.com/aisystant/activity-hub) | Единая точка записи событий в ЦД (LMS, бот, клуб, IWE) | PACK-digital-platform | aisystant |
| [knowledge-mcp](https://github.com/aisystant/knowledge-mcp) | MCP-сервер поиска по знаниям (Pack, DS, FMT) | PACK-digital-platform | aisystant |
| [guides-mcp](https://github.com/aisystant/guides-mcp) | MCP-сервер руководств и гайдов | PACK-digital-platform | aisystant |
| [fsm-mcp](https://github.com/aisystant/fsm-mcp) | MCP-сервер конечных автоматов | PACK-digital-platform | aisystant |
| [DS-autonomous-agents](https://github.com/TserenTserenov/DS-autonomous-agents) | Код автономных агентов (промпты, dispatcher, trajectory cache) | PACK-autonomous-agents, PACK-digital-platform | TserenTserenov |

### DS/governance

| Репозиторий | Назначение | Upstream packs | Владелец |
|-------------|------------|----------------|----------|
| [DS-ecosystem-development](https://github.com/aisystant/DS-ecosystem-development) | Координация экосистемы | PACK-ecosystem, PACK-personal, PACK-digital-platform | aisystant |
| [DS-my-strategy](https://github.com/TserenTserenov/DS-my-strategy) | Личное стратегирование (HUB агента Стратег) | PACK-personal, PACK-digital-platform | TserenTserenov |
| [DS-agent-workspace](https://github.com/TserenTserenov/DS-agent-workspace) | Шина данных автономных агентов (результаты, черновики, отчёты) | PACK-autonomous-agents, PACK-digital-platform | TserenTserenov |

### DS/surface

| Репозиторий | Назначение | Upstream pack | Владелец |
|-------------|------------|---------------|----------|
| [docs](https://github.com/aisystant/docs) | VitePress документация | PACK-personal, PACK-ecosystem | aisystant |
| [DS-marathon-v2-tseren](https://github.com/TserenTserenov/DS-marathon-v2-tseren) | Программа марафона v2 | PACK-personal, PACK-ecosystem | TserenTserenov |
| [DS-principles-curriculum](https://github.com/aisystant/DS-principles-curriculum) | Программа обучения принципам (FPF ячейки) | PACK-personal, PACK-ecosystem | aisystant |

---

## Граф зависимостей

```
ZP (Base/Принципы, Level 0)
  │
  └──▶ FPF (Base/Принципы, Level 1)
        │
        └──▶ SPF (Base/Принципы, Level 2)
        │
        ├──▶ PACK-personal (Pack: Созидатель)
        │     │
        │     ├──▶ aist_bot_newarchitecture (DS/instrument)
        │     ├──▶ DS-Knowledge-Index-Tseren (DS/instrument)
        │     ├──▶ docs (DS/surface)
        │     └──▶ DS-marathon-v2-tseren (DS/surface)
        │
        ├──▶ PACK-MIM (Pack: Мастерская)
        │     │
        │     └──▶ DS-ecosystem-development (DS/governance)
        │
        │     [PACK-education → archived, merged into PACK-MIM]
        │
        ├──▶ PACK-verification (Pack: Верификация и приёмка — трансдоменный)
        │
        ├──▶ PACK-ecosystem (Pack: Экосистема — чёрный ящик)
        │     │
        │     ├──▶ DS-ecosystem-development (DS/governance)
        │     ├──▶ docs (DS/surface)
        │     ├──▶ DS-marathon-v2-tseren (DS/surface)
        │     └──▶ DS-principles-curriculum (DS/surface)
        │
        ├──▶ PACK-digital-platform (Pack: ИТ-платформа)
        │     │
        │     ├──▶ DS-twin (DS/instrument)
        │     ├──▶ digital-twin-mcp (DS/instrument)
        │     ├──▶ DS-my-strategy (DS/governance — агент Стратег)
        │     ├──▶ DS-ai-systems (DS/instrument — 7 ИИ-систем)
        │     ├──▶ activity-hub (DS/instrument — единая точка записи событий)
        │     ├──▶ knowledge-mcp (DS/instrument — поиск по знаниям)
        │     ├──▶ guides-mcp (DS/instrument — руководства)
        │     └──▶ fsm-mcp (DS/instrument — конечные автоматы)
        │
        └──▶ FMT-S2R (Base/Форматы)
              │
              └──▶ DS-ecosystem-development (DS/governance)

FMT-exocortex-template (Base/Форматы, setup.sh встроен)
  │
  └──▶ DS-ai-systems/setup (DS/instrument, author-side: template-sync)
```

---

## Обязательный контракт

Каждый репозиторий экосистемы **ДОЛЖЕН** иметь:

### 1. Признак типа в README.md (первая строка после заголовка)

```markdown
> **Тип репозитория:** `Base/Принципы` | `Base/Форматы` | `Pack` | `DS/instrument` | `DS/governance` | `DS/surface`
```

### 2. Файл `REPO-TYPE.md` (только свои репо)

`REPO-TYPE.md` размещается только в репозиториях, которые создал пользователь (в т.ч. на аккаунте организации aisystant).
Для чужих репо (ailev/FPF, aisystant/aisystant, aisystant/SystemsSchool_bot и др.) описание хранится только в этом реестре — не в самом репо.

---

## Правила

1. **Pack — единственный source-of-truth**. DS меняется вслед за Pack
2. **Один репозиторий — один тип**. Не смешивать Pack и DS
3. **При изменении Pack** — обновить DS
4. **При добавлении репозитория** — обновить этот реестр
5. **При удалении репозитория** — обновить этот реестр
6. **REPO-TYPE.md** — только в своих репозиториях (созданных пользователем, в т.ч. на org-аккаунте). Для чужих — описание только в этом реестре

---

*Последнее обновление: 2026-03-18*
