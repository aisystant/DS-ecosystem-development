---

type: doc
audience: mixed
edit_mode: manual
layer: service
scope: external
security: internal
status: draft
version: 0.1
created: 2025-12-21
---

# Интеграция с LLM Apps SDK: Единый интерфейс входа в экосистему

Использование Apps SDK от производителей LLM (OpenAI, Anthropic, Google) как универсального интерфейса для взаимодействия участников с ИИ-платформой экосистемы развития интеллекта.

## Стратегическое видение

### Проблема

Участники экосистемы используют разные ИИ-интерфейсы для взаимодействия:
- ChatGPT (OpenAI)
- Claude (Anthropic)
- Gemini (Google)
- Локальные модели

Каждый участник уже имеет привычный интерфейс. Заставлять всех переходить на собственную платформу — создавать лишний барьер входа.

### Решение

**Использовать LLM Apps SDK как "розетки" для подключения к экосистеме** — участник работает в привычном ChatGPT/Claude/Gemini, но получает полный доступ к функционалу экосистемы развития.

```
┌─────────────────────────────────────────────────────────────────┐
│                    УЧАСТНИК ЭКОСИСТЕМЫ                          │
│                 (использует привычный LLM)                      │
└─────────────────────────────────────────────────────────────────┘
                              │
           ┌──────────────────┼──────────────────┐
           │                  │                  │
           ▼                  ▼                  ▼
    ┌──────────────┐   ┌──────────────┐   ┌──────────────┐
    │   ChatGPT    │   │    Claude    │   │   Gemini     │
    │  (OpenAI     │   │  (Anthropic  │   │  (Google     │
    │  Apps SDK)   │   │     MCP)     │   │ Extensions)  │
    └──────────────┘   └──────────────┘   └──────────────┘
           │                  │                  │
           └──────────────────┼──────────────────┘
                              │
                    ┌─────────▼─────────┐
                    │   MCP GATEWAY     │
                    │   (единый слой)   │
                    └─────────┬─────────┘
                              │
    ┌─────────────────────────┼─────────────────────────┐
    │              ЭКОСИСТЕМА РАЗВИТИЯ                   │
    │  ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐  │
    │  │ Digital │ │ Memory  │ │  Token  │ │   LMS   │  │
    │  │  Twin   │ │  Bank   │ │ Economy │ │         │  │
    │  └─────────┘ └─────────┘ └─────────┘ └─────────┘  │
    └───────────────────────────────────────────────────┘
```

### Почему MCP — универсальный протокол

**Model Context Protocol (MCP)** стал стандартом индустрии:
- **OpenAI Apps SDK** построен на MCP
- **Anthropic Claude** — создатель и главный драйвер MCP
- **Google Gemini** — объявил поддержку MCP в 2025
- **Linux Foundation** — MCP передан в Agentic AI Foundation (декабрь 2025)

Экосистема может создать **один MCP-сервер**, который будет работать через все три платформы.

---

## Ландшафт LLM Apps SDK (2025)

### 1. OpenAI Apps SDK

**Статус:** Beta, submissions открыты (октябрь 2025)

**Архитектура:**
- **MCP Server** — определяет tools (возможности) для ChatGPT
- **Web Widget** — iframe-компонент для UI в ChatGPT
- **OAuth 2.1** — аутентификация пользователей

**Ключевые возможности:**
- Tools — действия, которые выполняет приложение
- Templates — шаблоны ответов
- Widget Runtime — рендеринг UI в ChatGPT

**Публикация:** Через OpenAI Developer Platform, модерация и review

### 2. Anthropic MCP + Integrations

**Статус:** Production, MCP Connector в API

**Архитектура:**
- **Remote MCP Servers** — сторонние сервера с инструментами
- **MCP Connector API** — автоматическое подключение к серверам
- **Pre-built Integrations** — Jira, Confluence, GitHub, Slack и др.

