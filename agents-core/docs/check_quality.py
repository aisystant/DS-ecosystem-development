#!/usr/bin/env python3
"""
Docs Agent: Check Quality

Проверка качества документации по нескольким метрикам.

Использование:
    # Полная проверка всех документов
    python3 agents-core/docs/check_quality.py

    # Проверка конкретного файла
    python3 agents-core/docs/check_quality.py --path "content/4. Системы/4.12. Memory Bank.md"

    # Проверка с созданием отчета
    python3 agents-core/docs/check_quality.py --output "artifacts/docs/reviews/quality-report.md"

    # Проверка с fail при низком качестве (для CI)
    python3 agents-core/docs/check_quality.py --fail-below 60
"""

import argparse
import re
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Tuple

# Базовая директория проекта
BASE_DIR = Path(__file__).parent.parent.parent
CONTENT_DIR = BASE_DIR / "content"
ARTIFACTS_DIR = BASE_DIR / "artifacts" / "docs" / "reviews"

# Создаем директорию для отчетов если не существует
ARTIFACTS_DIR.mkdir(parents=True, exist_ok=True)


def check_frontmatter(file_path: Path) -> Dict:
    """Проверяет наличие и корректность frontmatter"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    issues = []
    score = 100

    # Проверка наличия frontmatter
    if not content.startswith('---'):
        issues.append("Отсутствует frontmatter")
        return {"score": 0, "issues": issues}

    # Извлекаем frontmatter
    parts = content.split('---', 2)
    if len(parts) < 3:
        issues.append("Некорректный формат frontmatter")
        return {"score": 0, "issues": issues}

    frontmatter = parts[1]

    # Обязательные поля
    required_fields = ["type", "audience", "edit_mode", "layer", "scope", "security"]
    for field in required_fields:
        if f"{field}:" not in frontmatter:
            issues.append(f"Отсутствует обязательное поле: {field}")
            score -= 15

    # Рекомендуемые поля
    recommended_fields = ["status", "version"]
    for field in recommended_fields:
        if f"{field}:" not in frontmatter:
            issues.append(f"Рекомендуется добавить поле: {field}")
            score -= 5

    return {"score": max(0, score), "issues": issues}


def check_links(file_path: Path, content_dir: Path) -> Dict:
    """Проверяет валидность wiki-ссылок"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    issues = []
    score = 100

    # Находим все wiki-ссылки
    wiki_links = re.findall(r'\[\[([^\]]+)\]\]', content)

    if not wiki_links:
        return {"score": 100, "issues": [], "total": 0, "broken": 0}

    broken_links = []

    for link in wiki_links:
        # Убираем секции (#...)
        link_file = link.split('#')[0].strip()

        # Ищем файл в content/
        found = False
        for file in content_dir.rglob("*.md"):
            if link_file in file.stem or link_file in str(file):
                found = True
                break

        if not found:
            broken_links.append(link)

    if broken_links:
        score = int(100 * (1 - len(broken_links) / len(wiki_links)))
        for link in broken_links[:5]:  # Показываем первые 5
            issues.append(f"Битая ссылка: [[{link}]]")

        if len(broken_links) > 5:
            issues.append(f"... и еще {len(broken_links) - 5} битых ссылок")

    return {
        "score": score,
        "issues": issues,
        "total": len(wiki_links),
        "broken": len(broken_links)
    }


def calculate_readability(text: str) -> int:
    """
    Упрощенный расчет читаемости (Flesch Reading Ease)

    90-100: Very Easy (5th grade)
    60-70: Standard (8th-9th grade) ← целевое значение
    0-30: Very Difficult (college graduate)
    """

    # Удаляем код блоки и frontmatter
    text = re.sub(r'```.*?```', '', text, flags=re.DOTALL)
    text = re.sub(r'---.*?---', '', text, flags=re.DOTALL)

    # Удаляем markdown разметку
    text = re.sub(r'[#*_`\[\]]', '', text)

    # Подсчитываем предложения (приблизительно)
    sentences = len(re.findall(r'[.!?]+', text))
    if sentences == 0:
        return 0

    # Подсчитываем слова
    words = len(re.findall(r'\b\w+\b', text))
    if words == 0:
        return 0

    # Упрощенная формула (без подсчета слогов)
    # Используем среднюю длину предложения как proxy
    avg_sentence_length = words / sentences

    # Эмпирическая формула для русского текста
    # Чем короче предложения, тем проще текст
    if avg_sentence_length < 15:
        score = 75  # Easy
    elif avg_sentence_length < 20:
        score = 65  # Standard
    elif avg_sentence_length < 25:
        score = 55  # Fairly Difficult
    else:
        score = 45  # Difficult

    return int(score)


