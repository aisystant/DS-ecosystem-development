---
type: guide
status: draft
version: 0.1
created: 2025-12-30
layer: integration
scope: ecosystem
related:
  - "Архитектура доступа ИИ к данным экосистемы 0.9"
  - "FSM-архитектура ИИ-ассистентов 3.2"
  - "Канонический шаблон описания MCP Tools и Resources"
description: "Пошаговая процедура интеграции MCP-серверов с LLM через OpenAI Apps SDK"
---

# Интеграция MCP-серверов с LLM через OpenAI Apps SDK

> **Назначение:** Пошаговое руководство по подключению MCP-серверов экосистемы к LLM через OpenAI Apps SDK для предоставления пользователям доступа через ChatGPT.

---

## Что вы получите в результате

После выполнения этого руководства:

1. Пользователи смогут обращаться к ИИ-ассистентам экосистемы через ChatGPT
2. LLM получит доступ ко всем инструментам подключённых MCP-серверов
3. MCP-app сможет вызывать MCP-data для получения персонализированных данных

---

## Архитектура интеграции

```
┌───────────────────────────────────────────────────────────────────────────┐
│                              ChatGPT                                       │
│                                                                            │
│  Пользователь ──► GPT ──► Apps SDK Runtime                                │
│                                                                            │
└────────────────────────────────┬──────────────────────────────────────────┘
                                 │
                                 │ Apps SDK подключает все MCP
                                 ▼
┌───────────────────────────────────────────────────────────────────────────┐
│                     MCP-серверы (все на одном уровне)                      │
│                                                                            │
│   ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐           │
│   │    MCP-APP      │  │    MCP-DATA     │  │    MCP-DATA     │           │
│   │    fsm-mcp      │  │     dt-mcp      │  │   guides-mcp    │           │
│   │                 │  │                 │  │                 │           │
│   │ get_instruction │  │ dt.get_progress │  │ guides.search   │           │
│   │                 │  │ dt.get_goals    │  │ guides.get      │           │
│   └────────┬────────┘  └─────────────────┘  └─────────────────┘           │
│            │                    ▲                                          │
│            │ server-to-server   │                                          │
│            └────────────────────┘                                          │
│                                                                            │
│   GPT может вызывать любой MCP напрямую                                   │
│   MCP-app может вызывать MCP-data (server-to-server)                      │
│                                                                            │
└───────────────────────────────────────────────────────────────────────────┘
```

---

## Предварительные требования

| Требование | Описание |
|------------|----------|
| **Аккаунт OpenAI** | Верифицированный аккаунт разработчика |
| **MCP-серверы** | Развёрнутые и доступные по HTTPS |
| **OAuth-провайдер** | Aisystant Identity для авторизации пользователей |

### Проверка готовности MCP-серверов

Перед интеграцией убедитесь, что MCP-серверы отвечают:

```bash
# MCP-app
curl -X POST https://fsm-mcp.aisystant.workers.dev/mcp \
  -H "Content-Type: application/json" \
  -d '{"method": "tools/list"}'

# MCP-data
curl -X POST https://dt-mcp.aisystant.workers.dev/mcp \
  -H "Content-Type: application/json" \
  -d '{"method": "tools/list"}'
```

---

## Пошаговая процедура интеграции

### Шаг 1. Включить Developer Mode в ChatGPT

1. Войдите в ChatGPT с аккаунтом OpenAI
2. Откройте **Settings → Apps & Connectors → Advanced**
3. Включите **Developer Mode**
4. Сохраните изменения

**Результат:** Доступ к созданию коннекторов в Developer Platform.

---

### Шаг 2. Создать приложение в Developer Platform