**Ключевые возможности:**
- Стандартный протокол для любых интеграций
- Обработка OAuth, tool discovery, error handling на стороне Anthropic
- Marketplace интеграций в Claude

### 3. Google Gemini Extensions + Interactions API

**Статус:** Production (CLI Extensions), Beta (Interactions API)

**Архитектура:**
- **CLI Extensions** — playbooks для интеграции с внешними инструментами
- **Interactions API** — единый REST endpoint для моделей и агентов
- **Connected Apps** — интеграции с Google-сервисами

**Ключевые возможности:**
- MCP-совместимые extensions
- Поддержка Figma, Shopify, Stripe, Postman и др.
- Custom agents через Interactions API

---

## Сценарии использования для экосистемы

### Сценарий 1: Персональная траектория развития

**Пользователь:** Ученик на начальном этапе

**Интерфейс:** ChatGPT / Claude / Gemini

**Диалог:**
```
Участник: @Aisystant, покажи мою траекторию развития

Ассистент: [Подключается к Digital Twin через MCP]

📊 Твоя траектория развития:

🎯 Текущий уровень: Ученик (EQF 1)
📈 Прогресс: 23% к уровню Интеллектуал

Следующие шаги:
1. [Завершить] Урок 3.2: Системное мышление (осталось 40 мин)
2. [Практика] Построить модель целей по шаблону
3. [Рефлексия] Еженедельный ревью (воскресенье)

💡 Рекомендация на сегодня:
Пройди урок 3.2 — он критически важен для понимания
следующих тем. Estimated time: 40 минут.

[Начать урок] [Изменить план] [Показать календарь]
```

**MCP Tools:**
```json
{
  "tools": [
    {
      "name": "get_learning_trajectory",
      "description": "Получить персональную траекторию развития участника",
      "parameters": {
        "user_id": "string",
        "include_recommendations": "boolean"
      }
    },
    {
      "name": "get_next_best_action",
      "description": "Рекомендация следующего действия",
      "parameters": {
        "user_id": "string",
        "context": "string (time_available, energy_level)"
      }
    },
    {
      "name": "start_learning_session",
      "description": "Начать сессию обучения",
      "parameters": {
        "lesson_id": "string",
        "estimated_duration": "integer"
      }
    }
  ]
}
```

---

### Сценарий 2: Токен-экономика и Solana

**Пользователь:** Активный участник экосистемы

**Диалог:**
```
Участник: @Aisystant, сколько токенов я заработал на этой неделе?

Ассистент: [Подключается к Token Economy + Solana через MCP]

💰 Твой баланс STK:

┌─────────────────────────────────────────┐
│  Текущий баланс: 4,250 STK             │
│  Эта неделя:     +1,584 STK            │
│  Кошелёк Solana: 8xK2...9fD3           │
└─────────────────────────────────────────┘

📊 Разбивка недели:
• Чтение разделов (5): 250 баллов
• Выполнение заданий (3): 300 баллов
• Пост в сообществе (1): 200 баллов
• Лайки полученные (10): 200 баллов
• Бонус систематичности (4 недели): ×1.10

Твой коэффициент квалификации: ×1.5 (Практик)

🔗 [Открыть в Solana Explorer] [История транзакций]
```

**MCP Tools:**
```json
{
  "tools": [
    {
      "name": "get_token_balance",
      "description": "Получить баланс STK токенов",
      "parameters": {
        "user_id": "string",
        "include_history": "boolean"
      }
    },
    {
      "name": "get_weekly_rewards",
      "description": "Детализация начислений за неделю",
      "parameters": {
        "user_id": "string",
        "week_offset": "integer"
      }
    },
    {
      "name": "get_solana_wallet",
      "description": "Информация о кошельке Solana",
      "parameters": {
        "user_id": "string"
      }
    },
    {
      "name": "transfer_tokens",
      "description": "Перевод токенов другому участнику",
      "parameters": {
        "from_user_id": "string",
        "to_user_id": "string",
        "amount": "integer",
        "reason": "string"
      }
    }
  ]
}
```

