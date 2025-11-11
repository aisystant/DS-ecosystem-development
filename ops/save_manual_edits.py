#!/usr/bin/env python3
"""
Скрипт для сохранения ручных правок из таблицы в JSON

ВАЖНО: Этот скрипт извлекает значения БЕЗ тегов <mark> (желтый)
и сохраняет их как ручные правки с зеленым фоном.

Использование:
    python ops/save_manual_edits.py

Как это работает:
1. Читает таблицу из документа 0.6
2. Находит строки БЕЗ тегов <mark> или с зелеными тегами
3. Сохраняет их в ops/manual_classifications.json
4. При следующем запуске classify_documents.py эти значения будут:
   - Отображаться ЗЕЛЕНЫМ
   - НИКОГДА не изменяться AI
   - Изменяться только человеком вручную
"""

import re
import json
from pathlib import Path
from typing import Dict, List

# Базовая директория проекта
BASE_DIR = Path(__file__).parent.parent
CONTENT_DIR = BASE_DIR / "content"
STRUCTURE_DOC = CONTENT_DIR / "0. Управление" / "0.6. Структура этого хранилища.md"
MANUAL_EDITS_FILE = BASE_DIR / "ops" / "manual_classifications.json"


def extract_value_from_cell(cell: str) -> tuple[str, bool]:
    """
    Извлекает значение из ячейки и определяет, является ли оно ручной правкой

    Args:
        cell: содержимое ячейки

    Returns:
        Tuple (значение, is_manual)
        - is_manual=True если это зеленый тег или обычный текст (БЕЗ <mark>)
        - is_manual=False если это желтый <mark> (AI-предложение)
    """
    cell = cell.strip()

    # Проверяем, есть ли желтый <mark> тег (AI-предложение)
    if '<mark>' in cell:
        # Это AI-предложение, НЕ сохраняем
        mark_pattern = r'<mark>(.*?)</mark>'
        match = re.search(mark_pattern, cell)
        if match:
            return match.group(1).strip(), False
        return cell, False

    # Проверяем, есть ли зеленый тег (ручная правка)
    green_pattern = r'<span style="background-color: lightgreen">(.*?)</span>'
    match = re.search(green_pattern, cell)
    if match:
        return match.group(1).strip(), True

    # Обычный текст без тегов - это тоже ручная правка
    return cell, True


def save_manual_edits_from_table():
    """
    Извлекает ручные правки из таблицы и сохраняет в JSON

    ВАЖНО: Сохраняются только значения БЕЗ <mark> тегов!
    """
    if not STRUCTURE_DOC.exists():
        print(f"❌ Документ не найден: {STRUCTURE_DOC}")
        return

    with open(STRUCTURE_DOC, 'r', encoding='utf-8') as f:
        content = f.read()

    # Находим таблицу классификации
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
        print("❌ Таблица классификации не найдена в документе 0.6")
        return

    # Парсим строки таблицы
    row_pattern = r'\|\s*(\d+)\s*\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|'

    manual_edits = {}
    manual_count = 0
    ai_count = 0

    for row in table_rows:
        match = re.match(row_pattern, row)
        if not match:
            continue

        row_num = match.group(1)
        doc_name = match.group(2).strip()
        folder = match.group(3).strip()

        # Извлекаем значения и проверяем, являются ли они ручными правками
        type_val, type_manual = extract_value_from_cell(match.group(4))
        audience_val, audience_manual = extract_value_from_cell(match.group(5))
        edit_mode_val, edit_mode_manual = extract_value_from_cell(match.group(6))
        layer_val, layer_manual = extract_value_from_cell(match.group(7))
        scope_val, scope_manual = extract_value_from_cell(match.group(8))
        security_val, security_manual = extract_value_from_cell(match.group(9))

        # Если ВСЕ значения - ручные правки, сохраняем строку целиком
        if all([type_manual, audience_manual, edit_mode_manual,
                layer_manual, scope_manual, security_manual]):

            # Определяем путь к документу (относительный от content/)
            doc_path = f"{folder}/{doc_name}"

            manual_edits[doc_path] = {
                "type": type_val,
                "audience": audience_val,
                "edit_mode": edit_mode_val,
                "layer": layer_val,
                "scope": scope_val,
                "security": security_val
            }

            manual_count += 1
            print(f"✅ Сохранена ручная правка: {doc_name}")
        else:
            ai_count += 1

    # Сохраняем в JSON
    with open(MANUAL_EDITS_FILE, 'w', encoding='utf-8') as f:
        json.dump(manual_edits, f, ensure_ascii=False, indent=2)

    print()
    print(f"📊 Статистика:")
    print(f"  ✅ Ручных правок (зеленые): {manual_count}")
    print(f"  🤖 AI-предложений (желтые): {ai_count}")
    print()
    print(f"💾 Ручные правки сохранены в: {MANUAL_EDITS_FILE}")
    print()
    print("🔒 Защита данных:")
    print("  • Зеленые значения НИКОГДА не будут изменены AI")
    print("  • Только человек может изменить зеленые значения")
    print("  • При запуске classify_documents.py зеленые останутся зелеными")


def main():
    """Главная функция"""
    print("💾 Сохранение ручных правок из таблицы...\n")
    save_manual_edits_from_table()


if __name__ == "__main__":
    main()
