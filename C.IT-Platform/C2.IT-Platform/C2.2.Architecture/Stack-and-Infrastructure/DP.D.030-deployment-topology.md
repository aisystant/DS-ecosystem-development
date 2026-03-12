---
id: DP.D.030
name: "Топология деплоя платформы"
type: distinction
status: active
summary: "Railway (бот) + CF Workers (MCP) + Neon (DB + pgvector) + GitHub (код + шаблон). Позже Railway → Kubernetes. Каждый сервис — в своей экологической нише (compute vs edge vs serverless DB vs VCS)"
created: 2026-02-19
edition: "2026-02"
source: "Решение Архитектора 19 фев 2026"
trust:
  F: 4
  G: domain
  R: 0.8
related:
  extends: [DP.ARCH.001]
  uses: [DP.AISYS.014]
---

# Топология деплоя платформы

## 1. Различение

| Компонент | Провайдер | Роль | Регион |
|-----------|-----------|------|--------|
| **Бот** (Python, aiogram) | Railway | Long-running process, webhooks | EU Amsterdam |
| **MCP-серверы** (TypeScript) | Cloudflare Workers | Edge compute, stateless | Auto (global) |
| **База данных** (PostgreSQL + pgvector) | Neon | Serverless DB, vector search | EU Frankfurt |
| **Код + шаблон** | GitHub | VCS, CI/CD, Actions | — |

## 2. Почему именно эта связка

| Критерий | Объяснение |
|----------|-----------|
| **Экологические ниши** | Каждый провайдер силён в своём: Railway — Python processes, CF — edge JS, Neon — serverless PG, GitHub — git+CI |
| **Free tier** | CF Workers (100K req/day), Neon Free (100 connections), GitHub Actions (2000 мин/мес) |
| **Vendor lock-in** | Низкий: бот = стандартный Python (переносим), MCP = CF Workers API (портируем), Neon = стандартный PG (pg_dump) |
| **Latency** | Railway EU ↔ Neon EU: ~2-5ms. Railway EU ↔ CF Workers: ~10-20ms (edge). Приемлемо для бот-бюджета <3 сек |

## 3. Эволюция

```
Текущая:   Railway → CF Workers → Neon → GitHub
Ближайшая: + Neon Pro ($20/мес, PgBouncer)
Будущая:   Railway → Kubernetes (больше контроля, multi-instance)
```

> **Решение Архитектора:** текущая топология верна. Kubernetes — когда потребуется больше контроля и масштаба (10+ инстансов).
