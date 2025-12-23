# D.1 Спецификация API ДЗ-чекера

Спецификация HTTP API для интеграции LMS с ДЗ-чекером (v0.1).

---

## Общие сведения

| Параметр | Значение |
|----------|----------|
| Базовый URL | `https://<homework-checker-host>/` |
| Протокол | HTTPS |
| Формат данных | JSON |
| Кодировка | UTF-8 |
| Аутентификация | v0.1: отсутствует (внутренняя сеть) |

---

## Endpoints

### POST /check

Синхронная проверка одного ответа студента.

#### Запрос

**Headers:**
```
Content-Type: application/json; charset=utf-8
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
| `answer_text` | string | Да | Текст ответа студента |
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
  "checked_at": "string (ISO 8601)"
}
```

| Поле | Тип | Описание |
|------|-----|----------|
| `comment` | string | Форматированный комментарий для студента (Markdown) |
| `checked_at` | string | Время проверки в формате ISO 8601 |

**Пример:**
```json
{
  "comment": "**✓ Принято** (85/100)\n\n**Сильные стороны:**\n- Верно указано ключевое положение...\n\n**Замечания:**\n- Не использован термин «описание системы»...\n\n**Следующий шаг:**\nПопробуйте привести ещё один пример...\n\n---\n*Проверено: Claude 3.5 Sonnet*\n*По материалам: Физический мир и ментальное пространство*",
  "checked_at": "2025-09-08T20:35:00Z"
}
```

---

## Коды ошибок

| Код | Описание | Когда возникает |
|-----|----------|-----------------|
| `400 Bad Request` | Некорректный запрос | Отсутствуют обязательные поля, невалидный JSON |
| `500 Internal Server Error` | Внутренняя ошибка | Ошибка LLM API, ошибка репозитория руководств |
| `503 Service Unavailable` | Сервис недоступен | LLM API недоступен |

**Формат ошибки:**
```json
{
  "error": "string",
  "details": "string (optional)"
}
```

---

## Health Check

### GET /health

Проверка работоспособности сервиса.

**Ответ:**
```json
{
  "status": "ok",
  "version": "0.1"
}
```

---

## Ограничения v0.1

1. **Синхронный режим** — ответ возвращается в том же соединении
2. **Без аутентификации** — предполагается работа во внутренней сети
3. **Без rate limiting** — контроль частоты на стороне LMS
4. **Результат не сохраняется** — только возврат в LMS

---

## Пример интеграции (curl)

```bash
curl -X POST https://homework-checker.internal/check \
  -H "Content-Type: application/json" \
  -d '{
    "answer_text": "Ответ студента...",
    "question_text": "Текст вопроса...",
    "course_name": "Системное мышление",
    "section_name": "Физический мир и ментальное пространство"
  }'
```

---

## Пример интеграции (JavaScript)

```javascript
async function checkHomework(answer, question, course, section) {
  const response = await fetch('https://homework-checker.internal/check', {
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

  if (!response.ok) {
    throw new Error(`HTTP ${response.status}`);
  }

  return await response.json();
}
```

---

## Связанные документы

- [Общее описание Проверяльщика ДЗ](../Общее%20описание%20Проверяльщика%20ДЗ%20(ДЗ-чекер)%203.2.md)
- [D.5 Требования к LMS](./D.5%20Требования%20к%20LMS.md)
- Рабочий файл: `agents-core/homework-checker/schemas/check_request.json`
- Рабочий файл: `agents-core/homework-checker/schemas/check_result.json`

---

**Версия:** 0.1
**Дата:** 2025-12-23
**Статус:** Для согласования с командой LMS
