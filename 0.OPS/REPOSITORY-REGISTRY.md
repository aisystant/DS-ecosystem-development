# Реестр репозиториев экосистемы

> **Source-of-truth** для списка репозиториев экосистемы развития интеллекта.
> Обновляется при создании/удалении репозиториев.

## Типы репозиториев (5 типов)

| Тип | Уровень принципов | Критерий | Source-of-truth |
|-----|-------------------|----------|-----------------|
| **Foundation** | 0-й (нулевые) | Транс-дисциплинарные мета-ограничения | Да |
| **Pack** | 2-й (вторые принципы) | Source-of-truth области (что истинно и как проверять) | Да |
| **Framework** | 1-й / 2-й | Рамки корректности (FPF/SPF) | Да |
| **Format** | 3-й (фреймворк третьих) | Протокол оформления | Да (для формата) |
| **Downstream** | 3-й (третьи принципы) | Производные от Pack | Нет |

> Pack = вторые принципы. Downstream = третьи принципы. Подробно: `ZP/README.md`

### Подтипы Downstream

| Подтип | Что делает |
|--------|------------|
| `instrument` | Код, сервисы, MCP, боты |
| `governance` | Управление, планы, реестры |
| `surface` | Курсы, гайды, документация |

---

## 4D-классификация (сводная таблица)

> 4 измерения: **Тип** / **Система (SoI)** / **Содержание** / **Для кого**

