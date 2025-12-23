# Ссылка на репозиторий MCP

## Текущий статус

**Репозиторий:** Пока не создан отдельно

MCP-сервер в Release 1 реализован как часть тестовой инфраструктуры и развёрнут на Cloudflare Workers.

## Планируемое расположение

После выделения в отдельный репозиторий:

```
github.com/aisystant/digital-twin-mcp
```

## Структура репозитория (планируемая)

```
digital-twin-mcp/
├── src/
│   ├── index.ts           # Точка входа Cloudflare Worker
│   ├── tools/             # Реализация MCP-инструментов
│   │   ├── get_week_state.ts
│   │   ├── get_week_time.ts
│   │   ├── get_slot_consistency.ts
│   │   └── get_work_products.ts
│   ├── demo/              # Демо-данные
│   │   ├── profiles.ts
│   │   └── data.ts
│   └── utils/
│       ├── validation.ts
│       └── formatting.ts
├── tests/
│   └── tools.test.ts
├── wrangler.toml          # Конфиг Cloudflare
├── package.json
└── README.md
```

## Технологии

| Компонент | Технология |
|-----------|------------|
| Runtime | Cloudflare Workers |
| Язык | TypeScript |
| MCP SDK | @modelcontextprotocol/sdk |
| Тесты | Vitest |
| Деплой | Wrangler CLI |

## Доступ

После создания репозитория доступ будет предоставлен:
- Команде AI Platform (read/write)
- CI/CD для автодеплоя

## Временное решение (Release 1)

Код MCP-сервера находится в:
```
[внутренний репозиторий]/cloudflare-workers/digital-twin-mcp/
```

Деплой выполняется вручную через Wrangler.

---

**Связанные документы:**
- [[Ссылка-на-MCP-эндпоинт-и-описание]]
- [[Совместимость-версий-MCP-и-контрактов]]
