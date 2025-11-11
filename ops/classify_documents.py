#!/usr/bin/env python3
"""
Скрипт автоматической классификации документов репозитория

Использование:
    python ops/classify_documents.py

Результат: обновляет документ "0.6. Структура этого хранилища.md"
с таблицей классификации всех документов
"""

import os
import re
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional
import json

# Базовая директория проекта
BASE_DIR = Path(__file__).parent.parent
CONTENT_DIR = BASE_DIR / "content"
STRUCTURE_DOC = CONTENT_DIR / "0. Управление" / "0.6. Структура этого хранилища.md"
CLASSIFICATION_DOC = CONTENT_DIR / "0. Управление" / "0.7. Классификация документов и теги.md"

# Файл для хранения ручных правок
MANUAL_EDITS_FILE = BASE_DIR / "ops" / "manual_classifications.json"

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


def load_env_file():
    """Загружает переменные окружения из .env файла"""
    env_file = BASE_DIR / '.env'
    if env_file.exists():
        with open(env_file, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    value = value.strip().strip('"').strip("'")
                    os.environ[key.strip()] = value
        print(f"✅ Загружен .env файл")


def load_manual_edits() -> Dict[str, Dict]:
    """Загружает ручные правки из JSON файла"""
    if MANUAL_EDITS_FILE.exists():
        with open(MANUAL_EDITS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}


def save_manual_edits(edits: Dict[str, Dict]):
    """Сохраняет ручные правки в JSON файл"""
    with open(MANUAL_EDITS_FILE, 'w', encoding='utf-8') as f:
        json.dump(edits, f, ensure_ascii=False, indent=2)


def collect_all_documents() -> List[Dict]:
    """Собирает список всех документов в репозитории"""
    documents = []

    for md_file in sorted(CONTENT_DIR.rglob("*.md")):
        # Пропускаем служебные файлы
        if ".obsidian" in str(md_file):
            continue
        if "0.5. Проверочный документ" in md_file.name:
            continue
        if "0.6. Структура этого хранилища" in md_file.name:
            continue

        relative_path = md_file.relative_to(CONTENT_DIR)

        documents.append({
            "name": md_file.name,
            "path": str(relative_path),
            "full_path": str(md_file),
            "folder": md_file.parent.name
        })

    return documents


def classify_document_with_ai(doc_path: str, doc_content: str) -> Dict[str, str]:
    """
    Классифицирует документ с помощью AI

    Returns:
        Dict с ключами: type, audience, edit_mode, layer, scope, security
    """
    try:
        from openai import OpenAI

        api_key = os.getenv('OPENAI_API_KEY')
        if not api_key:
            print("⚠️  OPENAI_API_KEY не установлен, используются значения по умолчанию")
            return get_default_classification(doc_path)

        client = OpenAI(api_key=api_key)

        # Ограничиваем размер контента
        max_chars = 3000
        if len(doc_content) > max_chars:
            doc_content = doc_content[:max_chars] + "..."

        prompt = f"""Проанализируй документ и классифицируй его по 4 осям согласно документу 0.7:

ДОКУМЕНТ: {doc_path}

СОДЕРЖИМОЕ:
{doc_content}

ОСИ КЛАССИФИКАЦИИ:

Ось A - Вид (type): doc, data, code, model, policy, contract, metric, economy
Ось B - Читаемость (audience): manual, mixed, machine
Ось B - Изменение (edit_mode): manual, mixed, machine
Ось C - Слой (layer): philosophy, methodology, ontology, program, conops, requirements, architecture, service, data, analytics, economy, content
Ось D - Область (scope): global-core, local-edge
Ось D - Безопасность (security): public, internal, restricted

Верни ТОЛЬКО JSON в формате:
{{
  "type": "...",
  "audience": "...",
  "edit_mode": "...",
  "layer": "...",
  "scope": "...",
  "security": "..."
}}

БЕЗ дополнительных пояснений, ТОЛЬКО JSON."""

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3,
            max_tokens=200
        )

        result_text = response.choices[0].message.content.strip()

        # Извлекаем JSON из ответа
        json_match = re.search(r'\{[^}]+\}', result_text, re.DOTALL)
        if json_match:
            classification = json.loads(json_match.group(0))

            # Валидируем значения
            for key, value in classification.items():
                if key in CLASSIFICATION_AXES and value not in CLASSIFICATION_AXES[key]:
                    print(f"⚠️  Некорректное значение {value} для оси {key}, используется по умолчанию")
                    classification[key] = CLASSIFICATION_AXES[key][0]

            return classification
        else:
            print(f"⚠️  Не удалось распарсить ответ AI для {doc_path}")
            return get_default_classification(doc_path)

    except Exception as e:
        print(f"⚠️  Ошибка AI-классификации для {doc_path}: {e}")
        return get_default_classification(doc_path)