| # | Репозиторий | Тип | Система | Содержание | Для кого | SoT | Статус |
|---|-------------|-----|---------|------------|----------|-----|--------|
| 0 | [ZP](https://github.com/TserenTserenov/ZP) | Foundation | cross-cutting | text-description | public | yes | Active |
| 1 | [FPF](https://github.com/ailev/FPF) | Framework | cross-cutting | text-description | public | yes | External |
| 21 | [aisystant](https://github.com/aisystant/aisystant) | Downstream/instrument | Экосистема | code | team | no | External |
| 22 | [SystemsSchool_bot](https://github.com/aisystant/SystemsSchool_bot) | Downstream/instrument | Экосистема | code | team | no | External |
| 2 | [SPF](https://github.com/TserenTserenov/SPF) | Framework | cross-cutting | text-description | public | yes | Active |
| 3 | [s2r](https://github.com/TserenTserenov/FMT-S2R) | Format | cross-cutting | text-description | public | yes | Active |
| 4 | [PACK-personal](https://github.com/aisystant/PACK-personal) | Pack | Созидатель | text-description | team | yes | Active |
| 5 | [PACK-ecosystem](https://github.com/TserenTserenov/PACK-ecosystem) | Pack | Экосистема | text-description | team | yes | Active |
| 6 | [PACK-digital-platform](https://github.com/TserenTserenov/PACK-digital-platform) | Pack | ИТ-платформа | text-description | team | yes | Active |
| 20 | [PACK-MIM](https://github.com/TserenTserenov/PACK-MIM) | Pack | МИМ (мастерская) | text-description | team | yes | Active |
| 24 | [PACK-education](https://github.com/TserenTserenov/PACK-education) | Pack | Методика обучения | text-description | team | yes | Active |
| — | ~~DS-aist-bot~~ | ~~Downstream/instrument~~ | — | — | — | — | Archived → aist_bot_newarchitecture |
| 8 | [DS-twin](https://github.com/aisystant/DS-twin) | Downstream/instrument | ИТ-платформа | code | team | no | Active |
| 9 | [DS-Knowledge-Index-Tseren](https://github.com/TserenTserenov/DS-Knowledge-Index-Tseren) | Downstream/instrument | Созидатель | code | personal | no | Active |
| 10 | [DS-ecosystem-development](https://github.com/aisystant/DS-ecosystem-development) | Downstream/governance | Экосистема | text-governance | team | no | Active |
| 11 | [DS-my-strategy](https://github.com/TserenTserenov/DS-my-strategy) | Downstream/governance | Созидатель | text-governance | personal | no | Active |
| 12 | [docs](https://github.com/aisystant/docs) | Downstream/surface | Экосистема | text-publication | public | no | Active |
| 13 | [DS-marathon-v2-tseren](https://github.com/TserenTserenov/DS-marathon-v2-tseren) | Downstream/surface | Экосистема | text-publication | team | no | Active |
| 14 | [FMT-exocortex-template](https://github.com/TserenTserenov/FMT-exocortex-template) | Format | cross-cutting | text-description | public | yes | Active |
| 15 | [DS-ai-systems](https://github.com/TserenTserenov/DS-ai-systems) | Downstream/instrument | ИТ-платформа | code | personal | no | Active |
| 18 | [digital-twin-mcp](https://github.com/aisystant/digital-twin-mcp) | Downstream/instrument | ИТ-платформа | code | team | no | Active |
| 19 | [aist_bot_newarchitecture](https://github.com/aisystant/aist_bot_newarchitecture) | Downstream/instrument | Бот Aist | code | team | no | Active |
| — | ~~DS-synchronizer~~ | ~~Downstream/instrument~~ | — | — | — | — | Archived → DS-ai-systems |
| — | ~~DS-fixer-agent~~ | ~~Downstream/instrument~~ | — | — | — | — | Archived → DS-ai-systems |
| — | ~~DS-pulse-agent~~ | ~~Downstream/instrument~~ | — | — | — | — | Archived → DS-ai-systems |

---

## По типам (детали)

### Foundation

| Репозиторий | Роль | Владелец |
|-------------|------|----------|
| [ZP](https://github.com/TserenTserenov/ZP) | Zeroth Principles (6 мета-ограничений + карта иерархии 0→1→2→3) | TserenTserenov |

### Framework & Format

| Репозиторий | Роль | Владелец |
|-------------|------|----------|
| [FPF](https://github.com/ailev/FPF) | First Principles Framework | ailev |
| [SPF](https://github.com/TserenTserenov/SPF) | Second Principles Framework | TserenTserenov |
| [FMT-S2R](https://github.com/TserenTserenov/FMT-S2R) | Structured Second-level Repository | TserenTserenov |
| [FMT-exocortex-template](https://github.com/TserenTserenov/FMT-exocortex-template) | Exocortex template (fork & deploy) | TserenTserenov |

### Pack (Source-of-truth)

| Репозиторий | Область | Upstream | Владелец |
|-------------|---------|----------|----------|
| [PACK-personal](https://github.com/aisystant/PACK-personal) | Созидатель (персональное развитие) | SPF, FPF | aisystant |
| [PACK-ecosystem](https://github.com/TserenTserenov/PACK-ecosystem) | Экосистема развития интеллекта (чёрный ящик + подсистемы) | SPF, FPF | TserenTserenov |
| [PACK-digital-platform](https://github.com/TserenTserenov/PACK-digital-platform) | ИТ-платформа и цифровой двойник | SPF, FPF, PACK-personal | TserenTserenov |
| [PACK-MIM](https://github.com/TserenTserenov/PACK-MIM) | Мастерская: форматы, программы, организация развития | SPF, FPF | TserenTserenov |
| [PACK-education](https://github.com/TserenTserenov/PACK-education) | Методика обучения: возрастные и профессиональные методы преподавания | SPF, FPF, PACK-personal | TserenTserenov |

### Downstream/instrument

| Репозиторий | Назначение | Upstream pack | Владелец |
|-------------|------------|---------------|----------|
| ~~DS-aist-bot~~ | ~~Archived → aist_bot_newarchitecture~~ | — | — |
| [DS-twin](https://github.com/aisystant/DS-twin) | MCP-сервис цифрового двойника | PACK-digital-platform, PACK-personal | aisystant |
| [DS-Knowledge-Index-Tseren](https://github.com/TserenTserenov/DS-Knowledge-Index-Tseren) | Персональный индекс знаний + публичные посты (`posts/`) | PACK-personal | TserenTserenov |
| [DS-ai-systems](https://github.com/TserenTserenov/DS-ai-systems) | Монорепо ИИ-систем (7 систем: стратег, экстрактор, синхронизатор, наладчик, статистик, оценщик, шаблонизатор) | PACK-digital-platform, PACK-personal | TserenTserenov |
| [digital-twin-mcp](https://github.com/aisystant/digital-twin-mcp) | MCP-сервер цифрового двойника | PACK-digital-platform, PACK-personal | aisystant |
| [aist_bot_newarchitecture](https://github.com/aisystant/aist_bot_newarchitecture) | Telegram-бот (new architecture, State Machine) | PACK-personal | aisystant |
| [aisystant](https://github.com/aisystant/aisystant) | LMS Aisystant (SYS.004) | PACK-ecosystem | aisystant (external) |
| [SystemsSchool_bot](https://github.com/aisystant/SystemsSchool_bot) | Telegram-бот стажировок и расписания | PACK-ecosystem | aisystant (external) |

### Downstream/governance

| Репозиторий | Назначение | Upstream packs | Владелец |
|-------------|------------|----------------|----------|
| [DS-ecosystem-development](https://github.com/aisystant/DS-ecosystem-development) | Координация экосистемы | PACK-ecosystem, PACK-personal, PACK-digital-platform | aisystant |
| [DS-my-strategy](https://github.com/TserenTserenov/DS-my-strategy) | Личное стратегирование (HUB агента Стратег) | PACK-personal, PACK-digital-platform | TserenTserenov |

### Downstream/surface

| Репозиторий | Назначение | Upstream pack | Владелец |
|-------------|------------|---------------|----------|
| [docs](https://github.com/aisystant/docs) | VitePress документация | PACK-personal, PACK-ecosystem | aisystant |
| [DS-marathon-v2-tseren](https://github.com/TserenTserenov/DS-marathon-v2-tseren) | Программа марафона v2 | PACK-personal, PACK-ecosystem | TserenTserenov |

---

## Граф зависимостей

```
ZP (Foundation, Level 0)
  │
  └──▶ FPF (ailev, Level 1)
        │
        └──▶ SPF (Framework, Level 2)
        │
        ├──▶ PACK-personal (Pack: Созидатель)
        │     │
        │     ├──▶ aist_bot_newarchitecture (Downstream/instrument)
        │     ├──▶ DS-twin (Downstream/instrument)
        │     ├──▶ DS-Knowledge-Index-Tseren (Downstream/instrument)
        │     ├──▶ docs (Downstream/surface)
        │     └──▶ DS-marathon-v2-tseren (Downstream/surface)
        │
        ├──▶ PACK-MIM (Pack: Мастерская)
        │     │
        │     └──▶ DS-ecosystem-development (Downstream/governance)
        │
        ├──▶ PACK-education (Pack: Методика обучения)
        │     │
        │     └──▶ (downstream TBD)
        │
        ├──▶ PACK-ecosystem (Pack: Экосистема — чёрный ящик)
        │     │
        │     ├──▶ DS-ecosystem-development (Downstream/governance)
        │     ├──▶ docs (Downstream/surface)
        │     └──▶ DS-marathon-v2-tseren (Downstream/surface)
        │
        ├──▶ PACK-digital-platform (Pack: ИТ-платформа)
        │     │
        │     ├──▶ DS-twin (Downstream/instrument)
        │     ├──▶ digital-twin-mcp (Downstream/instrument)
        │     ├──▶ DS-my-strategy (Downstream/governance — агент Стратег)
        │     └──▶ DS-ai-systems (Downstream/instrument — 7 ИИ-систем)
        │
        └──▶ FMT-S2R (Format)
              │
              └──▶ DS-ecosystem-development (Downstream/governance)

FMT-exocortex-template (Format)
  │
  └──▶ DS-ai-systems/setup (Downstream/instrument)
```

---

## Обязательный контракт

Каждый репозиторий экосистемы **ДОЛЖЕН** иметь:

### 1. Признак типа в README.md (первая строка после заголовка)

```markdown
> **Тип репозитория:** `Foundation` | `Pack` | `Framework` | `Format` | `Downstream/instrument` | `Downstream/governance` | `Downstream/surface`
```

### 2. Файл `REPO-TYPE.md` с 4D-полями:

```markdown
# Тип репозитория

**Тип**: `Foundation` | `Pack` | `Framework` | `Format` | `Downstream/instrument` | `Downstream/governance` | `Downstream/surface`
**Система (SoI)**: Созидатель | Экосистема | ИТ-платформа | Бот Aist | cross-cutting
**Содержание**: code | text-description | text-governance | text-publication
**Для кого**: personal | team | public
**Source-of-truth**: yes | no

## Upstream dependencies
- Список зависимостей

## Downstream outputs
- Что потребляет этот репозиторий

## Non-goals
- Что НЕ входит в scope
```

### 3. Покрытие REPO-TYPE.md

| Репозиторий | REPO-TYPE.md | 4D-поля |
|-------------|-------------|---------|
| ZP | — (minimal, no REPO-TYPE needed) | — |
| FPF | — (external) | — |
| SPF | yes | partial |
| FMT-S2R | yes | partial |
| PACK-personal | yes | partial |
| PACK-ecosystem | yes | partial |
| PACK-digital-platform | yes | partial |
| ~~DS-aist-bot~~ | — | — (→ aist_bot_newarchitecture) |
| DS-twin | yes | partial |
| DS-Knowledge-Index-Tseren | **yes** | **yes** |
| DS-ecosystem-development | yes | partial |
| DS-my-strategy | yes | yes |
| docs | **yes** | **yes** |
| DS-marathon-v2-tseren | **yes** | **yes** |
| FMT-exocortex-template | **yes** | **yes** |
| DS-ai-systems | **yes** | **yes** |
| digital-twin-mcp | yes | **yes** |
| aist_bot_newarchitecture | **yes** | **yes** |
| ~~DS-synchronizer~~ | — | — (→ DS-ai-systems) |

> **partial** = файл есть, но без полей Система/Содержание/Для кого. Обновить при следующем ревью.

---

## Правила

1. **Pack — единственный source-of-truth**. Downstream меняется вслед за pack
2. **Один репозиторий — один тип**. Не смешивать pack и downstream
3. **При изменении pack** — обновить downstream
4. **При добавлении репозитория** — обновить этот реестр
5. **При удалении репозитория** — обновить этот реестр
6. **REPO-TYPE.md обязателен** для всех репозиториев (кроме external)

---

*Последнее обновление: 2026-02-25*
