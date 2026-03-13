---
type: reference
family: F8
cell: "B2.2"
status: active
created: 2026-02-07
source_of_truth: PACK-digital-platform
---

# B2.2. Архитектура ИТ-платформы

> **Source-of-truth**: [PACK-digital-platform](../../../../PACK-digital-platform/pack/digital-platform/02-domain-entities/)
>
> Формализованное знание об ИТ-платформе находится в Pack-репозитории.
> Этот документ содержит **ссылки и реестр** объектов внимания.

---

## Назначение

Этот раздел описывает **архитектуру ИТ-платформы экосистемы** — слоистую структуру, детерминированные системы, ИИ-ассистенты и агенты.

---

## Реестр моделей

| Модель | Описание | Source-of-truth |
|--------|----------|-----------------
| **Архитектура платформы** | 5-слойная структура | [DP.ARCH.001](../../../../PACK-digital-platform/pack/digital-platform/02-domain-entities/DP.ARCH.001-platform-architecture.md) |
| **Концепция платформы** | Что даёт пользователю | [DP.CONCEPT.001](../../../../PACK-digital-platform/pack/digital-platform/02-domain-entities/DP.CONCEPT.001-platform-concept.md) |
| **Детерминированные системы** | 14 систем инфраструктуры | [DP.SYS.001](../../../../PACK-digital-platform/pack/digital-platform/02-domain-entities/DP.SYS.001-deterministic-systems.md) |
| **ИИ-агенты** | 17 системных агентов | [DP.ROLE.001](../../../../PACK-digital-platform/pack/digital-platform/02-domain-entities/DP.ROLE.001-platform-roles.md) |
| **ИИ-ассистенты** | Диалоговые помощники | [DP.ASSIST.001](../../../../PACK-digital-platform/pack/digital-platform/02-domain-entities/DP.ASSIST.001-ai-assistants.md) |

---

## Governance-контент (остаётся здесь)

### Подразделы

| Подраздел | Назначение |
|-----------|------------|
| 2.2.1. IT-Platform-Concept | Пользовательский взгляд |
| 2.2.2. Architectural-Decisions | Технические решения |
| 2.2.3. Deterministic-IT-Systems | 14 систем |
| 2.2.4. AI-Assistants | Диалоговые интерфейсы |
| 2.2.5. AI-Agents | Автономные агенты |
| 2.2.6. Data-Stores | Данные и storage |

### Реестр ИТ-систем (Governance)

| Система | Статус | Репозиторий |
|---------|--------|-------------|
| Цифровой двойник | Active | DS-twin |
| LMS (Aisystant) | Active | — |
| Клуб | Active | — |
| Aist Bot | Active | aist_bot |

---

## Миграция

**Статус миграции:** Частично завершена

| Элемент | Статус | Целевой Pack |
|---------|--------|--------------|
| Архитектура платформы | ✅ Мигрирован | PACK-digital-platform |
| Концепция платформы | ✅ Мигрирован | PACK-digital-platform |
| Детерминированные системы | ✅ Мигрирован | PACK-digital-platform |
| ИИ-агенты | 🟡 Stub | PACK-digital-platform |
| ИИ-ассистенты | 🟡 Stub | PACK-digital-platform |
| Детали систем | 🔴 TODO | PACK-digital-platform |

---

*Последнее обновление: 2026-02-07*
