# Docs Agent

Документалист экосистемы — агент для создания, форматирования и поддержки качества документации.

## Быстрый старт

```bash
# 1. Создать новую систему
python3 agents-core/docs/create_document.py \
  --type system \
  --number 13 \
  --title "Система аналитики"

# 2. Проверить качество всех документов
python3 agents-core/docs/check_quality.py

# 3. Проверить конкретный документ
python3 agents-core/docs/check_quality.py \
  --path "content/4. Системы/4.12. Memory Bank.md"
```

## Доступные команды

### create_document.py

Создание нового документа на основе шаблона.

**Примеры:**

```bash
# Создать документ системы
python3 agents-core/docs/create_document.py \
  --type system \
  --number 13 \
  --title "Система аналитики"

# Создать документ агента
python3 agents-core/docs/create_document.py \
  --type agent \
  --title "Agent: Reviewer" \
  --template "content/templates/Agent-Template.md"

# Создать произвольный документ
python3 agents-core/docs/create_document.py \
  --title "Новый документ" \
  --layer "methodology" \
  --doc-type "doc"
```

**Опции:**
- `--type` — тип документа (system, agent, custom)
- `--number` — номер системы (для type=system)
- `--title` — название документа
- `--template` — путь к шаблону (для type=custom)
- `--output` — путь для сохранения
- `--layer` — семантический слой (service, methodology, ...)
- `--doc-type` — тип артефакта (doc, data, code, ...)

**Output:**
- Черновик в `artifacts/docs/drafts/`
- Автоматический frontmatter
- Структура из шаблона

### check_quality.py

Проверка качества документации по нескольким метрикам.

**Примеры:**

```bash
# Полная проверка всех документов
python3 agents-core/docs/check_quality.py

# Проверка конкретного файла
python3 agents-core/docs/check_quality.py \
  --path "content/4. Системы/4.12. Memory Bank.md"

# Проверка с созданием детального отчета
python3 agents-core/docs/check_quality.py \
  --full-report \
  --output "artifacts/docs/reviews/quality-report.md"

# Для CI: fail если score < 60
python3 agents-core/docs/check_quality.py --fail-below 60
```

**Опции:**
- `--path` — путь к файлу/директории для проверки
- `--output` — путь для сохранения отчета
- `--fail-below` — выйти с кодом 1 если score ниже указанного
- `--full-report` — показать полный отчет в консоли

**Метрики:**
- **Frontmatter** (30%) — наличие и корректность метаданных
- **Links** (20%) — валидность wiki-ссылок
- **Structure** (20%) — правильная иерархия заголовков
- **Readability** (30%) — читаемость текста (Flesch score)

## Структура агента

```
agents-core/docs/
├── README.md              # Этот файл
├── manifest.json          # Манифест агента
├── create_document.py     # Создание документов
├── check_quality.py       # Проверка качества
├── config.yaml           # Конфигурация (будущее)
└── prompts/              # AI промпты (будущее)
```

## Паспорт агента

Полное описание агента, роли, workflow и метрик:
- [content/agents/docs.md](../../content/agents/docs.md)

## Интеграция с CI/CD

Docs Agent можно использовать в GitHub Actions:

```yaml
# .github/workflows/docs-check.yml
- name: Check documentation quality
  run: |
    python3 agents-core/docs/check_quality.py --fail-below 60
```

## Roadmap

### v1.0 (текущая)
- ✅ Создание документов из шаблонов
- ✅ Проверка качества (frontmatter, links, structure, readability)
- ✅ Генерация отчетов

### v1.1 (в планах)
- [ ] Автосинхронизация документации (sync_documentation.py)
- [ ] Генерация туториалов (generate_tutorial.py)
- [ ] AI-улучшение текстов (OpenAI API integration)
- [ ] Автоисправление простых ошибок (--auto-fix)

### v2.0 (будущее)
- [ ] Автогенерация API docs из кода
- [ ] Semantic search по документации
- [ ] Многоязычность (перевод)
- [ ] Real-time preview в Obsidian

## Troubleshooting

### Ошибка: "Шаблон не найден"

**Проблема:** `FileNotFoundError: Шаблон не найден: ...`

**Решение:**
1. Проверьте что запускаете скрипт из корня проекта
2. Проверьте что шаблон существует в `content/templates/`

### Ошибка: "Permission denied"

**Проблема:** Скрипты не исполняются

**Решение:**
```bash
chmod +x agents-core/docs/*.py
```

### Низкий readability score

**Проблема:** Документ получает низкий score по читаемости

**Решение:**
1. Разбейте длинные предложения (>25 слов)
2. Используйте активный залог
3. Избегайте сложных технических терминов без пояснений
4. Добавьте примеры и списки для лучшей структуры

## Вклад в агента

Хотите улучшить Docs Agent?

1. Создайте issue с предложением
2. Fork репозиторий
3. Добавьте функциональность
4. Создайте PR с описанием изменений

См. [CONTRIBUTING.md](../../CONTRIBUTING.md)

## Контакты

- Паспорт агента: [content/agents/docs.md](../../content/agents/docs.md)
- Индекс всех агентов: [content/agents/00-Index.md](../../content/agents/00-Index.md)
- Issues: [GitHub Issues](https://github.com/YOUR_ORG/DS-ecosystem-development/issues)

---

**Version:** 1.0
**Status:** ✅ Production Ready
**Last Updated:** 2025-11-12
