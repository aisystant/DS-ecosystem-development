# C2.2. IT-Platform — Architecture

> **Source-of-truth (domain)**: [PACK-digital-platform](../../../../PACK-digital-platform/)
>
> Реализационные решения ИТ-платформы. Здесь живёт то, что зависит от конкретных вендоров, фреймворков, инфраструктуры.

## Подразделы

| Папка | Содержит |
|-------|----------|
| [Stack-and-Infrastructure](Stack-and-Infrastructure/) | Топология деплоя, стек, circuit breaker |
| [Data-Stores](Data-Stores/) | Neon, PostgreSQL, pgvector — схемы и конфигурации |
| [Identity-and-Access](Identity-and-Access/) | Модели доступа, Ory, RLS |
| [System-Implementations](System-Implementations/) | ADR, реестр детерминированных систем |

## HD #29 — Pack vs DS

**Тест:** «Заменили вендора/фреймворк — утверждение стало ложным? Да → тут (DS). Нет → в Pack.»
