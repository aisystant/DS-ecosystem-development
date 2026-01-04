# API ДЗ-чекера v2 — Инструкция для интеграции

## Эндпоинт

```
POST https://tseren.app.n8n.cloud/webhook/check
Content-Type: application/json; charset=utf-8
```

---

## Формат запроса

```json
{
  "question_text": "Текст вопроса из ДЗ",
  "answer_text": "Ответ стажера",
  "course_name": "Название курса",
  "section_name": "Название раздела"
}
```

### Поля

| Поле | Тип | Обязательное | Описание |
|------|-----|--------------|----------|
| `question_text` | string | **Да** | Текст вопроса домашнего задания |
| `answer_text` | string | **Да** | Ответ стажера для проверки |
| `course_name` | string | Нет | Название курса (для контекста) |
| `section_name` | string | Нет | Название раздела (для контекста) |

---

## Формат ответа (успех)

**HTTP 200 OK**

```json
{
  "ok": true,
  "request_id": "req_1704389288123_a1b2c3",
  "checked_at": "2026-01-04T17:30:00.000Z",
  "verdict": "needs_revision",
  "score": 65,
  "strengths": [
    "Упоминание о формировании нейронных связей",
    "Понимание важности структурирования мыслей"
  ],
  "issues": [
    {
      "criterion": "полнота",
      "issue": "Недостаточно полный ответ",
      "suggestion": "Расширить ответ, добавив информацию о культурной практике"
    },
    {
      "criterion": "терминология",
      "issue": "Ограниченное использование терминологии",
      "suggestion": "Использовать термины: экзокортекс, мыслитель письмом"
    }
  ],
  "next_step": "Дополнить ответ более подробным объяснением",
  "comment": "**На доработку** (65/100)\n\n**Сильные стороны:**\n- Упоминание о формировании нейронных связей\n..."
}
```

### Поля ответа

| Поле | Тип | Описание |
|------|-----|----------|
| `ok` | boolean | `true` если проверка выполнена |
| `request_id` | string | Уникальный ID запроса (для логов) |
| `checked_at` | string | Время проверки (ISO 8601) |
| `verdict` | string | Вердикт: `accepted`, `needs_revision`, `rejected` |
| `score` | number | Балл 0–100 |
| `strengths` | array | Список сильных сторон ответа |
| `issues` | array | Список замечаний с рекомендациями |
| `next_step` | string | Рекомендация следующего шага |
| `comment` | string | Готовый комментарий в Markdown |

### Вердикты

| Verdict | Score | Значение |
|---------|-------|----------|
| `accepted` | 90–100 | Ответ принят |
| `needs_revision` | 60–89 | На доработку |
| `rejected` | 0–59 | Не принят |

---

## Формат ответа (ошибка)

**HTTP 400 Bad Request**

```json
{
  "ok": false,
  "request_id": "req_...",
  "error": {
    "code": "bad_request",
    "message": "Missing required fields: question_text, answer_text",
    "details": {
      "missing": ["question_text", "answer_text"]
    }
  }
}
```

---

## Пример интеграции (JavaScript)

```javascript
async function checkHomework(questionText, answerText, courseName = null) {
  const response = await fetch('https://tseren.app.n8n.cloud/webhook/check', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json; charset=utf-8'
    },
    body: JSON.stringify({
      question_text: questionText,
      answer_text: answerText,
      course_name: courseName
    })
  });

  if (!response.ok) {
    throw new Error(`HTTP ${response.status}`);
  }

  const result = await response.json();

  if (!result.ok) {
    throw new Error(result.error?.message || 'Unknown error');
  }

  return result;
}

// Использование
const result = await checkHomework(
  'Почему важно развивать мышление письмом?',
  'Мышление письмом помогает структурировать мысли.',
  'Системное саморазвитие'
);

console.log(result.verdict);  // "needs_revision"
console.log(result.score);    // 65
console.log(result.comment);  // Markdown-комментарий для отображения
```

---

## Пример интеграции (React)

```jsx
import { useState } from 'react';

function HomeworkChecker({ question, courseName }) {
  const [answer, setAnswer] = useState('');
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleCheck = async () => {
    setLoading(true);
    try {
      const response = await fetch('https://tseren.app.n8n.cloud/webhook/check', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json; charset=utf-8' },
        body: JSON.stringify({
          question_text: question,
          answer_text: answer,
          course_name: courseName
        })
      });
      const data = await response.json();
      setResult(data);
    } catch (error) {
      console.error('Check failed:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <textarea
        value={answer}
        onChange={(e) => setAnswer(e.target.value)}
        placeholder="Введите ваш ответ..."
      />
      <button onClick={handleCheck} disabled={loading}>
        {loading ? 'Проверка...' : 'Проверить с ИИ'}
      </button>

      {result && (
        <div className={`result ${result.verdict}`}>
          <h3>{result.verdict === 'accepted' ? '✓ Принято' : 'На доработку'}</h3>
          <p>Балл: {result.score}/100</p>
          <div dangerouslySetInnerHTML={{ __html: marked(result.comment) }} />
        </div>
      )}
    </div>
  );
}
```

---

## Тестирование

### cURL (Linux/Mac)

```bash
curl -X POST https://tseren.app.n8n.cloud/webhook/check \
  -H "Content-Type: application/json; charset=utf-8" \
  -d '{
    "question_text": "Почему важно развивать мышление письмом?",
    "answer_text": "Это помогает думать лучше."
  }'
```

### PowerShell (Windows)

```powershell
$body = @{
    question_text = "Почему важно развивать мышление письмом?"
    answer_text = "Это помогает думать лучше."
} | ConvertTo-Json -Compress

$bytes = [System.Text.Encoding]::UTF8.GetBytes($body)

Invoke-RestMethod -Uri "https://tseren.app.n8n.cloud/webhook/check" -Method POST -ContentType "application/json; charset=utf-8" -Body $bytes
```

---

## Рекомендации для UI

1. **Кнопка "Проверить с ИИ"** — показывать рядом с полем ответа
2. **Индикатор загрузки** — проверка занимает 3–10 секунд
3. **Отображение результата:**
   - Использовать `comment` (готовый Markdown)
   - Или собрать свой UI из `verdict`, `score`, `strengths`, `issues`
4. **Цветовая индикация:**
   - `accepted` → зелёный
   - `needs_revision` → жёлтый
   - `rejected` → красный

---

## Ограничения

- Таймаут: ~30 секунд
- Кодировка: UTF-8 обязательна
- Размер ответа: до 10 000 символов

---

## Контакты

При проблемах — обращаться к команде разработки экосистемы.
