#!/usr/bin/env python3
"""
Docs Agent: Create Document

Создание нового документа на основе шаблона с AI-генерацией структуры.

Использование:
    python3 agents-core/docs/create_document.py \
        --type system \
        --number 13 \
        --title "Система аналитики"

    python3 agents-core/docs/create_document.py \
        --template "content/templates/Agent-Template.md" \
        --output "artifacts/docs/drafts/new-agent.md" \
        --title "Agent: Analytics"
"""

import argparse
import os
import sys
from datetime import datetime
from pathlib import Path

# Базовая директория проекта
BASE_DIR = Path(__file__).parent.parent.parent
CONTENT_DIR = BASE_DIR / "content"
TEMPLATES_DIR = CONTENT_DIR / "templates"
ARTIFACTS_DIR = BASE_DIR / "artifacts" / "docs" / "drafts"

# Создаем директорию для артефактов если не существует
ARTIFACTS_DIR.mkdir(parents=True, exist_ok=True)


def load_template(template_path: Path) -> str:
    """Загружает шаблон из файла"""
    if not template_path.exists():
        raise FileNotFoundError(f"Шаблон не найден: {template_path}")

    with open(template_path, 'r', encoding='utf-8') as f:
        return f.read()


def generate_frontmatter(doc_type: str, layer: str, scope: str = "local-edge",
                         security: str = "internal") -> str:
    """Генерирует frontmatter метаданные для документа"""
    frontmatter = f"""---
type: {doc_type}
audience: mixed
edit_mode: manual
layer: {layer}
scope: {scope}
security: {security}
status: draft
version: 0.1
created: {datetime.now().strftime('%Y-%m-%d')}
---

"""
    return frontmatter


def create_system_document(number: int, title: str, output_path: Path) -> str:
    """Создает документ для новой системы"""

    # Генерируем содержимое на основе шаблона систем
    content = f"""# {number}. {title}

Краткое описание системы: что делает, зачем нужна, как взаимодействует с другими подсистемами.

## Назначение

Основная цель системы и решаемые задачи:
- Задача 1
- Задача 2
- Задача 3

## Архитектура

### Компоненты

1. **Компонент 1**
   - Описание
   - Ответственность

2. **Компонент 2**
   - Описание
   - Ответственность

### Технологический стек

- Backend: [указать технологии]
- Frontend: [указать технологии]
- База данных: [указать технологии]
- Инфраструктура: [указать технологии]

## Интеграции

### Входящие интеграции

Какие системы используют эту систему:
- [[4.X. Система Y]] — для чего использует

### Исходящие интеграции

Какие системы использует эта система:
- [[4.X. Система Y]] — для чего использует

## API и контракты

### Основные эндпоинты

```
GET /api/v1/resource
POST /api/v1/resource
PUT /api/v1/resource/:id
DELETE /api/v1/resource/:id
```

### События

Какие события генерирует система:
- `system.event.created` — когда происходит
- `system.event.updated` — когда происходит

## Хранилище данных

### Схема данных

Основные сущности и их поля:
- **Entity1**: field1, field2, field3
- **Entity2**: field1, field2, field3

### Retention policy

- Активные данные: [срок хранения]
- Архивные данные: [срок хранения]

## Метрики и мониторинг

### Ключевые метрики

| Метрика | Целевое значение | Текущее |
|---------|------------------|---------|
| Availability | 99.9% | — |
| Response time (p95) | <200ms | — |
| Error rate | <1% | — |

### Алерты

- Критические: [условия]
- Предупреждения: [условия]

## Roadmap

### v1.0 (MVP)
- [ ] Базовый функционал
- [ ] API endpoints
- [ ] Документация

### v1.1
- [ ] Улучшения производительности
- [ ] Расширенные интеграции

### v2.0
- [ ] Новые функции
- [ ] Масштабирование

## Связанные документы

- [[4.1. Список подсистем]] — реестр всех систем
- [[4.0. Информация]] — обзор раздела Системы
- [[0.7. Классификация документов и теги]] — метаданные

## История изменений

| Дата | Версия | Описание |
|------|--------|----------|
| {datetime.now().strftime('%Y-%m-%d')} | 0.1 | Первое создание документа |

---

**Status:** 🟡 Draft
**Owner:** [указать владельца]
**Last Updated:** {datetime.now().strftime('%Y-%m-%d')}
"""

    # Добавляем frontmatter
    frontmatter = generate_frontmatter("doc", "service")
    full_content = frontmatter + content

    return full_content


