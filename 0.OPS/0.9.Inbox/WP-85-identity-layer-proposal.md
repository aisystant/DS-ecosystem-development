---
type: proposal
wp: 85
title: "Identity Layer: DT MCP as BFF"
status: pending-review
created: 2026-03-13
author: engineer
---

# Proposal: Identity Layer — DT MCP as BFF (Variant C)

## Контекст

WP-85 Phase 3 done. `public.users` с UUID PK работает. Колонка `ory_id` существует, но не заполняется — бот авторизуется через DT MCP (OAuth PKCE на Cloudflare Workers), не через Ory напрямую.

## Вопрос

Где граница identity layer? DT MCP уже выдаёт `dt_user_id` (UUID) через OAuth. Нужен ли отдельный Ory сейчас?

## Предложение: DT MCP as BFF (АрхГейт 8.4)

`dt_user_id` = identity UUID. Бот продолжает один OAuth flow через DT MCP. При появлении второго клиента (Web app) — DT MCP делегирует auth в Ory, UUID портируется через Admin API import.

```
Сейчас:  Бот → DT MCP (OAuth + данные) → UUID
Потом:   Бот → Ory (OAuth) + DT MCP (данные) → тот же UUID
```

Переход C→B не ломает данные: Ory импортирует существующие UUID, `public.users` не меняется.

## Вопрос к архитектору

Согласуете: `dt_user_id` = identity UUID (заполняем `ory_id` в callback), Ory откладываем до второго клиента?
