# Задание: Создание персонального Репозитория знаний

## Цель

Создать структуру GitHub-репозитория для хранения персонального контента в виде чанков (до 10 000 знаков), с возможностью автоматического импорта из внешних источников и ручного редактирования.

## Требования к структуре

### 1. Основные директории

Создать следующую структуру папок:

```
knowledge-repository/
├── README.md                          # Описание репозитория
├── .github/workflows/                 # CI/CD для автоимпорта
├── config/                            # Конфигурационные файлы
├── club/                              # Контент из Клуба
│   ├── posts/                         # Мои посты
│   └── comments/                      # Мои комментарии
│       ├── on-posts/                  # Под постами других
│       └── on-my-posts/               # Под моими постами
├── lms/                               # Контент из LMS
│   ├── homework-reviews/              # Комментарии под ДЗ стажеров
│   └── my-homework/                   # Мои ДЗ
├── manual/                            # Ручные добавления
│   ├── notes/                         # Заметки
│   ├── reflections/                   # Рефлексии
│   └── projects/                      # Проектные материалы
├── external/                          # Импорт из других репо
│   └── ecosystem-development/         # Контент из ecosystem-development
├── metadata/                          # Метаданные
└── scripts/                           # Утилиты
```

### 2. Формат чанка

Каждый чанк — это markdown файл с frontmatter-метаданными:

```markdown
---
id: chunk_YYYYMMDD_NNN
source: club/posts | club/comments | lms/homework-reviews | manual/notes | external
type: post | comment | homework-review | note | reflection | project
created: ISO8601 datetime
updated: ISO8601 datetime
author: Tseren Tserenov
tags: [список тегов]
word_count: число слов
char_count: число символов (макс 10000)
related_chunks: [список ID связанных чанков]
original_url: URL источника (если есть)
context: краткое описание контекста
---

# Заголовок

Текст контента (макс 10 000 знаков)
```

### 3. Конфигурационные файлы

#### `config/sources.yaml`

```yaml
sources:
  club:
    url: "https://club.systemschool.ru"
    api_endpoint: "/api/v1/posts"
    auth_token_env: "CLUB_API_TOKEN"
    user_id: "tseren_tserenov"
    import_types:
      - posts
      - comments
    
  lms:
    url: "https://lms.systemschool.ru"
    api_endpoint: "/api/v1/reviews"
    auth_token_env: "LMS_API_TOKEN"
    user_id: "tseren_tserenov"
    import_types:
      - homework_reviews
  
  external_repos:
    - name: "ecosystem-development"
      url: "https://github.com/aisystant/ecosystem-development"
      branch: "main"
      paths:
        - "content/**/*.md"
      exclude:
        - "**/архив/**"

chunk_settings:
  max_chars: 10000
  split_strategy: "semantic"  # разбивка по смыслу, не посередине предложения
  frontmatter_required: true
```

#### `config/metadata-schema.yaml`

```yaml
metadata_schema:
  required_fields:
    - id
    - source
    - type
    - created
    - author
    - char_count
  
  optional_fields:
    - updated
    - tags
    - related_chunks
    - original_url
    - context
    - word_count
  
  types:
    - post
    - comment
    - homework-review
    - note
    - reflection
    - project
    - document
```

### 4. Скрипты для работы

#### `scripts/import_from_club.py`

Скрипт для импорта постов и комментариев из Клуба:

```python
"""
Импортирует посты и комментарии из Клуба.
Использование:
  python scripts/import_from_club.py --from-date 2025-01-01 --to-date 2025-01-11
"""
# TODO: Реализовать
# 1. Подключение к API Клуба
# 2. Получение списка постов и комментариев пользователя
# 3. Создание чанков с метаданными
# 4. Сохранение в папку club/
# 5. Автоматическая разбивка на чанки, если текст > 10000 символов
```

#### `scripts/import_from_lms.py`

Скрипт для импорта комментариев из LMS:

```python
"""
Импортирует комментарии под ДЗ стажеров из LMS.
Использование:
  python scripts/import_from_lms.py --student-id all
"""
# TODO: Реализовать
# 1. Подключение к API LMS
# 2. Получение списка комментариев под ДЗ
# 3. Создание чанков с метаданными
# 4. Сохранение в папку lms/homework-reviews/
```

#### `scripts/import_from_repo.py`

Скрипт для импорта из других репозиториев:

```python
"""
Импортирует контент из других GitHub репозиториев.
Использование:
  python scripts/import_from_repo.py --repo ecosystem-development
"""
# TODO: Реализовать
# 1. Клонирование/обновление репозитория
# 2. Копирование указанных файлов
# 3. Создание чанков с сохранением структуры
# 4. Сохранение в папку external/
```