def create_document_from_template(template_path: Path, title: str,
                                   doc_type: str, layer: str) -> str:
    """Создает документ на основе шаблона"""

    # Загружаем шаблон
    template = load_template(template_path)

    # Заменяем плейсхолдеры
    content = template.replace("{{AgentName}}", title)
    content = content.replace("{{Описание роли агента и его миссия в экосистеме.}}",
                             "[Добавьте описание роли]")
    content = content.replace("{{Пути к данным или разделам content/}}",
                             "- [Укажите входные данные]")
    content = content.replace("{{Папки в artifacts/, куда агент пишет результаты}}",
                             "- [Укажите выходные артефакты]")
    content = content.replace("{{Используемые инструменты (SDK, MCP, Actions)}}",
                             "- [Укажите инструменты]")
    content = content.replace("{{YYYY-MM-DD}}", datetime.now().strftime('%Y-%m-%d'))

    # Добавляем frontmatter
    frontmatter = generate_frontmatter(doc_type, layer)
    full_content = frontmatter + content

    return full_content


def save_document(content: str, output_path: Path) -> None:
    """Сохраняет документ в файл"""

    # Создаем директорию если не существует
    output_path.parent.mkdir(parents=True, exist_ok=True)

    # Сохраняем файл
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"✅ Документ создан: {output_path}")


def analyze_existing_systems() -> list:
    """Анализирует существующие системы и возвращает список для рекомендаций"""
    systems_dir = CONTENT_DIR / "4. Системы"

    if not systems_dir.exists():
        return []

    # Получаем список всех .md файлов
    systems = []
    for file in systems_dir.glob("4.*.md"):
        systems.append(file.stem)

    return systems


def suggest_related_systems(new_system_number: int) -> list:
    """Предлагает связанные системы на основе эвристики"""

    # Простая эвристика: предлагаем системы близкие по номеру
    suggestions = []

    # Всегда предлагаем основные системы
    core_systems = [
        (1, "Список подсистем"),
        (2, "Операционная система ИИ-платформы"),
        (12, "Единое хранилище знаний (Memory Bank)")
    ]

    for num, name in core_systems:
        if num != new_system_number:
            suggestions.append(f"4.{num}. {name}")

    return suggestions


def main():
    parser = argparse.ArgumentParser(
        description="Создание нового документа с помощью Docs Agent"
    )

    # Основные аргументы
    parser.add_argument(
        "--type",
        choices=["system", "agent", "custom"],
        default="custom",
        help="Тип создаваемого документа"
    )

    parser.add_argument(
        "--number",
        type=int,
        help="Номер системы (для type=system)"
    )

    parser.add_argument(
        "--title",
        required=True,
        help="Название документа"
    )

    parser.add_argument(
        "--template",
        type=Path,
        help="Путь к шаблону (для type=custom)"
    )

    parser.add_argument(
        "--output",
        type=Path,
        help="Путь для сохранения документа"
    )

    parser.add_argument(
        "--layer",
        default="service",
        choices=["philosophy", "methodology", "ontology", "program", "requirements",
                "architecture", "service", "data", "analytics", "economy", "content"],
        help="Семантический слой документа"
    )

    parser.add_argument(
        "--doc-type",
        default="doc",
        choices=["doc", "data", "code", "model", "policy", "contract", "metric", "economy"],
        help="Тип артефакта"
    )

    args = parser.parse_args()

    # Определяем output path
    if args.output:
        output_path = args.output
    elif args.type == "system" and args.number:
        filename = f"4.{args.number}. {args.title}.md"
        output_path = ARTIFACTS_DIR / filename
    else:
        filename = f"{args.title.replace(' ', '-').lower()}.md"
        output_path = ARTIFACTS_DIR / filename

    # Генерируем содержимое в зависимости от типа
    if args.type == "system":
        if not args.number:
            print("❌ Ошибка: для type=system требуется --number")
            sys.exit(1)

        content = create_system_document(args.number, args.title, output_path)

    elif args.type == "custom" and args.template:
        content = create_document_from_template(
            args.template,
            args.title,
            args.doc_type,
            args.layer
        )

    else:
        # Простой документ с минимальной структурой
        frontmatter = generate_frontmatter(args.doc_type, args.layer)
        content = frontmatter + f"""# {args.title}

Краткое описание документа.

## Содержание

[Добавьте содержание]

## Связанные документы

- [[0.0. Информация]]

## История изменений

| Дата | Версия | Описание |
|------|--------|----------|
| {datetime.now().strftime('%Y-%m-%d')} | 0.1 | Первое создание документа |
"""

    # Сохраняем документ
    save_document(content, output_path)

    # Выводим дополнительную информацию
    print(f"📋 Frontmatter: type={args.doc_type}, layer={args.layer}")

    if args.type == "system":
        # Анализируем существующие системы
        related = suggest_related_systems(args.number)
        if related:
            print(f"🔗 Рекомендуется добавить связи с: {', '.join(related)}")

    print(f"📝 Следующий шаг: проверьте черновик и перенесите в content/ через PR")

    # Напоминание об обновлении списка подсистем
    if args.type == "system":
        print(f"⚠️  Не забудьте обновить: content/4. Системы/4.1. Список подсистем.md")


if __name__ == "__main__":
    main()
