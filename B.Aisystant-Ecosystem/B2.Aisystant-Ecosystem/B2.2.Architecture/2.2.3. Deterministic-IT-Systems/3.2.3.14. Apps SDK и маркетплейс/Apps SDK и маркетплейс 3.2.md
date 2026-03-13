---

type: doc
audience: mixed
edit_mode: manual
layer: service
scope: local-edge
security: internal
status: draft
version: 0.1
created: 2025-11-12
---


# 15. Apps SDK и маркетплейс ассистентов

Платформа для создания, публикации и распространения ИИ-ассистентов и инструментов через декларативный SDK. Обеспечивает маркетплейс для монетизации и дистрибуции ассистентов, интеграцию с мультиагентной ОС и контроль качества публикаций.

## Назначение

Основная цель системы и решаемые задачи:
- **Декларативный SDK** — простой способ создания ИИ-ассистентов без глубоких технических знаний
- **Маркетплейс** — каталог ассистентов с рейтингами, отзывами и монетизацией
- **Интеграция с ОС ИИ** — бесшовный вызов инструментов через мультиагентную платформу
- **Контроль качества** — модерация, тестирование и безопасность публикаций
- **Монетизация** — распределение доходов создателям через токеномику
- **Минимальные разрешения** — безопасность через декларативные действия с ограниченными правами

## Архитектура

### Компоненты

1. **Apps SDK (Declarative SDK)**
   - Манифест ассистента (JSON/YAML описание возможностей)
   - Библиотека для создания Actions (атомарные операции)
   - Tools композиция (сборка сложных операций из Actions)
   - Локальное тестирование и отладка

2. **Маркетплейс (Marketplace)**
   - Каталог ассистентов с поиском и фильтрацией
   - Рейтинги и отзывы пользователей
   - Системы оплаты (фиат и токены)
   - Статистика использования и аналитика

3. **Registry & Distribution**
   - Реестр опубликованных ассистентов
   - Версионирование и управление релизами
   - CDN для дистрибуции манифестов и assets
   - Rollback и A/B тестирование

4. **Quality & Security**
   - Автоматическое тестирование (unit, integration)
   - Статический анализ и security scan
   - Модерация контента
   - Sandboxing и изоляция выполнения

5. **MCP Integration (Model Context Protocol)**
   - Адаптеры для вызова MCP инструментов
   - Протокол взаимодействия с ОС ИИ
   - Context passing и state management

### Технологический стек

- **Backend:** Node.js/Python для SDK, Go для Registry, Kubernetes для orchestration
- **Frontend:** Next.js для маркетплейса, React для SDK UI
- **База данных:** PostgreSQL (Frontmatter ассистентов), Redis (кеш), S3 (манифесты и assets)
- **Инфраструктура:** Kubernetes, Docker, GitHub Actions (CI/CD), Cloudflare CDN

## Интеграции

### Входящие интеграции

Разработчики и системы публикуют ассистентов:
- Разработчики ИИ-агентов — создание и публикация через SDK
- [[4.13. Система управления кейсами]] — специализированные ассистенты для кейсов
- Внешние разработчики — сообщество создателей

### Исходящие интеграции

Система интегрируется с:
- [[4.2. Операционная система ИИ-платформы]] — вызов инструментов ассистентов
- [[4.9. Биллинг]] — оплата за использование премиум-ассистентов
- [[Система баллов и лояльности 3.1]] — распределение доходов создателям
- [[4.14. Система идентификации и доступа (ORY)]] — авторизация публикации
- [[4.6. Система учета активностей (хаб активностей)]] — логирование использования
- [[3.4. Описание единого хранилища знаний (Memory Bank)]] — доступ ассистентов к знаниям

## API и контракты

### Основные эндпоинты

**SDK API (для разработчиков):**
```
POST /sdk/assistants                         # Создание нового ассистента
PUT  /sdk/assistants/:id                     # Обновление ассистента
POST /sdk/assistants/:id/publish             # Публикация в маркетплейс
POST /sdk/assistants/:id/test                # Тестирование локально
GET  /sdk/assistants/:id/manifest            # Получение манифеста
POST /sdk/assistants/:id/versions            # Создание новой версии
```

**Marketplace API (для пользователей):**
```
GET  /marketplace/assistants                 # Список ассистентов (с фильтрами)
GET  /marketplace/assistants/:id             # Детали ассистента
POST /marketplace/assistants/:id/install     # Установка ассистента
POST /marketplace/assistants/:id/review      # Оставить отзыв
GET  /marketplace/assistants/:id/stats       # Статистика использования
GET  /marketplace/categories                 # Категории ассистентов
```

