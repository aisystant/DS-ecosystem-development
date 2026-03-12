# Ядро D: Aist-Bot (Telegram-бот персонального маршрута)

> **Downstream-артефакт** в архитектуре FPF/SPF/Pack. Source-of-truth: [aisystant/spf-personal](https://github.com/aisystant/spf-personal)

## Обзор ядра

**SoI (Система интереса)**: Telegram-бот — персональный помощник для развития системного мышления через регулярную практику.

**Репозиторий бота**: [github.com/aisystant/aist_bot](https://github.com/aisystant/aist_bot) (ветка `new-architecture`)

## Системная структура ядра D (S2R)

```
D.Aist-Bot/
├── D0.Aist-Bot-Management/           # Управление ядром
│   └── 01-kernel-overview.md         # Обзор ядра
│
├── D1.IT-Platform/                   # Надсистема (+ Cyberidentity)
│   ├── D1.1.Meaning/                 # Контекст надсистем
│   ├── D1.2.Architecture/
│   │   ├── IT-Platform/              # Надсистема 1: ИТ-платформа
│   │   └── Cyberidentity/            # Надсистема 2: Киберличность
│   └── D1.3.Operations/
│
├── D2.Aist-Bot/                      # SoI: сам бот
│   ├── D2.1.Meaning/                 # Миссия, ценность, пользователи
│   ├── D2.2.Architecture/            # Режимы, структура, State Machine
│   └── D2.3.Operations/              # Команды, сценарии, процессы
│
└── D3.Dev-Team/                      # Система создания: команда
    ├── D3.1.Meaning/
    ├── D3.2.Architecture/            # Роли, инструменты
    └── D3.3.Operations/              # Процесс разработки, деплой
```

### Две надсистемы бота

| Надсистема | Роль бота | Связь с ядрами |
|------------|-----------|----------------|
| **IT-Platform** | Компонент ИТ-инфраструктуры | C.IT-Platform |
| **Cyberidentity** | Часть цифрового "я", элемент экзокортекса | A.Systems-Builder |

## Позиционирование в архитектуре знаний

| Уровень | Репозиторий | Роль |
|---------|-------------|------|
| FPF | [ailev/FPF](https://github.com/ailev/FPF) | Мета-онтология |
| SPF + Pack | [aisystant/spf-personal](https://github.com/aisystant/spf-personal) | Source-of-truth |
| **Downstream** | **Этот бот** | Производное представление |

## Два режима работы

### 1. Марафон (Marathon)
- 14-дневная структурированная программа
- 28 тем: 2 урока в день (теория + практика)
- Переход от хаоса → к системным практикам → к роли созидателя

### 2. Лента (Feed)
- Гибкий формат по выбранным темам
- Дайджесты в удобном ритме
- До 3 тем одновременно

## Технологический стек

- Python 3.11 + aiogram 3.x
- Anthropic Claude API
- PostgreSQL
- Railway / Render

## Ключевые документы

- [[D0.Aist-Bot-Management/01-kernel-overview.md]] — обзор ядра
- [[D2.1.Meaning/01-mission.md]] — миссия и ценность
- [[D2.2.Architecture/01-modes.md]] — режимы работы
- [[D2.2.Architecture/02-marathon-structure.md]] — 14 дней, 28 тем
- [[D2.3.Operations/01-commands.md]] — команды бота

## Связь с другими ядрами

- **C.IT-Platform** — бот как компонент ИТ-платформы
- **A.Systems-Builder** — бот для развития созидателя
- **B.Aisystant-Ecosystem** — часть экосистемы Aisystant

## См. также

- [Онтология бота](https://github.com/aisystant/aist_bot/blob/new-architecture/docs/ontology.md)
- [[0.OPS/0.1.Knowledge-Logic/01-kernels-model.md]] — модель ядер S2R
- [[0.OPS/0.1.Knowledge-Logic/10-knowledge-architecture.md]] — архитектура знаний
