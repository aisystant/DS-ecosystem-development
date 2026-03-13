# D.1 Спецификация API ДЗ-чекера

Спецификация n8n Webhook API для интеграции LMS с ДЗ-чекером (v0.1).

---

## Общие сведения

| Параметр | Значение |
|----------|----------|
| Реализация | n8n Webhook |
| Базовый URL (prod) | `https://<n8n-host>/webhook/check` |
| Базовый URL (test) | `https://<n8n-host>/webhook-test/check` |
| Протокол | HTTPS |
| Формат данных | JSON |
| Кодировка | UTF-8 |
| Аутентификация | v0.1: отсутствует |

---

## Endpoints

### POST /webhook/check

Синхронная проверка одного ответа стажёра.

#### Запрос

**Headers:**
```
Content-Type: application/json
```

**Body:**
```json
{
  "answer_text": "string (required)",
  "question_text": "string (required)",
  "course_name": "string (required)",
  "section_name": "string (required)"
}
```

| Поле | Тип | Обязательное | Описание |
|------|-----|--------------|----------|
| `answer_text` | string | Да | Текст ответа стажёра |
| `question_text` | string | Да | Текст вопроса/пункта чеклиста |
| `course_name` | string | Да | Название курса (текстовое, без идентификаторов) |
| `section_name` | string | Да | Название раздела из дерева навигации |

**Пример:**
```json
{
  "answer_text": "Любая модель части физического мира фокусируется на одних свойствах и опускает другие...",
  "question_text": "Почему физический мир может иметь множество описаний?",
  "course_name": "Системное мышление",
  "section_name": "Физический мир и ментальное пространство"
}
```

#### Ответ (успех)

**Status:** `200 OK`

**Body:**
```json
{
  "comment": "string",
  "checked_at": "string (ISO 8601)",
  "raw_llm": "object"
}
```

| Поле | Тип | Описание |
|------|-----|----------|
| `comment` | string | Форматированный комментарий для стажёра (Markdown) |
| `checked_at` | string | Время проверки в формате ISO 8601 |
| `raw_llm` | object | Сырой ответ LLM (для отладки и аналитики) |

**Пример:**
```json
{
  "comment": "**✓ Принято** (85/100)\n\n**Сильные стороны:**\n- Верно указано ключевое положение...\n\n**Замечания:**\n- Не использован термин «описание системы»...\n\n**Следующий шаг:**\nПопробуйте привести ещё один пример...",
  "checked_at": "2025-12-31T12:00:00.000Z",
  "raw_llm": {
    "verdict": "accepted",
    "score": 85,
    "strengths": ["Верно указано ключевое положение"],
    "issues": [{"criterion": "terminology", "issue": "Не использован термин «описание системы»", "suggestion": "Используйте терминологию из материалов"}],
    "next_step": "Попробуйте привести ещё один пример",
    "criterion_scores": {"main_idea": 40, "example": 25, "terminology": 10, "completeness": 10}
  }
}
```

---

## Структура raw_llm

Сырой ответ LLM содержит структурированные данные проверки:

```json
{
  "verdict": "accepted | needs_revision | rejected",
  "score": 0-100,
  "strengths": ["string", ...],
  "issues": [
    {
      "criterion": "string",
      "issue": "string",
      "suggestion": "string"
    }
  ],
  "next_step": "string",
  "criterion_scores": {
    "criterion_id": score,
    ...
  }
}
```

| Поле | Тип | Описание |
|------|-----|----------|
| `verdict` | string | Вердикт: accepted, needs_revision, rejected |
| `score` | number | Общий балл 0–100 |
| `strengths` | array | Список сильных сторон ответа |
| `issues` | array | Список замечаний с рекомендациями |
| `next_step` | string | Рекомендация для дальнейшего изучения |
| `criterion_scores` | object | Баллы по отдельным критериям |

---

## Коды ошибок

| Код | Описание | Когда возникает |
|-----|----------|-----------------|
| `400 Bad Request` | Некорректный запрос | Отсутствуют обязательные поля |
| `500 Internal Server Error` | Внутренняя ошибка | Ошибка LLM API или workflow |
| `503 Service Unavailable` | Сервис недоступен | LLM API недоступен |

**Формат ошибки 400:**
```json
{
  "status": 400,
  "error": "Missing: answer_text, question_text"
}
```

---

## Валидация (Code node)

Валидация выполняется первой Code-нодой в workflow:

```javascript
const body = items[0]?.json?.body ?? {};
const required = ["answer_text", "question_text", "course_name", "section_name"];
const missing = required.filter(k => !body[k]);

if (missing.length) {
  return [{ json: { status: 400, error: `Missing: ${missing.join(", ")}` } }];
}

return [{ json: body }];
```

---

## Пример интеграции (curl)

```bash
curl -X POST https://n8n.example.com/webhook/check \
  -H "Content-Type: application/json" \
  -d '{
    "answer_text": "Ответ стажёра...",
    "question_text": "Текст вопроса...",
    "course_name": "Системное мышление",
    "section_name": "Физический мир и ментальное пространство"
  }'
```

---

## Пример интеграции (JavaScript)

```javascript
async function checkHomework(answer, question, course, section) {
  const response = await fetch('/webhook/check', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      answer_text: answer,
      question_text: question,
      course_name: course,
      section_name: section
    })
  });

  if (response.status === 400) {
    throw new Error('Ошибка в запросе, проверьте текст ответа');
  }

  if (response.status >= 500) {
    throw new Error('Сервис временно недоступен, попробуйте позже');
  }

  if (!response.ok) {
    throw new Error(`HTTP ${response.status}`);
  }

  return await response.json();
}
```

---

## Ограничения v0.1

1. **Синхронный режим** — ответ возвращается в том же соединении
2. **Без аутентификации** — предполагается проксирование через LMS
3. **Без rate limiting** — контроль частоты на стороне LMS
4. **Результат не сохраняется** — только возврат клиенту

---

## URL для разных режимов

| Режим | URL | Использование |
|-------|-----|---------------|
| Production | `/webhook/check` | Боевое использование |
| Test | `/webhook-test/check` | Только при Execute в редакторе n8n |

**Важно:** Тестовый URL работает только когда workflow открыт в редакторе n8n и запущен через Execute.

---

## Связанные документы

- [Общее описание Проверяльщика ДЗ](../Общее%20описание%20Проверяльщика%20ДЗ%20(ДЗ-чекер)%203.2.md)
- [D.5 Требования к LMS](./D.5%20Требования%20к%20LMS.md)

---

**Версия:** 0.1
**Дата:** 2025-12-31
**Статус:** Реализовано (n8n webhook)