---

### Сценарий 3: Эпистемологический статус и публикации

**Пользователь:** Профессионал, строящий репутацию

**Диалог:**
```
Участник: @Aisystant, покажи мой эпистемический профиль

Ассистент: [Подключается к Epistemic Graph через MCP]

🎓 Эпистемический профиль: @username

┌─────────────────────────────────────────────────────┐
│  Квалификация: Профессионал (EQF 4)                │
│  Срок действия: до 2027-03-15                       │
│  Коэффициент STK: ×1.8                              │
└─────────────────────────────────────────────────────┘

📚 Публикации (5):
• "Системный подход к архитектуре" — peer-reviewed ✓
• "Холонические модели в практике" — verified 10+ uses
• "Методология ADI-цикла" — production use

🔨 Создаваемые системы (3):
• Project Alpha — в разработке (60%)
• Training Platform v2 — production
• MCP Integration — MVP

🌐 Активность в экосистеме:
• Менторство: 12 сессий (средний рейтинг 4.8)
• Ответы в сообществе: 47 (23 отмечены полезными)
• Курирование учеников: 3 активных

📈 Репутационный индекс: 847 / 1000

[Обновить профиль] [Добавить публикацию] [Запросить повышение]
```

**MCP Tools:**
```json
{
  "tools": [
    {
      "name": "get_epistemic_profile",
      "description": "Полный эпистемический профиль участника",
      "parameters": {
        "user_id": "string"
      }
    },
    {
      "name": "list_publications",
      "description": "Список публикаций и их статус",
      "parameters": {
        "user_id": "string",
        "status_filter": "string (all, verified, peer_reviewed)"
      }
    },
    {
      "name": "list_created_systems",
      "description": "Системы, создаваемые участником",
      "parameters": {
        "user_id": "string"
      }
    },
    {
      "name": "get_reputation_breakdown",
      "description": "Детализация репутационного индекса",
      "parameters": {
        "user_id": "string"
      }
    },
    {
      "name": "submit_publication",
      "description": "Добавить публикацию для верификации",
      "parameters": {
        "user_id": "string",
        "title": "string",
        "url": "string",
        "type": "string (article, code, system)"
      }
    }
  ]
}
```

---

### Сценарий 4: Привлечение новых участников (реферальная система)

**Пользователь:** Активный участник, развивающий экосистему

**Диалог:**
```
Участник: @Aisystant, как мне пригласить коллегу в экосистему?

Ассистент: [Подключается к Referral + Onboarding через MCP]

🎁 Реферальная программа

Твоя персональная ссылка:
https://aisystant.com/join/ref-8xK2f9D3

При регистрации по ссылке:
• Новый участник получает: +100 STK бонус
• Ты получаешь: +50 STK за каждого

📊 Твоя статистика приглашений:
• Приглашено: 7 человек
• Активных: 4 человека
• Заработано: 350 STK

💡 Совет: Наибольшая конверсия — когда ты делишься
конкретным полезным материалом + ссылкой.

Хочешь, сгенерирую пост для LinkedIn с описанием
твоего опыта в экосистеме?

[Создать пост] [Скопировать ссылку] [QR-код]
```

**MCP Tools:**
```json
{
  "tools": [
    {
      "name": "get_referral_link",
      "description": "Получить персональную реферальную ссылку",
      "parameters": {
        "user_id": "string"
      }
    },
    {
      "name": "get_referral_stats",
      "description": "Статистика приглашений",
      "parameters": {
        "user_id": "string"
      }
    },
    {
      "name": "generate_invitation_content",
      "description": "Сгенерировать контент для приглашения",
      "parameters": {
        "user_id": "string",
        "platform": "string (linkedin, telegram, twitter)",
        "style": "string (professional, casual)"
      }
    }
  ]
}
```