def get_default_classification(doc_path: str) -> Dict[str, str]:
    """Возвращает классификацию по умолчанию на основе пути"""
    # Простая эвристика
    if "0. Управление" in doc_path:
        return {
            "type": "doc",
            "audience": "manual",
            "edit_mode": "manual",
            "layer": "methodology",
            "scope": "global-core",
            "security": "public"
        }
    elif "1. Идеи" in doc_path:
        return {
            "type": "doc",
            "audience": "manual",
            "edit_mode": "manual",
            "layer": "philosophy",
            "scope": "global-core",
            "security": "public"
        }
    elif "4. Системы" in doc_path:
        return {
            "type": "doc",
            "audience": "manual",
            "edit_mode": "manual",
            "layer": "architecture",
            "scope": "global-core",
            "security": "internal"
        }
    else:
        return {
            "type": "doc",
            "audience": "manual",
            "edit_mode": "manual",
            "layer": "content",
            "scope": "global-core",
            "security": "public"
        }


def generate_classification_table(documents: List[Dict], manual_edits: Dict) -> str:
    """
    Генерирует таблицу классификации документов

    ВАЖНО: Ручные правки НИКОГДА не перезаписываются AI!
    - AI-предложения: <mark>value</mark> (желтый фон)
    - Ручные правки: <span style="background-color: lightgreen">value</span> (зеленый фон)

    Если документ есть в manual_edits, AI НЕ запускается для него вообще.
    Только человек может изменить ручные правки.
    """
    table_lines = []

    # Заголовок таблицы
    table_lines.append("| № | Документ | Папка | Type | Audience | Edit Mode | Layer | Scope | Security |")
    table_lines.append("|---|----------|-------|------|----------|-----------|-------|-------|----------|")

    for idx, doc in enumerate(documents, 1):
        doc_path = doc['path']

        # КРИТИЧЕСКИ ВАЖНО: Проверяем наличие ручных правок ПЕРВЫМ делом
        # Если есть ручные правки - AI вообще не запускается!
        if doc_path in manual_edits:
            # ✅ РУЧНАЯ ПРАВКА - используем ее БЕЗ изменений
            classification = manual_edits[doc_path]
            is_manual = True
        else:
            # 🤖 AI-классификация (только если НЕТ ручных правок)
            try:
                with open(doc['full_path'], 'r', encoding='utf-8') as f:
                    content = f.read()
            except:
                content = ""

            classification = classify_document_with_ai(doc_path, content)
            is_manual = False

        # Форматируем значения:
        # - Ручные правки (человек) = ЗЕЛЕНЫЙ фон
        # - AI-предложения = ЖЕЛТЫЙ фон
        def format_value(value):
            if is_manual:
                # ✅ ЗЕЛЕНЫЙ = подтверждено человеком, AI НЕ ТРОГАЕТ
                return f'<span style="background-color: lightgreen">{value}</span>'
            else:
                # 🤖 ЖЕЛТЫЙ = предложение AI, человек может изменить
                return f'<mark>{value}</mark>'

        # Формируем строку таблицы
        row = (
            f"| {idx} | {doc['name']} | {doc['folder']} | "
            f"{format_value(classification['type'])} | "
            f"{format_value(classification['audience'])} | "
            f"{format_value(classification['edit_mode'])} | "
            f"{format_value(classification['layer'])} | "
            f"{format_value(classification['scope'])} | "
            f"{format_value(classification['security'])} |"
        )

        table_lines.append(row)

        # Задержка между API вызовами (если используется AI)
        if not is_manual and idx % 5 == 0:
            print(f"  Обработано {idx}/{len(documents)} документов...")

    return '\n'.join(table_lines)