1. Откройте [platform.openai.com](https://platform.openai.com)
2. Перейдите в **Apps**
3. Нажмите **Create App**

Заполните базовые параметры:

| Поле | Значение |
|------|----------|
| Name | Aisystant Ecosystem |
| Description | Персонализированное развитие через ИИ-ассистентов |
| Category | Education, Productivity |

**Результат:** Создано приложение, готовое к подключению MCP-серверов.

---

### Шаг 3. Подключить MCP-серверы

В настройках приложения добавьте все MCP-серверы экосистемы:

#### 3.1 Добавить MCP-app (логика ассистентов)

| Параметр | Значение |
|----------|----------|
| Name | fsm-mcp |
| URL | `https://fsm-mcp.aisystant.workers.dev/mcp` |
| Auth | OAuth (Aisystant Identity) |

#### 3.2 Добавить MCP-data (данные)

Добавьте каждый MCP-data сервер:

**dt-mcp (Цифровой двойник):**

| Параметр | Значение |
|----------|----------|
| Name | dt-mcp |
| URL | `https://dt-mcp.aisystant.workers.dev/mcp` |
| Auth | OAuth (Aisystant Identity) |

**guides-mcp (Руководства):**

| Параметр | Значение |
|----------|----------|
| Name | guides-mcp |
| URL | `https://guides-mcp.aisystant.workers.dev/mcp` |
| Auth | OAuth (Aisystant Identity) |

**exercises-mcp (Упражнения):**

| Параметр | Значение |
|----------|----------|
| Name | exercises-mcp |
| URL | `https://exercises-mcp.aisystant.workers.dev/mcp` |
| Auth | OAuth (Aisystant Identity) |

#### Конфигурация в формате JSON

```json
{
  "mcpServers": {
    "fsm-mcp": {
      "url": "https://fsm-mcp.aisystant.workers.dev/mcp",
      "auth": {
        "type": "oauth",
        "provider": "aisystant-identity"
      }
    },
    "dt-mcp": {
      "url": "https://dt-mcp.aisystant.workers.dev/mcp",
      "auth": {
        "type": "oauth",
        "provider": "aisystant-identity"
      }
    },
    "guides-mcp": {
      "url": "https://guides-mcp.aisystant.workers.dev/mcp",
      "auth": {
        "type": "oauth",
        "provider": "aisystant-identity"
      }
    },
    "exercises-mcp": {
      "url": "https://exercises-mcp.aisystant.workers.dev/mcp",
      "auth": {
        "type": "oauth",
        "provider": "aisystant-identity"
      }
    }
  }
}
```

**Результат:** Все MCP-серверы подключены. GPT видит все инструменты.

---

### Шаг 4. Настроить OAuth авторизацию

#### 4.1 В Aisystant Identity

Создайте OAuth-клиент для OpenAI Apps SDK:

| Параметр | Значение |
|----------|----------|
| Client ID | `openai-apps-sdk` |
| Redirect URI | Согласно документации OpenAI |
| Scopes | `profile`, `read:dt`, `write:dt`, `read:guides` |

#### 4.2 В Developer Platform

Настройте OAuth в приложении:

| Параметр | Значение |
|----------|----------|
| OAuth Provider | Aisystant Identity |
| Authorization URL | `https://identity.aisystant.com/oauth/authorize` |
| Token URL | `https://identity.aisystant.com/oauth/token` |
| Scopes | `profile read:dt write:dt read:guides` |

**Результат:** Пользователи смогут авторизоваться, токен будет передаваться в MCP-запросы.

---

### Шаг 5. Проверить доступность инструментов

После подключения GPT должен видеть все инструменты. Проверьте в Developer Console:

**Ожидаемые инструменты:**

| MCP-сервер | Инструменты |
|------------|-------------|
| fsm-mcp | `get_instruction(state?)` |
| dt-mcp | `dt.get_progress()`, `dt.get_goals()`, `dt.save_reflection()` |
| guides-mcp | `guides.search(query)`, `guides.get(id)` |
| exercises-mcp | `exercises.get(id)`, `exercises.check(id, answer)` |

**Результат:** GPT может вызывать любой инструмент любого MCP-сервера.

---

### Шаг 6. Тестирование сценариев

#### Сценарий 1: Через MCP-app (FSM-логика)

Пользователь: *"Подведи итоги недели"*

```
1. GPT вызывает get_instruction() → fsm-mcp
2. fsm-mcp определяет состояние weekly_reflection
3. fsm-mcp вызывает dt.get_week_summary() → dt-mcp (s2s)
4. fsm-mcp возвращает инструкции + данные
5. GPT формирует структурированный ответ
```

#### Сценарий 2: Напрямую к MCP-data

Пользователь: *"Найди руководство по системному мышлению"*

```
1. GPT вызывает guides.search("системное мышление") → guides-mcp
2. guides-mcp возвращает список руководств
3. GPT формирует ответ
```

#### Сценарий 3: Комбинированный

Пользователь: *"Какие мои цели? И дай упражнение по первой цели"*

```
1. GPT вызывает dt.get_goals() → dt-mcp
2. GPT вызывает exercises.get(goal_id) → exercises-mcp
3. GPT формирует комбинированный ответ
```

**Результат:** Все сценарии работают корректно.

---

### Шаг 7. Настроить server-to-server вызовы (MCP-app → MCP-data)

Для сложных сценариев MCP-app должен уметь вызывать MCP-data:

```typescript
// В fsm-mcp: вызов dt-mcp для получения данных

async function callMcpData(
  mcpUrl: string,
  tool: string,
  args: object,
  token: string
) {
  const response = await fetch(mcpUrl, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${token}`  // Передаём токен пользователя
    },
    body: JSON.stringify({
      method: 'tools/call',
      params: { name: tool, arguments: args }
    })
  });

  return response.json();
}

