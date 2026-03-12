---
id: DP.D.032
name: "Единый Circuit Breaker для внешних зависимостей"
type: distinction
status: active
summary: "Один паттерн circuit breaker для всех внешних зависимостей (Claude API, MCP, Neon). Цель: предотвратить циклические запросы, которые списывают деньги. Не per-client — единый middleware"
created: 2026-02-19
edition: "2026-02"
source: "Решение Архитектора 19 фев 2026"
trust:
  F: 3
  G: domain
  R: 0.7
related:
  extends: [DP.ARCH.001]
  uses: [DP.AISYS.014, DP.FM.003]
---

# Единый Circuit Breaker для внешних зависимостей

## 1. Различение

| Подход | Описание | Проблема |
|--------|----------|----------|
| **Per-client** (текущий) | MCP имеет свой CB (2 failures → 60s cooldown). Claude API — нет CB. Neon — нет CB | Циклические ошибки Claude API списывают деньги. Разная логика в разных клиентах |
| **Единый паттерн** (решение) | Один middleware CB для всех внешних зависимостей | Единообразие. Защита от циклических расходов |

## 2. Целевое состояние

```python
# Единый circuit breaker middleware
class CircuitBreaker:
    """Применяется ко всем внешним зависимостям."""

    states = {
        'closed':    # Нормальная работа
        'open':      # Запросы блокируются (fallback)
        'half-open': # Пробный запрос
    }

    config = {
        'claude_api':  {'failures': 3, 'cooldown': 60, 'half_open_after': 30},
        'mcp':         {'failures': 2, 'cooldown': 60, 'half_open_after': 30},
        'neon':        {'failures': 5, 'cooldown': 120, 'half_open_after': 60},
    }
```

## 3. Мотивация

> **Циклические запросы не должны списывать деньги.** При ошибке Claude API (429, 529, timeout) — не retry бесконечно, а остановить и вернуть graceful degradation.