def update_structure_document(table_content: str):
    """Обновляет документ 0.6 с новой таблицей классификации"""

    # Читаем текущий документ
    if STRUCTURE_DOC.exists():
        with open(STRUCTURE_DOC, 'r', encoding='utf-8') as f:
            current_content = f.read()
    else:
        current_content = ""

    # Формируем новый контент
    new_content = f"""Этот документ объясняет правила структуры папок, именования, связей, версионирования и роли Obsidian↔Git; описывает «как здесь работают документы» и содержит полную таблицу классификации всех документов репозитория.

> Автоматически обновлено: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

---

## Таблица классификации документов

**Легенда:**
- <mark>Желтый фон</mark> - предложение AI (можно править вручную)
- Обычный текст - ручная правка человека

**Оси классификации** (из документа 0.7):
- **Type**: вид артефакта (doc, data, code, model, policy, contract, metric, economy)
- **Audience**: читаемость (manual, mixed, machine)
- **Edit Mode**: кто может изменять (manual, mixed, machine)
- **Layer**: семантический слой (philosophy, methodology, ontology, program, conops, requirements, architecture, service, data, analytics, economy, content)
- **Scope**: область (global-core, local-edge)
- **Security**: уровень доступа (public, internal, restricted)

{table_content}

**Итого документов:** {table_content.count('|') // 9 - 2}

---

## Как работать с классификацией

1. **Автоматическая классификация**: запустите `python ops/classify_documents.py`
2. **Ручная правка**: измените значения в таблице напрямую, уберите тег `<mark>`
3. **Новые документы**: автоматически появятся при следующем запуске скрипта
4. **Изменения в 0.7**: при изменении списка тегов скрипт предложит обновления

---

## Шаблон frontmatter для новых документов

```yaml
type: doc                 # из Оси A
audience: manual          # из Оси B
edit_mode: manual         # из Оси B
layer: methodology        # из Оси C
scope: global-core        # из Оси D
security: public          # из Оси D
status: draft             # draft, in_progress, approved, published, archived
```

"""

    # Сохраняем обновленный документ
    with open(STRUCTURE_DOC, 'w', encoding='utf-8') as f:
        f.write(new_content)

    print(f"✅ Документ обновлен: {STRUCTURE_DOC}")


def main():
    """Главная функция"""
    print("🚀 Запуск автоматической классификации документов...")
    print()

    # Загружаем .env
    load_env_file()

    # Загружаем ручные правки
    manual_edits = load_manual_edits()
    print(f"📝 Загружено ручных правок: {len(manual_edits)}")

    # Собираем все документы
    documents = collect_all_documents()
    print(f"📚 Найдено документов: {len(documents)}")
    print()

    # Генерируем таблицу
    print("🤖 Классификация документов с помощью AI...")
    table_content = generate_classification_table(documents, manual_edits)

    # Обновляем документ 0.6
    update_structure_document(table_content)

    print()
    print("✅ Классификация завершена!")
    print(f"📍 Результат: {STRUCTURE_DOC}")
    print()
    print("💡 Для ручной правки:")
    print("   1. Откройте документ 0.6 в Obsidian")
    print("   2. Измените значения в таблице")
    print("   3. Уберите теги <mark>...</mark> для подтверждения правки")
    print("   4. Сохраните файл")


if __name__ == "__main__":
    main()
