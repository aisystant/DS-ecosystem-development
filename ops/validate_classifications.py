#!/usr/bin/env python3
"""
Скрипт валидации классификации документов

Проверяет, что все значения в таблице классификации (документ 0.6)
соответствуют допустимым значениям из документа 0.7.

Использование:
    python ops/validate_classifications.py

Exit codes:
    0 - все значения валидны
    1 - найдены невалидные значения
"""

import re
import sys
from pathlib import Path
from typing import Dict, List, Set

# Базовая директория проекта
BASE_DIR = Path(__file__).parent.parent
CONTENT_DIR = BASE_DIR / "content"
STRUCTURE_DOC = CONTENT_DIR / "0. Управление" / "0.6. Структура этого хранилища.md"

# Определения осей классификации из документа 0.7
CLASSIFICATION_AXES = {
    "type": ["doc", "data", "code", "model", "policy", "contract", "metric", "economy"],
    "audience": ["manual", "mixed", "machine"],
    "edit_mode": ["manual", "mixed", "machine"],
    "layer": ["philosophy", "methodology", "ontology", "program", "conops",
              "requirements", "architecture", "service", "data", "analytics",
              "economy", "content"],
    "scope": ["global-core", "local-edge"],
    "security": ["public", "internal", "restricted"]
}


def extract_value_from_cell(cell: str) -> str:
    """
    Извлекает значение из ячейки таблицы, убирая любые HTML теги

    Поддерживаемые форматы:
    - <mark>value</mark> - желтый (AI-предложение)
    - <span style="background-color: lightgreen">value</span> - зеленый (ручная правка)
    - value - обычный текст

    Args:
        cell: содержимое ячейки

    Returns:
        Чистое значение без тегов
    """
    cell = cell.strip()

    # Убираем желтый <mark> тег
    mark_pattern = r'<mark>(.*?)</mark>'
    match = re.search(mark_pattern, cell)
    if match:
        return match.group(1).strip()

    # Убираем зеленый <span> тег
    green_pattern = r'<span style="background-color: lightgreen">(.*?)</span>'
    match = re.search(green_pattern, cell)
    if match:
        return match.group(1).strip()

    # Убираем любые другие HTML теги
    tag_pattern = r'<[^>]+>(.*?)</[^>]+>'
    match = re.search(tag_pattern, cell)
    if match:
        return match.group(1).strip()

    return cell


def validate_classification_table() -> tuple[bool, List[str]]:
    """
    Валидирует таблицу классификации в документе 0.6

    Returns:
        Tuple (is_valid, errors_list)
    """
    if not STRUCTURE_DOC.exists():
        return False, [f"❌ Документ не найден: {STRUCTURE_DOC}"]

    with open(STRUCTURE_DOC, 'r', encoding='utf-8') as f:
        content = f.read()

    errors = []

    # Находим таблицу классификации
    # Ищем строки с данными (начинаются с | и содержат номер)
    lines = content.split('\n')

    table_rows = []
    in_table = False

    for line in lines:
        # Начало таблицы
        if '| №' in line and '| Документ' in line and '| Type' in line:
            in_table = True
            continue

        # Разделитель таблицы (пропускаем)
        if in_table and line.strip().startswith('|') and '---' in line:
            continue

        # Конец таблицы
        if in_table and (line.startswith('**Итого') or line.startswith('---') or not line.strip()):
            if line.startswith('**Итого') or line.startswith('---'):
                break
            continue

        # Строки с данными
        if in_table and line.strip().startswith('|'):
            table_rows.append(line)

    if not table_rows:
        return False, ["❌ Таблица классификации не найдена в документе 0.6"]

    # Парсим строки таблицы
    # Формат: | № | Документ | Папка | Type | Audience | Edit Mode | Layer | Scope | Security |
    row_pattern = r'\|\s*(\d+)\s*\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|'

    for row in table_rows:
        match = re.match(row_pattern, row)
        if not match:
            continue

        row_num = match.group(1)
        doc_name = match.group(2).strip()
        folder = match.group(3).strip()

        # Извлекаем значения классификации
        values = {
            "type": extract_value_from_cell(match.group(4)),
            "audience": extract_value_from_cell(match.group(5)),
            "edit_mode": extract_value_from_cell(match.group(6)),
            "layer": extract_value_from_cell(match.group(7)),
            "scope": extract_value_from_cell(match.group(8)),
            "security": extract_value_from_cell(match.group(9))
        }

        # Валидируем каждое значение
        for axis, value in values.items():
            if value not in CLASSIFICATION_AXES[axis]:
                errors.append(
                    f"❌ Строка {row_num} ({doc_name}): "
                    f"невалидное значение '{value}' для оси '{axis}'. "
                    f"Допустимые значения: {', '.join(CLASSIFICATION_AXES[axis])}"
                )

    is_valid = len(errors) == 0
    return is_valid, errors


def print_allowed_values():
    """Выводит список допустимых значений для каждой оси"""
    print("\n📋 Допустимые значения классификации (из документа 0.7):\n")

    axis_names = {
        "type": "Type (Вид артефакта)",
        "audience": "Audience (Читаемость)",
        "edit_mode": "Edit Mode (Кто может изменять)",
        "layer": "Layer (Семантический слой)",
        "scope": "Scope (Область)",
        "security": "Security (Уровень доступа)"
    }

    for axis, name in axis_names.items():
        values = ", ".join(CLASSIFICATION_AXES[axis])
        print(f"  • {name}:")
        print(f"    {values}\n")


def main():
    """Главная функция"""
    print("🔍 Валидация классификации документов...\n")

    is_valid, errors = validate_classification_table()

    if is_valid:
        print("✅ Все значения классификации валидны!")
        print(f"📍 Проверен документ: {STRUCTURE_DOC}")
        print_allowed_values()
        return 0
    else:
        print("❌ Найдены ошибки валидации:\n")
        for error in errors:
            print(f"  {error}")

        print_allowed_values()

        print("💡 Для исправления:")
        print("  1. Откройте документ 0.6 в Obsidian")
        print("  2. Исправьте невалидные значения на допустимые")
        print("  3. Запустите валидацию снова: python ops/validate_classifications.py")

        return 1


if __name__ == "__main__":
    sys.exit(main())