---

### Сценарий 5: Изучение руководств и материалов

**Пользователь:** Любой участник

**Диалог:**
```
Участник: @Aisystant, объясни холонический принцип из FPF

Ассистент: [Подключается к Memory Bank через MCP]

📖 Холонический принцип (FPF Part A.1)

Холон — это нечто, что одновременно является:
• Целым (автономная единица)
• Частью большей системы

┌──────────────────────────────────────────┐
│     Организация                          │
│  ┌────────────────────────────────────┐  │
│  │   Отдел                            │  │
│  │  ┌──────────────────────────────┐  │  │
│  │  │   Команда                    │  │  │
│  │  │  ┌────────────────────────┐  │  │  │
│  │  │  │  Человек (созидатель)  │  │  │  │
│  │  │  └────────────────────────┘  │  │  │
│  │  └──────────────────────────────┘  │  │
│  └────────────────────────────────────┘  │
└──────────────────────────────────────────┘

Каждый уровень — холон: целый для нижних уровней
и часть для верхних.

📚 Связанные материалы:
• Bounded Context (A.1.1) — значение локально
• Strict Distinction (A.7) — роль ≠ метод ≠ работа

🎯 Практика:
Попробуй описать свою команду как холон. Что делает
её целой? Частью чего она является?

[Перейти к практике] [Следующий принцип] [Все принципы]
```

**MCP Tools:**
```json
{
  "tools": [
    {
      "name": "search_knowledge",
      "description": "Поиск в базе знаний экосистемы",
      "parameters": {
        "query": "string",
        "source": "string (fpf, courses, community)"
      }
    },
    {
      "name": "get_fpf_section",
      "description": "Получить раздел FPF спецификации",
      "parameters": {
        "section_id": "string",
        "include_examples": "boolean"
      }
    },
    {
      "name": "get_related_materials",
      "description": "Связанные материалы по теме",
      "parameters": {
        "topic": "string",
        "limit": "integer"
      }
    },
    {
      "name": "start_practice",
      "description": "Начать практическое задание",
      "parameters": {
        "practice_id": "string",
        "user_id": "string"
      }
    }
  ]
}
```

---

### Сценарий 6: Активные действия с начислением токенов

**Пользователь:** Участник выполняет задание

**Диалог:**
```
Участник: @Aisystant, отправляю выполненное задание по системному мышлению

Ассистент: [Подключается к Activity Hub + Proof-of-Impact через MCP]

📝 Принято! Задание на проверке.

┌─────────────────────────────────────────────────────┐
│  Задание: Построение системной модели цели         │
│  Статус: ⏳ На проверке                             │
│  Ожидаемые баллы: 100                              │
└─────────────────────────────────────────────────────┘

Что происходит:
1. ✅ Артефакт загружен в Activity Hub
2. ⏳ Автоматическая проверка качества
3. ⏳ Peer review (опционально)
4. ⏳ Начисление токенов

⏱️ Обычно проверка занимает 10-30 минут.

Уведомить тебя, когда результат будет готов?

[Да, уведомить] [Посмотреть другие задания]

---

[Через 15 минут]

🎉 Задание принято!

• Баллы: 100
• Коэффициент квалификации: ×1.5
• Начислено: 150 STK

💡 Feedback: Хорошо выделены ключевые стейкхолдеры.
Рекомендуем добавить анализ ограничений в следующий раз.

[Следующее задание] [Мой прогресс]
```

**MCP Tools:**
```json
{
  "tools": [
    {
      "name": "submit_work_artifact",
      "description": "Отправить выполненную работу",
      "parameters": {
        "user_id": "string",
        "assignment_id": "string",
        "content": "string",
        "attachments": "array"
      }
    },
    {
      "name": "get_submission_status",
      "description": "Статус проверки работы",
      "parameters": {
        "submission_id": "string"
      }
    },
    {
      "name": "log_activity",
      "description": "Записать активность в Activity Hub",
      "parameters": {
        "user_id": "string",
        "activity_type": "string",
        "metadata": "object"
      }
    },
    {
      "name": "calculate_rewards",
      "description": "Рассчитать вознаграждение за активность",
      "parameters": {
        "activity_id": "string"
      }
    }
  ]
}
```