#### `scripts/chunk_splitter.py`

Утилита для автоматической разбивки больших файлов:

```python
"""
Разбивает большие файлы на чанки по 10 000 символов.
Использование:
  python scripts/chunk_splitter.py --file path/to/file.md
"""
# TODO: Реализовать
# 1. Чтение файла
# 2. Семантическая разбивка (по параграфам, не посередине предложения)
# 3. Создание связанных чанков (part 1/N, part 2/N...)
# 4. Обновление related_chunks в метаданных
```

#### `scripts/validate_chunks.py`

Валидация всех чанков в репозитории:

```python
"""
Проверяет корректность всех чанков.
Использование:
  python scripts/validate_chunks.py --dir club/
"""
# TODO: Реализовать
# 1. Проверка наличия всех обязательных метаданных
# 2. Проверка размера чанков (макс 10000 символов)
# 3. Проверка корректности связей (related_chunks)
# 4. Вывод отчета с ошибками
```

#### `scripts/sync_external.sh`

Синхронизация с внешними репозиториями:

```bash
#!/bin/bash
# Синхронизирует контент из внешних репозиториев
# Использование: ./scripts/sync_external.sh
```

### 5. GitHub Actions (автоматизация)

#### `.github/workflows/import-club.yml`

```yaml
name: Import from Club
on:
  schedule:
    - cron: '0 2 * * *'  # Каждый день в 2:00
  workflow_dispatch:      # Ручной запуск

jobs:
  import:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      - name: Install dependencies
        run: pip install -r scripts/requirements.txt
      - name: Import from Club
        env:
          CLUB_API_TOKEN: ${{ secrets.CLUB_API_TOKEN }}
        run: python scripts/import_from_club.py --from-date yesterday
      - name: Commit changes
        run: |
          git config user.name "GitHub Actions"
          git config user.email "actions@github.com"
          git add .
          git commit -m "Auto-import from Club" || echo "No changes"
          git push
```

#### `.github/workflows/import-lms.yml`

Аналогично для LMS.

#### `.github/workflows/sync-external.yml`

Для синхронизации с внешними репозиториями.

### 6. README.md

```markdown
# Персональный Репозиторий знаний

Хранилище персонального контента в виде чанков (до 10 000 символов).

## Структура

- `club/` — посты и комментарии из Клуба
- `lms/` — комментарии под ДЗ стажеров
- `manual/` — ручные добавления (заметки, рефлексии, проекты)
- `external/` — контент из других репозиториев
- `metadata/` — индексы и метаданные
- `scripts/` — утилиты для работы с репозиторием

## Использование

### Автоматический импорт

Импорт происходит автоматически каждый день через GitHub Actions.

### Ручной импорт

```bash
# Из Клуба
python scripts/import_from_club.py --from-date 2025-01-01

# Из LMS
python scripts/import_from_lms.py --student-id all

# Из других репо
python scripts/import_from_repo.py --repo ecosystem-development
```

### Ручное добавление

Создайте новый markdown файл в папке `manual/` с корректными метаданными.

### Валидация

```bash
python scripts/validate_chunks.py
```

## Формат чанка

См. `config/metadata-schema.yaml`

## Интеграция с Индексатором знаний

Этот репозиторий является источником данных для **Индексатора знаний (1.2)**, 
который создает эмбеддинги и сохраняет их в **Базу данных эмбеддингов (2.4)**.

## Редактирование

Все файлы можно редактировать вручную. После коммита изменения автоматически 
подхватываются Индексатором знаний.
```

## Задачи для Claude Code

1. **Создать структуру репозитория** согласно описанию выше
2. **Создать конфигурационные файлы** (`sources.yaml`, `metadata-schema.yaml`)
3. **Создать скелеты скриптов** с комментариями TODO
4. **Создать GitHub Actions workflows**
5. **Создать README.md** с инструкциями
6. **Создать примеры чанков** в каждой категории (club/posts, lms/homework-reviews, manual/notes)
7. **Создать .gitignore** для исключения временных файлов

## Дополнительные требования

- Все скрипты на Python 3.11+
- Использовать `pydantic` для валидации метаданных
- Использовать `pyyaml` для работы с конфигами
- Добавить `requirements.txt` с зависимостями
- Включить примеры использования в README

## Путь создания

Создать новый репозиторий по адресу:
`~/tserentserenov/Github/knowledge-repository/`

---

**Примечание**: Это базовая структура. После создания можно будет добавлять новые категории и функции по мере необходимости.
