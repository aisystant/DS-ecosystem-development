#!/usr/bin/env python3
"""
Скрипт для переработки документов по единому шаблону.
Добавляет frontmatter и структуру к документам разделов 1-3.
"""

import os
import re
from pathlib import Path
from datetime import date

CONTENT_DIR = Path("/home/user/ecosystem-development/content")

SECTIONS = [
    "1. Мир (Надсистема)",
    "2. Созидатель (Целевая система)",
    "3. Экосистема развития (Система создания)"
]

# Описания для разделов (для генерации назначения)
SECTION_DESCRIPTIONS = {
    "1.1": "продвижение экосистемы",
    "1.2": "концепцию использования созидателя",
    "1.3": "репутацию и партнёрства",
    "2.1": "видение и ценность созидателя",
    "2.2": "модель и компетенции созидателя",
    "2.3": "путь и сопровождение созидателя",
    "3.1": "экономику и инвестиции экосистемы",
    "3.2": "платформу и подсистемы",
    "3.3": "команду и службы экосистемы",
}

def get_layer(filepath: str) -> str:
    """Определяет layer по пути файла."""
    if ".1." in filepath or "/1.1" in filepath or "/2.1" in filepath or "/3.1" in filepath:
        return "methodology"
    elif ".2." in filepath or "/1.2" in filepath or "/2.2" in filepath or "/3.2" in filepath:
        return "architecture"
    elif ".3." in filepath or "/1.3" in filepath or "/2.3" in filepath or "/3.3" in filepath:
        return "operations"
    return "methodology"

def get_section_code(filepath: str) -> str:
    """Извлекает код раздела из пути (например, 1.1, 2.3)."""
    match = re.search(r'/([123])\.([123])', filepath)
    if match:
        return f"{match.group(1)}.{match.group(2)}"
    return ""

def get_title_from_filename(filename: str) -> str:
    """Извлекает название из имени файла."""
    # Убираем .md и код раздела в конце
    name = filename.replace(".md", "")
    # Убираем код типа " 1.1", " 2.3" в конце
    name = re.sub(r'\s+\d+\.\d+$', '', name)
    return name

def get_parent_doc(filepath: str) -> str:
    """Определяет родительский документ для связей."""
    section_match = re.search(r'/([123])\. ', filepath)
    if section_match:
        section_num = section_match.group(1)
        return f"О разделе {section_num}.0"
    return "О разделе 0.0"

def has_valid_frontmatter(content: str) -> bool:
    """Проверяет наличие валидного frontmatter."""
    return content.strip().startswith("---") and "---" in content[4:]

def process_document(filepath: Path) -> bool:
    """Обрабатывает один документ."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"Error reading {filepath}: {e}")
        return False

    # Пропускаем документы с валидным frontmatter
    if has_valid_frontmatter(content):
        print(f"SKIP (has frontmatter): {filepath.name}")
        return False

    filename = filepath.name
    title = get_title_from_filename(filename)
    layer = get_layer(str(filepath))
    section_code = get_section_code(str(filepath))
    parent_doc = get_parent_doc(str(filepath))

    # Получаем описание раздела для назначения
    section_desc = SECTION_DESCRIPTIONS.get(section_code, "экосистему")

    # Очищаем существующий контент
    existing_content = content.strip()

    # Убираем старый заголовок если есть
    if existing_content.startswith("#"):
        lines = existing_content.split("\n")
        # Пропускаем первую строку с заголовком
        existing_content = "\n".join(lines[1:]).strip()

    # Убираем TODO если это единственный контент
    if existing_content == "> TODO: Документ в разработке":
        existing_content = ""

    # Формируем новый документ
    today = date.today().isoformat()

    new_content = f"""---
type: doc
status: stub
created: {today}
layer: {layer}
scope: local-edge
---

# {title}

## 0. Назначение документа

Этот документ описывает {title.lower()} в контексте раздела, посвящённого {section_desc}.

---

## 1. Содержание

{existing_content if existing_content else "> TODO: Документ в разработке"}

---

## 2. Связанные документы

- [[{parent_doc}]]
"""

    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"OK: {filepath.name}")
        return True
    except Exception as e:
        print(f"Error writing {filepath}: {e}")
        return False

def main():
    processed = 0
    skipped = 0
    errors = 0

    for section in SECTIONS:
        section_path = CONTENT_DIR / section
        if not section_path.exists():
            print(f"Section not found: {section_path}")
            continue

        for filepath in section_path.rglob("*.md"):
            # Пропускаем "О разделе" документы - они уже правильно оформлены
            if "О разделе" in filepath.name:
                print(f"SKIP (О разделе): {filepath.name}")
                skipped += 1
                continue

            result = process_document(filepath)
            if result:
                processed += 1
            elif result is False:
                skipped += 1
            else:
                errors += 1

    print(f"\n=== ИТОГО ===")
    print(f"Обработано: {processed}")
    print(f"Пропущено: {skipped}")
    print(f"Ошибок: {errors}")

if __name__ == "__main__":
    main()
