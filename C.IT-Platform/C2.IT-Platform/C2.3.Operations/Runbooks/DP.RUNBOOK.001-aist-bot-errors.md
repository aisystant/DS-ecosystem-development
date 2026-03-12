---
id: DP.RUNBOOK.001
name: "Runbook: Aist Bot Errors"
type: domain-entity
status: draft
summary: "Каталог типичных ошибок Aist Bot с классификацией по уровням (L1-L4), автоматическими действиями и ручными fix'ами"
created: 2026-02-18
trust:
  F: 3
  G: domain
  R: 0.4
epistemic_stage: emerging
related:
  - id: DP.AISYS.014
    type: extends
  - id: DP.ROLE.001
    type: uses
---

# Runbook: Aist Bot Errors

## 1. Определение

**Runbook** — каталог известных паттернов ошибок с инструкциями по автоматическому и ручному исправлению. Source-of-truth для Наладчика (I7).

## 2. Уровни реагирования

| Уровень | Название | Автономность | Время | Кто выполняет |
|---------|----------|-------------|-------|---------------|
| **L1** | Unstick | Полная (без человека) | <1 мин | I1 (bot, in-process) |
| **L2** | Auto-fix | Через PR (human review) | 5-15 мин | I7 (CLI) → GitHub PR |
| **L3** | Restart | Автоматический (по порогу) | 1-3 мин | Script (Railway API) |
| **L4** | Escalate | Уведомление человеку | <1 мин | I7 → GitHub Issue + TG |

### 2.1. L1 — Unstick (полностью автоматический)

**Что:** Бот сам обнаруживает и исправляет проблему. Пользователь может даже не заметить.

**Механика:** Scheduler каждые 5 мин проверяет `error_logs` + `user_states`. Если обнаружены симптомы (3+ ошибки за 5 мин, stuck >60 мин, rate limit, flood control) — бот автоматически выполняет действие: сброс FSM → mode_select, retry с backoff, skip + лог, fallback-контент. Код: `core/unstick.py` (in-process, не требует внешних сервисов).

**Примеры:** dead-end state, stuck user, Claude 429/529, TG flood control, blocked by user.

**Участие человека:** Не требуется. Информация доступна в `/errors` (dev-команда).

### 2.2. L2 — Auto-Fix (диагностика + PR с подтверждением)

**Что:** Ошибка в коде, которую можно исправить автоматически. Бот предлагает исправление, человек одобряет.

**Механика:** Scheduler каждые 15 мин ищет L2-ошибки (count >= 3, последние 15 мин). Для каждой: (1) fetch исходного файла через GitHub API, (2) Claude Sonnet анализирует ошибку + код → диагноз + минимальный fix + ArchGate-оценка, (3) фильтр: confidence != low, ArchGate >= 8, (4) TG-сообщение разработчику с кнопками [Применить / Отклонить], (5) на «Применить» → создаётся ветка `fix/<key>` → коммит → PR на GitHub. Код: `core/autofix.py`.

**Примеры:** state corruption, query timeout, invalid Claude/MCP response, message too long.

**Участие человека:** Два шага — одобрение в TG (кнопка) + merge PR на GitHub → Railway auto-deploy.

### 2.3. L3 — Restart (автоматический перезапуск)

**Что:** Инфраструктурная проблема, которую исправляет перезапуск. Код менять не нужно.

**Механика:** (планируется) По порогу (pool exhaustion, connection timeout) — скрипт вызывает Railway API для перезапуска сервиса. Пока реализовано: Grafana Alert Rule #1 (L3+ Critical) отправляет уведомление в TG → ручной restart через Railway dashboard.

**Примеры:** pool exhaustion (too many connections), connection timeout, MCP connection failure.

**Участие человека:** Пока — ручной restart через Railway dashboard по Grafana-алерту. После реализации L3-скрипта — без участия.

### 2.4. L4 — Escalate (уведомление человеку)

**Что:** Критическая проблема, которую нельзя исправить автоматически. Требуется вмешательство разработчика.

**Механика:** Scheduler каждые 15 мин проверяет L4-ошибки (count >= 2, не эскалированные). Отправляет TG-сообщение с описанием + suggested action. Grafana Alert Rules #1-#4 — независимый канал (работает даже если бот упал). Код: `core/error_classifier.py:check_escalation()`.

**Примеры:** migration failure (relation does not exist), scheduler stuck (asyncio deadlock).

