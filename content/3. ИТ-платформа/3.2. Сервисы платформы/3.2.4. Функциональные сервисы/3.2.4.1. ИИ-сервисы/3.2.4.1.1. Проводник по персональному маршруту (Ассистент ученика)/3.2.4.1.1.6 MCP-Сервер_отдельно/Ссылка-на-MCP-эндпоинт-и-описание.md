# MCP-сервер: эндпоинт и описание

## Текущий эндпоинт

**URL:** `https://digital-twin-mcp.aisystant.workers.dev/mcp`

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

### Для тестирования (curl)

```bash
curl -X POST https://digital-twin-mcp.aisystant.workers.dev/mcp \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "method": "tools/call",
    "params": {
      "name": "get_week_state",
      "arguments": {"demo_profile": "good"}
    },
    "id": 1
  }'
```

---

## Доступные инструменты (Release 1)

| Инструмент | Описание |
|------------|----------|
| `get_week_state` | Состояние недели (действия, дни) |
| `get_week_time` | Инвестированное время за неделю |
| `get_slot_consistency` | Систематичность слота |
| `get_week_products` | Рабочие продукты за неделю |

---

## Демо-режим

В Release 1 сервер работает без идентификации. Для переключения между демо-профилями используйте параметр `demo_profile`:

- `empty` — пустая неделя
- `weak` — слабая неделя
- `good` — хорошая неделя

---

## Логи и мониторинг

- **Dashboard:** Cloudflare Workers → digital-twin-mcp → Logs
- **Метрики:** Workers Analytics

---

## Контакты

При проблемах с MCP-сервером:
- [TBD: контакт]

---

**Последнее обновление:** 2025-12-23
