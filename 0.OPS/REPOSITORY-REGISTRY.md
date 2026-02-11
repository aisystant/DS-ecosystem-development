# Реестр репозиториев экосистемы

> **Source-of-truth** для списка репозиториев экосистемы развития интеллекта.
> Обновляется при создании/удалении репозиториев.

## Типы репозиториев (4 типа)

| Тип | Критерий | Source-of-truth |
|-----|----------|-----------------|
| **Pack** | Source-of-truth области (что истинно и как проверять) | Да |
| **Framework** | Рамки корректности (FPF/SPF) | Да |
| **Format** | Протокол оформления | Да (для формата) |
| **Downstream** | Производные от Pack | Нет |

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
| 1 | [FPF](https://github.com/ailev/FPF) | Framework | cross-cutting | text-description | public | yes | External |
| 2 | [SPF](https://github.com/TserenTserenov/SPF) | Framework | cross-cutting | text-description | public | yes | Active |
| 3 | [s2r](https://github.com/TserenTserenov/FMT-S2R) | Format | cross-cutting | text-description | public | yes | Active |
| 4 | [PACK-personal](https://github.com/aisystant/PACK-personal) | Pack | Созидатель | text-description | team | yes | Active |
| 5 | [PACK-ecosystem](https://github.com/TserenTserenov/PACK-ecosystem) | Pack | Экосистема | text-description | team | yes | Active |
| 6 | [PACK-digital-platform](https://github.com/TserenTserenov/PACK-digital-platform) | Pack | ИТ-платформа | text-description | team | yes | Active |
| 7 | [DS-aist-bot](https://github.com/aisystant/DS-aist-bot) | Downstream/instrument | Бот Aist | code | team | no | Active |
| 8 | [DS-twin](https://github.com/aisystant/DS-twin) | Downstream/instrument | ИТ-платформа | code | team | no | Active |
| 9 | [DS-Knowledge-Index-Tseren](https://github.com/TserenTserenov/DS-Knowledge-Index-Tseren) | Downstream/instrument | Созидатель | code | personal | no | Active |
| 10 | [DS-ecosystem-development](https://github.com/aisystant/DS-ecosystem-development) | Downstream/governance | Экосистема | text-governance | team | no | Active |
| 11 | [DS-my-strategy](https://github.com/TserenTserenov/DS-my-strategy) | Downstream/governance | Созидатель | text-governance | personal | no | Active |
| 12 | [docs](https://github.com/aisystant/docs) | Downstream/surface | Экосистема | text-publication | public | no | Active |
| 13 | [DS-marathon-v2-tseren](https://github.com/TserenTserenov/DS-marathon-v2-tseren) | Downstream/surface | Экосистема | text-publication | team | no | Active |
| 14 | [FMT-exocortex-template](https://github.com/TserenTserenov/FMT-exocortex-template) | Format | cross-cutting | text-description | public | yes | Active |
| 15 | [DS-exocortex-setup-agent](https://github.com/TserenTserenov/DS-exocortex-setup-agent) | Downstream/instrument | cross-cutting | code | public | no | Active |
| 16 | [DS-strategist-agent](https://github.com/TserenTserenov/DS-strategist-agent) | Downstream/instrument | Созидатель | code | personal | no | Active |
| 17 | [DS-extractor-agent](https://github.com/TserenTserenov/DS-extractor-agent) | Downstream/instrument | ИТ-платформа | code | personal | no | Active |
| 18 | [digital-twin-mcp](https://github.com/aisystant/digital-twin-mcp) | Downstream/instrument | ИТ-платформа | code | team | no | Active |
| 19 | [aist_bot_newarchitecture](https://github.com/aisystant/aist_bot_newarchitecture) | Downstream/instrument | Бот Aist | code | team | no | Active |

---

## По типам (детали)

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
| [PACK-ecosystem](https://github.com/TserenTserenov/PACK-ecosystem) | Экосистема развития интеллекта | SPF, FPF | TserenTserenov |
| [PACK-digital-platform](https://github.com/TserenTserenov/PACK-digital-platform) | ИТ-платформа и цифровой двойник | SPF, FPF, PACK-personal | TserenTserenov |

### Downstream/instrument

| Репозиторий | Назначение | Upstream pack | Владелец |
|-------------|------------|---------------|----------|
| [DS-aist-bot](https://github.com/aisystant/DS-aist-bot) | Telegram-бот марафона (production + State Machine) | PACK-personal | aisystant |
| [DS-twin](https://github.com/aisystant/DS-twin) | MCP-сервис цифрового двойника | PACK-digital-platform, PACK-personal | aisystant |
| [DS-Knowledge-Index-Tseren](https://github.com/TserenTserenov/DS-Knowledge-Index-Tseren) | Персональный индекс знаний + публичные посты (`posts/`) | PACK-personal | TserenTserenov |
| [DS-exocortex-setup-agent](https://github.com/TserenTserenov/DS-exocortex-setup-agent) | Агент развёртывания экзокортекса | FMT-exocortex-template | TserenTserenov |
| [DS-strategist-agent](https://github.com/TserenTserenov/DS-strategist-agent) | Агент стратегирования | PACK-personal, PACK-digital-platform | TserenTserenov |
| [DS-extractor-agent](https://github.com/TserenTserenov/DS-extractor-agent) | Агент извлечения знаний | PACK-digital-platform | TserenTserenov |
| [digital-twin-mcp](https://github.com/aisystant/digital-twin-mcp) | MCP-сервер цифрового двойника | PACK-digital-platform, PACK-personal | aisystant |
| [aist_bot_newarchitecture](https://github.com/aisystant/aist_bot_newarchitecture) | Telegram-бот (new architecture, State Machine) | PACK-personal | aisystant |

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
FPF (ailev)
  │
  └──▶ SPF (Framework)
        │
        ├──▶ PACK-personal (Pack: Созидатель)
        │     │
        │     ├──▶ DS-aist-bot (Downstream/instrument)
        │     ├──▶ aist_bot_newarchitecture (Downstream/instrument)
        │     ├──▶ DS-twin (Downstream/instrument)
        │     ├──▶ DS-Knowledge-Index-Tseren (Downstream/instrument)
        │     ├──▶ docs (Downstream/surface)
        │     └──▶ DS-marathon-v2-tseren (Downstream/surface)
        │
        ├──▶ PACK-ecosystem (Pack: Экосистема)
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
        │     ├──▶ DS-strategist-agent (Downstream/instrument — агент)
        │     └──▶ DS-extractor-agent (Downstream/instrument — агент)
        │
        └──▶ FMT-S2R (Format)
              │
              └──▶ DS-ecosystem-development (Downstream/governance)

FMT-exocortex-template (Format)
  │
  └──▶ DS-exocortex-setup-agent (Downstream/instrument)
```

---

## Обязательный контракт

Каждый репозиторий экосистемы **ДОЛЖЕН** иметь:

### 1. Признак типа в README.md (первая строка после заголовка)

```markdown
> **Тип репозитория:** `Pack` | `Framework` | `Format` | `Downstream/instrument` | `Downstream/governance` | `Downstream/surface`
```

### 2. Файл `REPO-TYPE.md` с 4D-полями:

```markdown
# Тип репозитория

**Тип**: `Pack` | `Framework` | `Format` | `Downstream/instrument` | `Downstream/governance` | `Downstream/surface`
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
| FPF | — (external) | — |
| SPF | yes | partial |
| FMT-S2R | yes | partial |
| PACK-personal | yes | partial |
| PACK-ecosystem | yes | partial |
| PACK-digital-platform | yes | partial |
| DS-aist-bot | **yes** | **yes** |
| DS-twin | yes | partial |
| DS-Knowledge-Index-Tseren | **yes** | **yes** |
| DS-ecosystem-development | yes | partial |
| DS-my-strategy | yes | yes |
| docs | **yes** | **yes** |
| DS-marathon-v2-tseren | **yes** | **yes** |
| FMT-exocortex-template | **yes** | **yes** |
| DS-exocortex-setup-agent | **yes** | **yes** |
| DS-strategist-agent | **yes** | **yes** |
| DS-extractor-agent | **yes** | **yes** |
| digital-twin-mcp | no | no |
| aist_bot_newarchitecture | no | no |

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

*Последнее обновление: 2026-02-11*