---

## Техническая архитектура MCP Gateway

### Компоненты

```
┌─────────────────────────────────────────────────────────────────┐
│                      MCP GATEWAY                                 │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌──────────────────┐  ┌──────────────────┐  ┌───────────────┐  │
│  │  Auth Provider   │  │  Tool Registry   │  │ Rate Limiter  │  │
│  │  (OAuth 2.1)     │  │  (all tools)     │  │ (per user)    │  │
│  └────────┬─────────┘  └────────┬─────────┘  └───────┬───────┘  │
│           │                     │                     │          │
│           └─────────────────────┼─────────────────────┘          │
│                                 │                                │
│                    ┌────────────▼────────────┐                   │
│                    │     MCP Router          │                   │
│                    │  (routes tool calls)    │                   │
│                    └────────────┬────────────┘                   │
│                                 │                                │
│  ┌──────────────────────────────┼──────────────────────────────┐ │
│  │                              │                              │ │
│  ▼                              ▼                              ▼ │
│ ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌─────┐ │
│ │ Digital  │  │  Memory  │  │  Token   │  │  LMS     │  │ ... │ │
│ │ Twin     │  │  Bank    │  │ Economy  │  │          │  │     │ │
│ │ Adapter  │  │ Adapter  │  │ Adapter  │  │ Adapter  │  │     │ │
│ └────┬─────┘  └────┬─────┘  └────┬─────┘  └────┬─────┘  └──┬──┘ │
│      │             │             │             │            │    │
└──────┼─────────────┼─────────────┼─────────────┼────────────┼────┘
       │             │             │             │            │
       ▼             ▼             ▼             ▼            ▼
   [Digital      [Memory       [Token       [LMS          [...]
    Twin]         Bank]        Economy]     Service]
```

### Манифест MCP Server

```json
{
  "name": "aisystant-ecosystem",
  "version": "1.0.0",
  "description": "Экосистема развития интеллекта Aisystant",
  "icon": "https://aisystant.com/icon.png",
  "authentication": {
    "type": "oauth2",
    "authorization_url": "https://auth.aisystant.com/authorize",
    "token_url": "https://auth.aisystant.com/token",
    "scopes": {
      "profile": "Базовый профиль",
      "trajectory": "Траектория развития",
      "tokens": "Управление токенами",
      "learning": "Обучение и задания",
      "community": "Активность в сообществе"
    }
  },
  "tools": [
    {
      "name": "get_my_profile",
      "description": "Получить профиль участника экосистемы"
    },
    {
      "name": "get_learning_trajectory",
      "description": "Персональная траектория развития"
    },
    {
      "name": "get_token_balance",
      "description": "Баланс STK токенов"
    },
    {
      "name": "search_knowledge",
      "description": "Поиск в базе знаний"
    },
    {
      "name": "submit_work",
      "description": "Отправить выполненную работу"
    },
    {
      "name": "get_referral_link",
      "description": "Реферальная ссылка"
    }
  ],
  "templates": [
    {
      "name": "daily_summary",
      "description": "Ежедневная сводка прогресса"
    },
    {
      "name": "week_review",
      "description": "Еженедельный ревью"
    }
  ]
}
```

---

## Стратегия публикации

### Фаза 1: OpenAI Apps SDK (приоритет)

**Почему первый:**
- Крупнейшая пользовательская база (ChatGPT)
- Apps SDK в активном развитии
- Submissions открыты