def check_document_structure(file_path: Path) -> Dict:
    """Проверяет структуру документа (заголовки, разделы)"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    issues = []
    score = 100

    # Проверяем наличие H1 (должен быть один)
    h1_count = len(re.findall(r'^# [^#]', content, flags=re.MULTILINE))
    if h1_count == 0:
        issues.append("Отсутствует заголовок первого уровня (H1)")
        score -= 20
    elif h1_count > 1:
        issues.append(f"Несколько заголовков H1 ({h1_count}), должен быть один")
        score -= 10

    # Проверяем наличие H2 (основные разделы)
    h2_count = len(re.findall(r'^## [^#]', content, flags=re.MULTILINE))
    if h2_count == 0:
        issues.append("Отсутствуют разделы (H2)")
        score -= 15

    # Проверяем порядок заголовков (не должно быть H4 без H3)
    if '####' in content and '###' not in content:
        issues.append("Некорректная иерархия заголовков (H4 без H3)")
        score -= 10

    # Проверяем наличие краткого описания (первый абзац после H1)
    lines = content.split('\n')
    h1_index = None
    for i, line in enumerate(lines):
        if line.startswith('# ') and not line.startswith('## '):
            h1_index = i
            break

    if h1_index is not None:
        # Ищем первый непустой абзац после H1
        has_description = False
        for i in range(h1_index + 1, min(h1_index + 10, len(lines))):
            line = lines[i].strip()
            if line and not line.startswith('#') and not line.startswith('---'):
                has_description = True
                break

        if not has_description:
            issues.append("Рекомендуется добавить краткое описание после заголовка")
            score -= 5

    return {"score": max(0, score), "issues": issues}


def check_document(file_path: Path, content_dir: Path) -> Dict:
    """Комплексная проверка документа"""

    # Читаем содержимое для расчета читаемости
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Проверки
    frontmatter_check = check_frontmatter(file_path)
    links_check = check_links(file_path, content_dir)
    structure_check = check_document_structure(file_path)
    readability_score = calculate_readability(content)

    # Общий score (средневзвешенный)
    total_score = int(
        frontmatter_check["score"] * 0.3 +
        links_check["score"] * 0.2 +
        structure_check["score"] * 0.2 +
        readability_score * 0.3
    )

    # Определяем оценку
    if total_score >= 80:
        grade = "✅ Отлично"
        status = "excellent"
    elif total_score >= 60:
        grade = "🟡 Хорошо"
        status = "good"
    else:
        grade = "🔴 Нужны улучшения"
        status = "needs_improvement"

    return {
        "file": file_path,
        "score": total_score,
        "grade": grade,
        "status": status,
        "readability": readability_score,
        "checks": {
            "frontmatter": frontmatter_check,
            "links": links_check,
            "structure": structure_check
        }
    }


def generate_report(results: List[Dict], output_path: Path = None) -> str:
    """Генерирует отчет о проверке качества"""

    # Статистика
    total_docs = len(results)
    excellent = sum(1 for r in results if r["status"] == "excellent")
    good = sum(1 for r in results if r["status"] == "good")
    needs_improvement = sum(1 for r in results if r["status"] == "needs_improvement")

    avg_score = sum(r["score"] for r in results) / total_docs if total_docs > 0 else 0

    # Формируем отчет
    report = f"""# Отчет о качестве документации

**Дата проверки:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Сводка

📊 **Общая статистика:**
- Всего документов: **{total_docs}**
- Средний score: **{avg_score:.1f}**

**Распределение по оценкам:**
- ✅ Отлично (≥80): **{excellent}** ({excellent/total_docs*100:.0f}%)
- 🟡 Хорошо (60-79): **{good}** ({good/total_docs*100:.0f}%)
- 🔴 Нужны улучшения (<60): **{needs_improvement}** ({needs_improvement/total_docs*100:.0f}%)

## Детальные результаты