**Execution API (для ОС ИИ):**
```
POST /execute/assistant/:id/action           # Выполнение действия
POST /execute/assistant/:id/tool             # Вызов инструмента
GET  /execute/assistant/:id/capabilities     # Получение возможностей
POST /execute/assistant/:id/context          # Передача контекста
```

**Admin API:**
```
GET  /admin/assistants/pending               # Ассистенты на модерации
POST /admin/assistants/:id/approve           # Одобрить публикацию
POST /admin/assistants/:id/reject            # Отклонить публикацию
GET  /admin/analytics                        # Аналитика маркетплейса
```

### События

Система генерирует следующие события:
- `assistant.created` — создан новый ассистент
- `assistant.published` — ассистент опубликован в маркетплейс
- `assistant.installed` — ассистент установлен пользователем
- `assistant.executed` — выполнено действие ассистента
- `assistant.reviewed` — добавлен отзыв
- `assistant.updated` — обновлена версия ассистента
- `revenue.distributed` — распределены доходы создателю

## Хранилище данных

### Схема данных

Основные сущности и их поля:
- **Assistant**: id, name, description, author_id, category, version, manifest_url, icon_url, created_at
- **AssistantVersion**: id, assistant_id, version, manifest, changelog, published_at, status
- **Action**: id, assistant_id, name, description, parameters_schema, permissions, code_ref
- **Tool**: id, assistant_id, name, description, actions (composition), input_schema
- **Installation**: id, user_id, assistant_id, version, installed_at, enabled
- **Review**: id, assistant_id, user_id, rating, comment, created_at
- **Usage**: id, assistant_id, user_id, action_name, timestamp, duration, success
- **Revenue**: id, assistant_id, period, total_revenue, author_share, mentor_share, treasury_share

### Retention policy

- **Активные ассистенты:** Бессрочно (пока не удалены автором)
- **Deprecated версии:** 1 год после deprecation
- **Логи использования:** 90 дней (детальные), 2 года (агрегированные)
- **Отзывы:** Бессрочно
- **История доходов:** 5 лет (для налоговой отчётности)

## Метрики и мониторинг

### Ключевые метрики

| Метрика | Целевое значение | Текущее |
|---------|------------------|---------|
| Доступность маркетплейса | 99.9% | — |
| Response time для каталога (p95) | <300ms | — |
| Response time для execution (p95) | <500ms | — |
| Successful execution rate | >95% | — |
| Number of published assistants | >100 | — |
| Active users (MAU) | >1000 | — |
| Average rating | >4.0/5.0 | — |

### Алерты

**Критические:**
- Execution error rate > 10% за последние 15 минут
- Маркетплейс недоступен
- Database connection errors
- Security vulnerability detected

**Предупреждения:**
- Execution latency (p95) > 1s за последние 15 минут
- Low rating on trending assistant (<3.0)
- Moderation queue > 20 pending items
- CDN cache hit rate < 80%

## Roadmap

### v1.0 (MVP)
- [ ] Apps SDK с базовыми возможностями (Actions, Tools)
- [ ] Простой маркетплейс с каталогом и поиском
- [ ] MCP интеграция для вызова из ОС ИИ
- [ ] Базовая модерация и тестирование
- [ ] Интеграция с биллингом (фиатные платежи)
- [ ] Документация и примеры для разработчиков

### v1.1
- [ ] Версионирование и rollback ассистентов
- [ ] Рейтинги, отзывы и рекомендации
- [ ] Токен-based монетизация (SplitRule)
- [ ] A/B тестирование для ассистентов
- [ ] Advanced analytics для создателей
- [ ] Sandboxing и расширенная безопасность

### v2.0
- [ ] Федеративный маркетплейс (кросс-платформенность)
- [ ] AI-powered ассистент для создания ассистентов (meta-assistant)
- [ ] Marketplace SDK для enterprise (private marketplace)
- [ ] Децентрализованная дистрибуция (IPFS/blockchain)
- [ ] Интеграция с внешними маркетплейсами (OpenAI GPT Store, etc.)

## Связанные документы

- [[4.1. Список подсистем]] — реестр всех систем
- [[4.2. Операционная система ИИ-платформы]] — вызов ассистентов
- [[4.9. Биллинг]] — монетизация
- [[Система баллов и лояльности 3.1]] — распределение доходов
- [[4.0. Информация]] — обзор раздела Системы
- [[0.7. Классификация документов и теги]] — Frontmatter

## История изменений

| Дата | Версия | Описание |
|------|--------|----------|
| 2025-11-12 | 0.1 | Первое создание документа |

---

**Status:** 🟡 Draft
**Owner:** AI Platform Team
**Last Updated:** 2025-11-12