**Участие человека:** Полное — ручная диагностика и исправление по инструкциям из RUNBOOK.

## 3. Категории ошибок

### 3.1. FSM (State Machine)

| Паттерн | Симптомы | Severity | Auto Action | Manual Fix |
|---------|----------|----------|-------------|------------|
| **Dead-end state** | Пользователь не может выйти из состояния, нет кнопок | L1 | Reset → mode_select | Добавить transition в transitions.yaml |
| **Missing handler** | `No handler for state X`, traceback в error_logs | L1 | Reset → mode_select | Создать handler для нового state |
| **Stuck user** | Пользователь в одном state >60 мин без активности | L1 | Reset → mode_select + извинение | Проверить UX: почему застревают |
| **Repeated errors** | 3+ ошибки одного user_id за 5 мин | L1 | Reset → mode_select + извинение | Анализ error_logs → root cause |
| **State corruption** | FSM state не совпадает с DB current_state | L2 | PR: sync state | Проверить все пути обновления state |

### 3.2. DB (Database / Neon)

| Паттерн | Симптомы | Severity | Auto Action | Manual Fix |
|---------|----------|----------|-------------|------------|
| **Pool exhaustion** | `too many connections`, все запросы висят | L3 | Restart бот (освободить pool) | Увеличить pool_size, проверить leaks |
| **Connection timeout** | `connection timed out`, latency >10с | L3 | Restart + keep-alive ping | Проверить Neon status, region |
| **Query timeout** | Один запрос >30с, остальные в очереди | L2 | PR: optimize query | Добавить index, переписать запрос |
| **Migration failure** | `relation X does not exist` после деплоя | L4 | Escalate → Issue | Ручной запуск CREATE TABLE |

### 3.3. Claude API

| Паттерн | Симптомы | Severity | Auto Action | Manual Fix |
|---------|----------|----------|-------------|------------|
| **429 Rate limit** | `rate_limit_error`, пользователь ждёт | L1 | Retry с exponential backoff (уже в коде) | Увеличить лимит в Anthropic Console |
| **529 Overloaded** | `overloaded_error`, все Claude-запросы fail | L1 | Degrade: показать cached content | Подождать, мониторить status.anthropic.com |
| **Timeout** | Claude >30с, пользователь ушёл | L1 | Retry 1 раз, затем fallback message | Оптимизировать промпт (длина context) |
| **Invalid response** | Claude вернул невалидный JSON/format | L2 | PR: fix parsing | Обновить промпт + добавить validation |

### 3.4. Telegram API

| Паттерн | Симптомы | Severity | Auto Action | Manual Fix |
|---------|----------|----------|-------------|------------|
| **Flood control** | `RetryAfter: X seconds` | L1 | Задержка X секунд (aiogram auto) | Снизить частоту отправки |
| **Blocked by user** | `Forbidden: bot was blocked` | L1 | Skip + пометить в DB | Не отправлять больше этому user |
| **Chat not found** | `chat not found` | L1 | Skip + лог | Очистить из scheduled messages |
| **Message too long** | `message is too long` | L2 | PR: add truncation | Проверить все точки генерации текста |

### 3.5. MCP (knowledge-mcp)

| Паттерн | Симптомы | Severity | Auto Action | Manual Fix |
|---------|----------|----------|-------------|------------|
| **Connection failure** | `MCP connection failed`, консультант не работает | L3 | Retry 3x, затем fallback без MCP | Проверить CF Workers status |
| **Timeout** | MCP >5с, пользователь ждёт | L1 | Fallback: ответ без MCP knowledge | Оптимизировать запрос / index |
| **Invalid response** | MCP вернул невалидный формат | L2 | PR: fix parsing | Проверить MCP server logs |

### 3.6. Scheduler

| Паттерн | Симптомы | Severity | Auto Action | Manual Fix |
|---------|----------|----------|-------------|------------|
| **Job failure** | Scheduled job бросил exception | L1 | Лог в error_logs, retry в след. цикл | Проверить error_logs → fix |
| **Pre-gen timeout** | Feed generation >60с для одного user | L1 | Skip user, retry в след. цикл | Оптимизировать промпт / batch |
| **Reminder failure** | Не отправились напоминания | L1 | Retry через 5 мин | Проверить schedule_time, blocked users |
| **Scheduler stuck** | Scheduler не запускается / висит | L4 | Escalate → restart | Проверить Railway logs, asyncio deadlock |