"""

    # Сортируем по score (худшие в начале)
    results_sorted = sorted(results, key=lambda x: x["score"])

    # Показываем документы требующие внимания
    report += "### 🔴 Документы требующие внимания\n\n"
    problem_docs = [r for r in results_sorted if r["status"] == "needs_improvement"]

    if problem_docs:
        for result in problem_docs:
            rel_path = result["file"].relative_to(BASE_DIR)
            report += f"#### {rel_path}\n\n"
            report += f"**Score:** {result['score']}/100 | **Readability:** {result['readability']}\n\n"
            report += "**Проблемы:**\n"

            # Frontmatter issues
            if result["checks"]["frontmatter"]["issues"]:
                for issue in result["checks"]["frontmatter"]["issues"]:
                    report += f"- ❌ {issue}\n"

            # Links issues
            if result["checks"]["links"]["issues"]:
                for issue in result["checks"]["links"]["issues"]:
                    report += f"- 🔗 {issue}\n"

            # Structure issues
            if result["checks"]["structure"]["issues"]:
                for issue in result["checks"]["structure"]["issues"]:
                    report += f"- 📝 {issue}\n"

            report += "\n"
    else:
        report += "Нет документов требующих немедленного внимания! ✅\n\n"

    # Показываем хорошие документы (топ 5)
    report += "### ✅ Лучшие документы (топ 5)\n\n"
    top_docs = sorted(results, key=lambda x: x["score"], reverse=True)[:5]

    for result in top_docs:
        rel_path = result["file"].relative_to(BASE_DIR)
        report += f"- **{rel_path}** — Score: {result['score']}/100\n"

    report += "\n---\n\n"
    report += "*Отчет сгенерирован Docs Agent*\n"

    # Сохраняем отчет если указан output path
    if output_path:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(report)
        print(f"📝 Детальный отчет: {output_path}")

    return report


def main():
    parser = argparse.ArgumentParser(
        description="Проверка качества документации"
    )

    parser.add_argument(
        "--path",
        type=Path,
        default=CONTENT_DIR,
        help="Путь к файлу или директории для проверки"
    )

    parser.add_argument(
        "--output",
        type=Path,
        help="Путь для сохранения отчета"
    )

    parser.add_argument(
        "--fail-below",
        type=int,
        help="Выйти с кодом 1 если средний score ниже указанного"
    )

    parser.add_argument(
        "--full-report",
        action="store_true",
        help="Показать полный отчет в консоли"
    )

    args = parser.parse_args()

    print("🔍 Проверка качества документации...\n")

    # Собираем список файлов для проверки
    if args.path.is_file():
        files = [args.path]
    else:
        files = list(args.path.rglob("*.md"))
        # Исключаем артефакты и служебные файлы
        files = [f for f in files if "artifacts" not in str(f) and ".obsidian" not in str(f)]

    if not files:
        print("❌ Не найдено файлов для проверки")
        sys.exit(1)

    print(f"📄 Найдено документов: {len(files)}\n")

    # Проверяем каждый документ
    results = []
    for file_path in files:
        try:
            result = check_document(file_path, CONTENT_DIR)
            results.append(result)
        except Exception as e:
            print(f"⚠️  Ошибка при проверке {file_path}: {e}")

    # Генерируем отчет
    if args.output:
        output_path = args.output
    else:
        output_path = ARTIFACTS_DIR / f"quality-report-{datetime.now().strftime('%Y-%m-%d')}.md"

    report = generate_report(results, output_path if args.full_report else None)

    # Выводим краткую сводку
    total_docs = len(results)
    excellent = sum(1 for r in results if r["status"] == "excellent")
    good = sum(1 for r in results if r["status"] == "good")
    needs_improvement = sum(1 for r in results if r["status"] == "needs_improvement")
    avg_score = sum(r["score"] for r in results) / total_docs if total_docs > 0 else 0

    print("📊 Результаты:")
    print("━" * 50)
    print(f"Всего документов: {total_docs}")
    print(f"✅ Отлично (≥80): {excellent} ({excellent/total_docs*100:.0f}%)")
    print(f"🟡 Хорошо (60-79): {good} ({good/total_docs*100:.0f}%)")
    print(f"🔴 Нужны улучшения (<60): {needs_improvement} ({needs_improvement/total_docs*100:.0f}%)")
    print()

    # Показываем проблемные документы
    if needs_improvement > 0:
        print("Проблемы:")
        print("━" * 50)
        problem_docs = sorted([r for r in results if r["status"] == "needs_improvement"],
                            key=lambda x: x["score"])
        for result in problem_docs[:5]:  # Топ 5 самых проблемных
            rel_path = result["file"].relative_to(BASE_DIR)
            print(f"🔴 {rel_path}")

            # Показываем первые 2 проблемы
            all_issues = (
                result["checks"]["frontmatter"]["issues"] +
                result["checks"]["links"]["issues"] +
                result["checks"]["structure"]["issues"]
            )
            for issue in all_issues[:2]:
                print(f"   - {issue}")

            if len(all_issues) > 2:
                print(f"   - ... и еще {len(all_issues) - 2} проблем(а)")
            print()

    if args.full_report or args.output:
        print(f"📝 Детальный отчет: {output_path}")

    # Проверяем пороговое значение
    if args.fail_below and avg_score < args.fail_below:
        print(f"\n❌ Средний score ({avg_score:.1f}) ниже порогового ({args.fail_below})")
        sys.exit(1)

    print("\n✅ Проверка завершена")


if __name__ == "__main__":
    main()
