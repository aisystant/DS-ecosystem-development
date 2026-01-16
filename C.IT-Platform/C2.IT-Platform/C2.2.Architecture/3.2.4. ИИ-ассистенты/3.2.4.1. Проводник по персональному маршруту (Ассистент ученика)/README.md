# 3.2.4.1. Проводник по персональному маршруту (Ассистент ученика)

ИИ-ассистент для сопровождения учеников по персональной траектории развития.

---

## Быстрые ссылки

| Ресурс | Ссылка |
|--------|--------|
| **Репозиторий** | [github.com/aisystant/fsm-mcp](https://github.com/aisystant/fsm-mcp) |
| **MCP-эндпоинт** | `https://fsm-mcp.aisystant.workers.dev/mcp` |
| **Архитектура** | [[FSM-архитектура ИИ-ассистентов 3.2]] |

---

## Документы в этой папке

| Документ | Описание |
|----------|----------|
| [[Описание ИИ-ассистента Проводник (Ассистент Ученика) 3.2]] | Назначение, ступени развития, сценарии использования |
| [[privacy-policy]] | Privacy Policy для OpenAI Apps |
| [[terms-of-service]] | Terms of Service для OpenAI Apps |
| [[demo-recording-guide]] | Инструкция для записи демо-видео |

---

## OpenAI Apps — Документы для ревью

Для регистрации в [OpenAI Apps](https://platform.openai.com/apps-manage) требуются:

| Требование | Файл | Статус |
|------------|------|--------|
| **Privacy Policy URL** | [privacy-policy.md](./privacy-policy.md) | Создан |
| **Terms of Service URL** | [terms-of-service.md](./terms-of-service.md) | Создан |
| **Demo Recording URL** | [demo-recording-guide.md](./demo-recording-guide.md) | Инструкция готова, видео нужно записать |

### Публичные URL

После публикации через GitHub Pages или другой хостинг, URL будут выглядеть примерно так:

```
Privacy Policy: https://aisystant.github.io/ecosystem-development/.../privacy-policy.html
Terms of Service: https://aisystant.github.io/ecosystem-development/.../terms-of-service.html
```

**Альтернативы для публикации:**
- GitHub Pages (этот репозиторий)
- Notion Public Page
- Google Docs (Published)
- Отдельная страница на aisystant.com

---

## Архитектура

```
Ассистент = LLM + Системный промпт + MCP-сервер (fsm-mcp)
```

Проводник построен на основе **FSM-архитектуры** — каждое состояние диалога описано в markdown-файле, а MCP-сервер выдаёт инструкции по запросу LLM.

Подробности: [[FSM-архитектура ИИ-ассистентов 3.2]]

---

## Связанные документы

- [[FSM-архитектура ИИ-ассистентов 3.2]] — ADR: архитектурное решение
- [[Модель данных цифрового двойника 3.2]] — данные для работы Проводника
- [[Уровни мастерства — квалификации и ступени 2.2]] — методика ступеней

---

**Последнее обновление:** 2025-12-24
