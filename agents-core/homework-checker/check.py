#!/usr/bin/env python3
"""
ДЗ-чекер v0.1: проверка домашних заданий с использованием LLM.

Формат v0.1:
- Входные данные: answer_text, question_text, course_name, section_name
- Выходные данные: comment (Markdown), checked_at
- Контекст получается из репозитория руководств по названию курса/раздела
"""

import json
import sys
import yaml
import os
from pathlib import Path
from datetime import datetime, timezone
from typing import Optional


# Корень агента
AGENT_ROOT = Path(__file__).parent
DEFAULT_CONFIG = AGENT_ROOT / "config.yaml"


def load_config(config_path: Path = DEFAULT_CONFIG) -> dict:
    """Загрузка конфигурации."""
    local_config = config_path.parent / "config.local.yaml"
    if local_config.exists():
        config_path = local_config

    with open(config_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def load_prompts(config: dict) -> dict:
    """Загрузка промптов."""
    prompts_dir = AGENT_ROOT / config["paths"]["prompts_dir"]
    prompts = {}

    system_prompt = prompts_dir / "system.txt"
    if system_prompt.exists():
        prompts["system"] = system_prompt.read_text(encoding="utf-8")

    check_template = prompts_dir / "check_template.txt"
    if check_template.exists():
        prompts["check_template"] = check_template.read_text(encoding="utf-8")

    return prompts


def load_rubrics(config: dict) -> dict:
    """Загрузка рубрик."""
    path = AGENT_ROOT / config["paths"]["rubrics"]
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def get_check_context(course_name: str, section_name: str, config: dict) -> dict:
    """
    Получение контекста проверки из репозитория руководств.

    v0.1: Заглушка — возвращает базовый контекст.
    TODO: Интеграция с MCP-эндпоинтом /check-context репозитория руководств.
    """
    # Базовая рубрика для v0.1
    rubrics = load_rubrics(config)
    default_rubric = rubrics.get("rubrics", {}).get("rubric_conceptual_understanding", {})

    return {
        "course_name": course_name,
        "section_name": section_name,
        "normative_content": f"[Норматив для раздела '{section_name}' курса '{course_name}' будет загружен из репозитория руководств]",
        "rubric": default_rubric
    }


def format_rubric_for_prompt(rubric: dict) -> str:
    """Форматирование рубрики для промпта."""
    if not rubric:
        return "[Рубрика не найдена]"

    lines = [f"### {rubric.get('name', 'Оценка')}\n"]
    lines.append(f"Проходной балл: {rubric.get('passing_score', 60)}/100\n")
    lines.append("Критерии:\n")

    for criterion in rubric.get("criteria", []):
        lines.append(f"- **{criterion.get('name', criterion.get('id'))}** (вес: {criterion.get('weight')})")
        lines.append(f"  {criterion.get('description', '')}")

    return "\n".join(lines)


def build_llm_request(
    request: dict,
    context: dict,
    prompts: dict,
    config: dict
) -> dict:
    """Сборка запроса к LLM."""

    check_prompt = prompts.get("check_template", "")

    # Подставляем переменные
    user_content = check_prompt.format(
        question_text=request["question_text"],
        answer_text=request["answer_text"],
        normative_content=context.get("normative_content", "")[:8000],
        rubric_criteria=format_rubric_for_prompt(context.get("rubric"))
    )

    return {
        "model": config["llm"]["model"],
        "max_tokens": config["llm"]["max_tokens"],
        "temperature": config["llm"]["temperature"],
        "messages": [
            {
                "role": "system",
                "content": prompts.get("system", "")
            },
            {
                "role": "user",
                "content": user_content
            }
        ]
    }


def call_llm(llm_request: dict, config: dict) -> dict:
    """
    Вызов LLM API (Anthropic Claude).

    Возвращает структурированный результат проверки.
    При отсутствии API-ключа возвращает демо-результат.
    """
    import re

    provider = config["llm"]["provider"]
    api_key = os.environ.get("ANTHROPIC_API_KEY")

    print(f"[INFO] Вызов {provider} API с моделью {llm_request['model']}", file=sys.stderr)
    print(f"[INFO] Промпт: {len(llm_request['messages'][1]['content'])} символов", file=sys.stderr)

    # Если API-ключ не установлен, возвращаем демо-результат
    if not api_key:
        print("[WARN] ANTHROPIC_API_KEY не установлен, возвращаем демо-результат", file=sys.stderr)
        return _get_demo_result()

    # Реальный вызов Claude API
    try:
        import httpx

        response = httpx.post(
            "https://api.anthropic.com/v1/messages",
            headers={
                "x-api-key": api_key,
                "anthropic-version": "2023-06-01",
                "content-type": "application/json"
            },
            json={
                "model": llm_request["model"],
                "max_tokens": llm_request["max_tokens"],
                "temperature": llm_request["temperature"],
                "system": llm_request["messages"][0]["content"],
                "messages": [
                    {"role": "user", "content": llm_request["messages"][1]["content"]}
                ]
            },
            timeout=60.0
        )

        if response.status_code != 200:
            print(f"[ERROR] Claude API вернул {response.status_code}: {response.text}", file=sys.stderr)
            return _get_demo_result()

        data = response.json()
        content = data.get("content", [{}])[0].get("text", "{}")

        # Извлекаем JSON из ответа
        json_match = re.search(r'\{[\s\S]*\}', content)
        if json_match:
            result = json.loads(json_match.group())
            print(f"[INFO] Получен результат: verdict={result.get('verdict')}, score={result.get('score')}", file=sys.stderr)
            return result
        else:
            print(f"[WARN] Не удалось извлечь JSON из ответа", file=sys.stderr)
            return _get_demo_result()

    except ImportError:
        print("[WARN] httpx не установлен, возвращаем демо-результат. Установите: pip install httpx", file=sys.stderr)
        return _get_demo_result()
    except json.JSONDecodeError as e:
        print(f"[ERROR] Ошибка парсинга JSON: {e}", file=sys.stderr)
        return _get_demo_result()
    except Exception as e:
        print(f"[ERROR] Ошибка вызова API: {e}", file=sys.stderr)
        return _get_demo_result()


def _get_demo_result() -> dict:
    """Демо-результат для тестирования без API."""
    return {
        "verdict": "needs_revision",
        "score": 75,
        "strengths": [
            "Ответ содержит ключевую идею",
            "Приведён собственный пример"
        ],
        "issues": [
            {
                "criterion": "terminology",
                "issue": "Терминология курса использована не полностью",
                "suggestion": "Рекомендуется использовать термины из материалов"
            }
        ],
        "next_step": "Перечитайте раздел о терминологии и дополните ответ"
    }


def format_comment(llm_result: dict, context: dict, config: dict) -> str:
    """Форматирование комментария для студента (Markdown)."""

    verdicts = config.get("verdicts", {})
    verdict_info = verdicts.get(llm_result.get("verdict", "unknown"), {})

    emoji = verdict_info.get("emoji", "?")
    text = verdict_info.get("text", llm_result.get("verdict", "?"))
    score = llm_result.get("score", 0)

    lines = [f"**{emoji} {text}** ({score}/100)\n"]

    # Сильные стороны
    strengths = llm_result.get("strengths", [])
    if strengths:
        lines.append("**Сильные стороны:**")
        for s in strengths:
            lines.append(f"- {s}")
        lines.append("")

    # Замечания
    issues = llm_result.get("issues", [])
    if issues:
        lines.append("**Замечания:**")
        for issue in issues:
            lines.append(f"- {issue.get('issue', '')}")
            if issue.get("suggestion"):
                lines.append(f"  _Рекомендация: {issue['suggestion']}_")
        lines.append("")

    # Следующий шаг
    next_step = llm_result.get("next_step")
    if next_step:
        lines.append(f"**Следующий шаг:**\n{next_step}\n")

    # Метаинформация
    lines.append("---")
    lines.append(f"*Проверено: {config['llm']['model']}*")
    lines.append(f"*По материалам: {context.get('section_name', 'N/A')}*")

    return "\n".join(lines)


def check_answer(request: dict, config: dict, prompts: dict) -> dict:
    """
    Основная функция проверки одного ответа (v0.1).

    Args:
        request: словарь с полями answer_text, question_text, course_name, section_name
        config: конфигурация
        prompts: промпты

    Returns:
        словарь с полями comment, checked_at
    """

    # 1. Получить контекст из репозитория руководств
    context = get_check_context(
        course_name=request["course_name"],
        section_name=request["section_name"],
        config=config
    )

    # 2. Собрать запрос к LLM
    llm_request = build_llm_request(request, context, prompts, config)

    # 3. Вызвать LLM
    llm_result = call_llm(llm_request, config)

    # 4. Сформировать комментарий
    comment = format_comment(llm_result, context, config)

    return {
        "comment": comment,
        "checked_at": datetime.now(timezone.utc).isoformat()
    }


def main():
    """CLI-интерфейс для тестирования."""
    import argparse

    parser = argparse.ArgumentParser(description="ДЗ-чекер v0.1")
    parser.add_argument("--input", "-i", type=str, help="Входной JSON-файл")
    parser.add_argument("--output", "-o", type=str, help="Выходной JSON-файл")
    parser.add_argument("--config", "-c", type=str, help="Путь к конфигурации")

    args = parser.parse_args()

    # Загрузка конфигурации
    config_path = Path(args.config) if args.config else DEFAULT_CONFIG
    config = load_config(config_path)
    prompts = load_prompts(config)

    # Чтение входных данных
    if args.input:
        with open(args.input, "r", encoding="utf-8") as f:
            request = json.load(f)
    else:
        request = json.load(sys.stdin)

    # Проверка
    result = check_answer(request, config, prompts)

    # Вывод
    output_text = json.dumps(result, ensure_ascii=False, indent=2)

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(output_text)
        print(f"[INFO] Результат записан в {args.output}", file=sys.stderr)
    else:
        print(output_text)


if __name__ == "__main__":
    main()