**Публикуемые приложения:**
1. **Aisystant Guide** — персональный проводник по траектории
2. **Aisystant Wallet** — управление STK токенами
3. **Aisystant Learn** — изучение материалов и выполнение заданий

### Фаза 2: Anthropic MCP Integration

**Почему второй:**
- MCP — основа Apps SDK, натуральная интеграция
- Claude популярен среди технических пользователей
- MCP Connector упрощает интеграцию

**Формат:** Remote MCP Server в каталоге Claude Integrations

### Фаза 3: Google Gemini Extensions

**Почему третий:**
- Поддержка MCP объявлена
- Interactions API в активном развитии
- Интеграция с Google Workspace

**Формат:** Gemini CLI Extension + Connected App

---

## Преимущества подхода

### Для участников

1. **Нулевой барьер входа** — работа в привычном интерфейсе
2. **Мультиплатформенность** — один аккаунт, любой LLM
3. **Бесшовный UX** — полный функционал без переключения контекста
4. **Мобильность** — ChatGPT/Claude/Gemini apps на телефоне

### Для экосистемы

1. **Расширение охвата** — доступ к аудитории всех LLM-платформ
2. **Снижение CAC** — не нужно убеждать людей устанавливать новое приложение
3. **Единая кодовая база** — MCP работает везде
4. **Brand presence** — экосистема присутствует в крупнейших маркетплейсах

### Технические

1. **Стандартизация** — MCP как открытый стандарт
2. **Масштабируемость** — один MCP сервер для всех платформ
3. **Безопасность** — OAuth 2.1, ACL через ORY
4. **Эволюция** — новые платформы легко добавляются

---

## Риски и митигация

| Риск | Митигация |
|------|-----------|
| Изменение API платформ | MCP — открытый стандарт под Linux Foundation |
| Модерация и rejection | Строгое соответствие guidelines каждой платформы |
| Rate limits платформ | Кеширование, graceful degradation |
| Data privacy | Минимальный скоп OAuth, transparent data usage |
| Зависимость от сторонних платформ | Параллельное развитие собственного интерфейса |

---

## Roadmap

### Q1 2026
- [ ] Разработка MCP Gateway
- [ ] Адаптеры для Digital Twin, Memory Bank, Token Economy
- [ ] Подготовка к submission в OpenAI

### Q2 2026
- [ ] Публикация Aisystant Guide в ChatGPT
- [ ] Интеграция с Claude через MCP Connector
- [ ] Сбор feedback и итерации

### Q3 2026
- [ ] Публикация дополнительных приложений
- [ ] Gemini Extensions
- [ ] Advanced features (голосовые интерфейсы, мультимодальность)

### Q4 2026
- [ ] Маркетплейс сторонних ассистентов на базе экосистемы
- [ ] Enterprise интеграции
- [ ] Федеративная архитектура

---

## Связанные документы

- [[Apps SDK и маркетплейс 3.2]] — внутренний маркетплейс ассистентов
- [[Общая архитектура ИТ-платформы 3.2]] — архитектура платформы
- [[Токеномика и распределение 3.1]] — экономика токенов
- [[Проводник по персональному маршруту 3.2]] — ИИ-ассистент

---

## Источники

- [OpenAI Apps SDK](https://developers.openai.com/apps-sdk/)
- [Introducing Apps in ChatGPT (OpenAI)](https://openai.com/index/introducing-apps-in-chatgpt/)
- [Model Context Protocol (Anthropic)](https://www.anthropic.com/news/model-context-protocol)
- [Claude Integrations](https://www.anthropic.com/news/integrations)
- [Gemini CLI Extensions](https://blog.google/technology/developers/gemini-cli-extensions/)
- [Google Interactions API](https://blog.google/technology/developers/interactions-api/)
- [MCP on Linux Foundation](https://en.wikipedia.org/wiki/Model_Context_Protocol)

---

**Status:** 🟡 Draft
**Owner:** AI Platform Team
**Last Updated:** 2025-12-21
