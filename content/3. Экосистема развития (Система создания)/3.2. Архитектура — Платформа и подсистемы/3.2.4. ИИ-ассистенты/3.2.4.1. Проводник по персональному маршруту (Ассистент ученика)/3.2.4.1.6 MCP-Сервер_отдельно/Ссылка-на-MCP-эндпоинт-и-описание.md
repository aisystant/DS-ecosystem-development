# MCP-сервер: эндпоинт и описание

## Эндпоинты

| URL | Назначение |
|-----|------------|
| `https://digital-twin-mcp.aisystant.workers.dev/mcp` | MCP-эндпоинт (JSON-RPC 2.0) |
| `https://digital-twin-mcp.aisystant.workers.dev/openapi.json` | OpenAPI 3.1 спецификация |
| `https://digital-twin-mcp.aisystant.workers.dev/` | Документация сервера и примеры |

**Платформа:** Cloudflare Workers

---

## Как подключить

### В OpenAI Apps SDK

```json
{
  "mcp_server": {
    "url": "https://digital-twin-mcp.aisystant.workers.dev/mcp"
  }
}
```

### Получить OpenAPI спецификацию

```bash
curl https://digital-twin-mcp.aisystant.workers.dev/openapi.json
```

### Получить список инструментов (MCP)

```bash
curl -X POST https://digital-twin-mcp.aisystant.workers.dev/mcp \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "method": "tools/list",
    "id": 1
  }'
```

### Вызвать инструмент

```bash
curl -X POST https://digital-twin-mcp.aisystant.workers.dev/mcp \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "method": "tools/call",
    "params": {
      "name": "dt.get_time_invested_summary",
      "arguments": {
        "period_start": "2025-12-16",
        "period_end": "2025-12-22"
      }
    },
    "id": 1
  }'
```

---

## Доступные инструменты

### Реализованные (✅)

| Инструмент | Описание |
|------------|----------|
| `dt.get_time_invested_summary` | Сводка по времени обучения за период |

**Параметры `dt.get_time_invested_summary`:**

| Параметр | Тип | Обязательный | Описание |
|----------|-----|--------------|----------|
| `period_start` | string (date) | Нет | Начальная дата (YYYY-MM-DD), по умолчанию -30 дней |
| `period_end` | string (date) | Нет | Конечная дата, по умолчанию сегодня |

**Ответ:**
```json
{
  "total_hours": 5.2,
  "sessions_count": 12,
  "pomodoros_completed": 8,
  "days_with_activity": 4,
  "avg_daily_minutes": 26,
  "period": {
    "start": "2025-12-16",
    "end": "2025-12-22"
  }
}
```

### Планируемые (🔜)

| Инструмент | Описание |
|------------|----------|
| `dt.get_week_state` | Состояние недели (действия, дни) |
| `dt.get_slot_consistency` | Систематичность слота |
| `dt.get_work_products` | Рабочие продукты за период |

---

## Демо-режим

В Release 1 сервер может работать с демо-данными. Подробности: [[Правила-демо-режима-без-идентификации]]

---

## MCP-методы сервера

Сервер поддерживает стандартные MCP-методы:

| Метод | Описание |
|-------|----------|
| `initialize` | Инициализация сеанса |
| `tools/list` | Получить список инструментов |
| `tools/call` | Вызвать инструмент |

---

## Логи и мониторинг

- **Dashboard:** Cloudflare Workers → digital-twin-mcp → Logs
- **Метрики:** Workers Analytics

---

**Последнее обновление:** 2025-12-23
