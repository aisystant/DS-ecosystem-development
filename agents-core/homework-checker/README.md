# ДЗ-чекер (Homework Checker)

Агент для автоматической проверки домашних заданий с использованием LLM.

**Описание:** [content/.../3.2.4.3. Проверяльщик ДЗ/](../../content/3.%20Экосистема%20развития%20(Система%20создания)/3.2.%20Архитектура%20—%20Платформа%20и%20подсистемы/3.2.4.%20ИИ-ассистенты/3.2.4.3.%20Проверяльщик%20ДЗ/)

---

## Быстрый старт

### Требования

- Python 3.10+
- API-ключ Anthropic

### Установка

```bash
cd agents-core/homework-checker
pip install -r requirements.txt  # TODO: создать
cp config.yaml config.local.yaml
# Отредактировать config.local.yaml, указать API-ключ
```

### Запуск HTTP-сервера (v0.1)

```bash
export ANTHROPIC_API_KEY="sk-..."
python3 server.py --port 8080
```

### Тестовый запрос

```bash
curl -X POST http://localhost:8080/check \
  -H "Content-Type: application/json" \
  -d @examples/request_example.json
```

---

## Структура

```
homework-checker/
├── server.py              # HTTP-сервер (точка входа v0.1)
├── check.py               # Логика проверки
├── config.yaml            # Конфигурация (шаблон)
├── manifest.json          # Метаданные агента
├── schemas/               # JSON-схемы для валидации
│   ├── check_request.json
│   └── check_result.json
├── data/
│   ├── prompts/           # Промпты для LLM
│   │   ├── system.txt
│   │   └── check_template.txt
│   ├── rubrics.yaml       # Рубрики проверки
│   └── questions_map.yaml # Карта вопросов (v0.2)
└── examples/              # Примеры данных
    ├── request_example.json
    └── result_example.json
```

---

## Конфигурация

Скопируйте `config.yaml` в `config.local.yaml` и настройте:

```yaml
llm:
  provider: anthropic
  model: claude-3-5-sonnet-20241022
  # api_key: берётся из переменной окружения ANTHROPIC_API_KEY

thresholds:
  auto_accept: 80    # Автоматически принять
  needs_review: 60   # Отправить наставнику
  auto_reject: 40    # Автоматически отклонить
```

---

## API (v0.1)

### POST /check

Синхронная проверка одного ответа.

**Запрос:** см. `schemas/check_request.json`
**Ответ:** см. `schemas/check_result.json`

---

**Версия:** 0.1
**Статус:** В разработке