// Использование в get_instruction
async function getInstruction(state: string, context: Context) {
  const token = context.headers.get('Authorization');

  // Получаем данные пользователя из dt-mcp
  const progress = await callMcpData(
    'https://dt-mcp.aisystant.workers.dev/mcp',
    'dt.get_progress',
    {},
    token
  );

  // Возвращаем инструкции с данными
  return {
    instructions: loadState(state),
    userData: progress
  };
}
```

**Результат:** MCP-app может обогащать инструкции данными из MCP-data.

---

### Шаг 8. Публикация приложения

#### 8.1 Подготовка метаданных

| Параметр | Значение |
|----------|----------|
| Иконка | 512x512 PNG |
| Скриншоты | 3-5 примеров диалогов |
| Категории | Education, Productivity |
| Описание | Подробное описание возможностей |

#### 8.2 Отправка на ревью

1. В Developer Platform нажмите **Submit for Review**
2. Дождитесь ответа (обычно 3-5 рабочих дней)
3. Доработайте по замечаниям при необходимости

**Результат:** Приложение доступно пользователям ChatGPT.

---

## Чек-лист интеграции

| # | Шаг | Статус |
|---|-----|--------|
| 1 | Developer Mode включён | ☐ |
| 2 | Приложение создано в Developer Platform | ☐ |
| 3 | Все MCP-серверы подключены | ☐ |
| 4 | OAuth настроен | ☐ |
| 5 | Инструменты доступны GPT | ☐ |
| 6 | Сценарий через MCP-app работает | ☐ |
| 7 | Сценарий напрямую к MCP-data работает | ☐ |
| 8 | Server-to-server вызовы работают | ☐ |
| 9 | Приложение опубликовано | ☐ |

---

## Диаграмма: два варианта вызова MCP

```
┌─────────────┐      ┌─────────────┐      ┌─────────────┐      ┌─────────────┐
│  ChatGPT    │      │    GPT      │      │  fsm-mcp    │      │   dt-mcp    │
└──────┬──────┘      └──────┬──────┘      └──────┬──────┘      └──────┬──────┘
       │                    │                    │                    │
       │                    │                    │                    │
       │  Вариант 1: через MCP-app (FSM-логика)  │                    │
       │  ─────────────────────────────────────  │                    │
       │                    │                    │                    │
       │ "Подведи итоги     │                    │                    │
       │  недели"           │                    │                    │
       │                    │  get_instruction() │                    │
       │                    │───────────────────>│                    │
       │                    │                    │  dt.get_progress() │
       │                    │                    │───────────────────>│
       │                    │                    │<───────────────────│
       │                    │<───────────────────│                    │
       │                    │                    │                    │
       │                    │                    │                    │
       │  Вариант 2: напрямую к MCP-data         │                    │
       │  ──────────────────────────────         │                    │
       │                    │                    │                    │
       │ "Какие мои цели?"  │                    │                    │
       │                    │  dt.get_goals()    │                    │
       │                    │────────────────────────────────────────>│
       │                    │<────────────────────────────────────────│
       │                    │                    │                    │
```

---

## Типичные проблемы и решения

| Проблема | Причина | Решение |
|----------|---------|---------|
| MCP-сервер недоступен | Неверный URL или сервер не запущен | Проверить URL, статус Workers |
| Инструменты не видны GPT | MCP не возвращает `tools/list` | Проверить реализацию MCP |
| Ошибка авторизации | Неверный OAuth-конфиг | Проверить Client ID, Redirect URI |
| s2s вызовы не работают | Токен не передаётся | Убедиться, что токен передаётся в заголовке |

---

## Безопасность

### Передача токена

```
Интерфейс → MCP-app → MCP-data
           ↓         ↓
     Authorization: Bearer <token>
```

- Каждый MCP проверяет токен
- Извлекает `user_id`
- Возвращает только данные этого пользователя

### Content Security Policy

```json
{
  "connect_domains": [
    "fsm-mcp.aisystant.workers.dev",
    "dt-mcp.aisystant.workers.dev",
    "guides-mcp.aisystant.workers.dev",
    "exercises-mcp.aisystant.workers.dev"
  ]
}
```

---

## Связанные документы

- **[[Архитектура доступа ИИ к данным экосистемы 0.9]]** — общая архитектура (MCP-app / MCP-data)
- **[[FSM-архитектура ИИ-ассистентов 3.2]]** — архитектура FSM-логики
- **[[Канонический шаблон описания MCP Tools и Resources]]** — формат описания инструментов

---

## Changelog

| Дата | Версия | Изменения |
|------|--------|-----------|
| 2025-12-30 | v0.1 | Документ создан на основе архитектуры v1.3. Фокус на пошаговой процедуре |