## 4. Проекция в Downstream

| Source (Pack) | Target (Downstream) | Формат |
|---------------|---------------------|--------|
| Эта сущность (§3) | `DS-ai-systems/fixer/runbook/patterns.yaml` | YAML (runtime) |
| Эта сущность (§3) | `core/unstick.py` (L1 in-process) | Python (embedded) |

## 5. Grafana Cloud Alerting

Независимый канал мониторинга (не зависит от процесса бота). Grafana Cloud подключён к Neon DB (PostgreSQL datasource).

### 5.1. Contact Point

| Параметр | Значение |
|----------|----------|
| **Тип** | Telegram |
| **Имя** | aist-bot-telegram |
| **Получатель** | DEVELOPER_CHAT_ID |
| **Формат** | HTML (🚨 GRAFANA ALERT → alertname: summary) |

### 5.2. Alert Rules

| # | Правило | Интервал | Порог | For | Severity | Что ловит |
|---|---------|----------|-------|-----|----------|-----------|
| 1 | **L3+ Critical Errors** | 5 мин | >0 L3/L4 не-эскалированных | 0s | critical | L3/L4 ошибки — немедленная реакция |
| 2 | **Unknown Error Spike** | 15 мин | >5 unknown с count≥3 | 5 мин | warning | Всплеск неклассифицированных — нужен triage для RUNBOOK |
| 3 | **Error Rate Anomaly** | 15 мин | >50 ошибок/час | 5 мин | warning | Аномальный уровень — проверить Claude API, Neon, Railway |
| 4 | **Bot Heartbeat Lost** | 1 час | >24ч без записей | 30 мин | info | Бот может быть остановлен |

### 5.3. Dashboard

`monitoring/grafana-dashboard.json` — 8 панелей: Errors (24h), L3+ Errors, Unknown Errors, Unique Errors, L1 Recoveries, Error Rate by Category, Severity Distribution, Recent Classified Errors, Unknown Errors (Triage).

**Setup:** `monitoring/setup-grafana-alerts.sh` (env vars: GRAFANA_URL, GRAFANA_TOKEN, GRAFANA_DS_UID, TG_BOT_TOKEN, TG_CHAT_ID).

## 6. L2 Auto-Fix Pipeline (TG Approval)

Автоматическая диагностика и исправление ошибок с подтверждением разработчика через Telegram.

### 6.1. Поток

```
error_logs (severity='L2', count≥3, last 15 min)
  ↓ scheduler (каждые 15 мин)
core/autofix.py → detect + fetch file from GitHub
  ↓
Claude Sonnet: диагноз + minimal fix + ArchGate (6 dims)
  ↓ (filter: confidence != low, archgate >= 8)
pending_fixes table → TG message [✅ Применить] [❌ Отклонить]
  ↓
✅ → GitHub API: branch fix/<key> → commit → PR
❌ → mark rejected
```

### 6.2. Ограничения безопасности

| Правило | Значение |
|---------|----------|
| Макс. файлов на fix | 3 |
| Макс. предложений за цикл | 3 |
| Защищённые файлы | db/models.py, core/scheduler.py, bot.py, config/ |
| Деду-пликация | Unique index на error_key (не предлагать повторно) |
| Всегда через PR | Никогда прямой push в main |
| ArchGate gate | Только решения с оценкой ≥8/10 |
| Graceful degradation | Без GITHUB_BOT_PAT — автофикс отключён |

### 6.3. Таблица pending_fixes

| Поле | Тип | Назначение |
|------|-----|-----------|
| error_log_id | INTEGER | Ссылка на ошибку |
| error_key | TEXT | Деду-пликация |
| status | TEXT | pending → approved → applied / rejected / failed |
| diagnosis | TEXT | Диагноз от Claude |
| archgate_eval | TEXT (JSON) | Оценка по 6 измерениям |
| proposed_diff | TEXT (JSON) | file_path + original_code + fixed_code |
| pr_url | TEXT | URL созданного PR |
| tg_message_id | BIGINT | Для редактирования сообщения после одобрения |

## 7. Связанные документы

- [DP.AISYS.014 Aist Bot](DP.AISYS.014-aist-bot.md) — паспорт бота
- [DP.ROLE.001 ИИ-агенты](DP.ROLE.001-platform-roles.md) — I7 Наладчик
