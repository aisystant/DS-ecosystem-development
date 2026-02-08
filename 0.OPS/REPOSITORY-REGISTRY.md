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
| 3 | [s2r](https://github.com/TserenTserenov/s2r) | Format | cross-cutting | text-description | public | yes | Active |
| 4 | [spf-personal-pack](https://github.com/aisystant/spf-personal-pack) | Pack | Созидатель | text-description | team | yes | Active |
| 5 | [spf-ecosystem-pack](https://github.com/TserenTserenov/spf-ecosystem-pack) | Pack | Экосистема | text-description | team | yes | Active |
| 6 | [spf-digital-platform-pack](https://github.com/TserenTserenov/spf-digital-platform-pack) | Pack | ИТ-платформа | text-description | team | yes | Active |
| 7 | [aist_bot](https://github.com/aisystant/aist_bot) | Downstream/instrument | Бот Aist | code | team | no | Active |
| 8 | [aist_bot_newarchitecture](https://github.com/aisystant/aist_bot) | Downstream/instrument | Бот Aist | code | team | no | Active |
| 9 | [digital-twin-mcp](https://github.com/aisystant/digital-twin-mcp) | Downstream/instrument | ИТ-платформа | code | team | no | Active |
| 10 | [Knowledge-Index-Tseren](https://github.com/TserenTserenov/Knowledge-Index-Tseren) | Downstream/instrument | Созидатель | code | personal | no | Active |
| 11 | [ecosystem-development](https://github.com/aisystant/ecosystem-development) | Downstream/governance | Экосистема | text-governance | team | no | Active |
| 12 | [my-strategy](https://github.com/TserenTserenov/my-strategy) | Downstream/governance | Созидатель | text-governance | personal | no | Active |
| 13 | [docs](https://github.com/aisystant/docs) | Downstream/surface | Экосистема | text-publication | public | no | Active |
| 14 | [marathon-v2-tseren](https://github.com/TserenTserenov/marathon-v2-tseren) | Downstream/surface | Экосистема | text-publication | team | no | Active |

---

## По типам (детали)

### Framework & Format

| Репозиторий | Роль | Владелец |
|-------------|------|----------|
| [FPF](https://github.com/ailev/FPF) | First Principles Framework | ailev |
| [SPF](https://github.com/TserenTserenov/SPF) | Second Principles Framework | TserenTserenov |
| [s2r](https://github.com/TserenTserenov/s2r) | Structured Second-level Repository | TserenTserenov |

### Pack (Source-of-truth)

| Репозиторий | Область | Upstream | Владелец |
|-------------|---------|----------|----------|
| [spf-personal-pack](https://github.com/aisystant/spf-personal-pack) | Созидатель (персональное развитие) | SPF, FPF | aisystant |
| [spf-ecosystem-pack](https://github.com/TserenTserenov/spf-ecosystem-pack) | Экосистема развития интеллекта | SPF, FPF | TserenTserenov |
| [spf-digital-platform-pack](https://github.com/TserenTserenov/spf-digital-platform-pack) | ИТ-платформа и цифровой двойник | SPF, FPF, spf-personal-pack | TserenTserenov |

### Downstream/instrument

| Репозиторий | Назначение | Upstream pack | Владелец |
|-------------|------------|---------------|----------|
| [aist_bot](https://github.com/aisystant/aist_bot) | Telegram-бот марафона (production) | spf-personal-pack | aisystant |
| [aist_bot_newarchitecture](https://github.com/aisystant/aist_bot) | Telegram-бот марафона (State Machine) | spf-personal-pack | aisystant |
| [digital-twin-mcp](https://github.com/aisystant/digital-twin-mcp) | MCP-сервис цифрового двойника | spf-digital-platform-pack, spf-personal-pack | aisystant |
| [Knowledge-Index-Tseren](https://github.com/TserenTserenov/Knowledge-Index-Tseren) | Персональный индекс знаний | spf-personal-pack | TserenTserenov |

### Downstream/governance

| Репозиторий | Назначение | Upstream packs | Владелец |
|-------------|------------|----------------|----------|
| [ecosystem-development](https://github.com/aisystant/ecosystem-development) | Координация экосистемы | spf-ecosystem-pack, spf-personal-pack, spf-digital-platform-pack | aisystant |
| [my-strategy](https://github.com/TserenTserenov/my-strategy) | Личное стратегирование (HUB агента Стратег) | spf-personal-pack, spf-digital-platform-pack | TserenTserenov |

### Downstream/surface

| Репозиторий | Назначение | Upstream pack | Владелец |
|-------------|------------|---------------|----------|
| [docs](https://github.com/aisystant/docs) | VitePress документация | spf-personal-pack, spf-ecosystem-pack | aisystant |
| [marathon-v2-tseren](https://github.com/TserenTserenov/marathon-v2-tseren) | Программа марафона v2 | spf-personal-pack, spf-ecosystem-pack | TserenTserenov |

---

## Граф зависимостей

```
FPF (ailev)
  │
  └──▶ SPF (Framework)
        │
        ├──▶ spf-personal-pack (Pack: Созидатель)
        │     │
        │     ├──▶ aist_bot (Downstream/instrument)
        │     ├──▶ aist_bot_newarchitecture (Downstream/instrument)
        │     ├──▶ digital-twin-mcp (Downstream/instrument)
        │     ├──▶ Knowledge-Index-Tseren (Downstream/instrument)
        │     ├──▶ docs (Downstream/surface)
        │     └──▶ marathon-v2-tseren (Downstream/surface)
        │
        ├──▶ spf-ecosystem-pack (Pack: Экосистема)
        │     │
        │     ├──▶ ecosystem-development (Downstream/governance)
        │     ├──▶ docs (Downstream/surface)
        │     └──▶ marathon-v2-tseren (Downstream/surface)
        │
        ├──▶ spf-digital-platform-pack (Pack: ИТ-платформа)
        │     │
        │     ├──▶ digital-twin-mcp (Downstream/instrument)
        │     └──▶ my-strategy (Downstream/governance — агент Стратег)
        │
        └──▶ s2r (Format)
              │
              └──▶ ecosystem-development (Downstream/governance)
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
| s2r | yes | partial |
| spf-personal-pack | yes | partial |
| spf-ecosystem-pack | yes | partial |
| spf-digital-platform-pack | yes | partial |
| aist_bot | yes | partial |
| aist_bot_newarchitecture | **yes** | **yes** |
| digital-twin-mcp | yes | partial |
| Knowledge-Index-Tseren | **yes** | **yes** |
| ecosystem-development | yes | partial |
| my-strategy | yes | yes |
| docs | **yes** | **yes** |
| marathon-v2-tseren | **yes** | **yes** |

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

*Последнее обновление: 2026-02-08*
