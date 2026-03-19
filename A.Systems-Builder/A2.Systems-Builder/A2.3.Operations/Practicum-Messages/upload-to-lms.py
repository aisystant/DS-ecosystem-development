#!/usr/bin/env python3
"""
Загрузка сообщений практикумов из markdown-источников в LMS Aisystant.

Источники:
  - ss-messages.md  →  Практикум «Системное саморазвитие»
  - ms-messages.md  →  Практикум «Методы саморазвития»

API: POST /api/crm/group-messages-template

Использование:
  python3 upload-to-lms.py                    # загрузить оба практикума
  python3 upload-to-lms.py --dry-run          # только показать, не загружать
  python3 upload-to-lms.py --list             # показать текущие шаблоны в LMS
  python3 upload-to-lms.py --file ss-messages.md  # загрузить один файл

Переменные окружения:
  AISYSTANT_SESSION_TOKEN  — session-token для авторизации (обязательно)
"""

import argparse
import os
import re
import sys
import yaml

try:
    import requests
except ImportError:
    print("pip install requests")
    sys.exit(1)

BASE_URL = "https://aisystant.system-school.ru/api/crm/group-messages-template"
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))


def get_session_token():
    token = os.environ.get("AISYSTANT_SESSION_TOKEN")
    if not token:
        print("Ошибка: установите AISYSTANT_SESSION_TOKEN")
        print("  export AISYSTANT_SESSION_TOKEN='your-token-here'")
        sys.exit(1)
    return token


def get_headers(token):
    return {
        "accept": "application/json",
        "content-type": "application/json",
        "cookie": f"session-token={token}"
    }


def parse_messages_file(filepath):
    """Парсит markdown-файл с сообщениями. Возвращает (frontmatter, messages)."""
    with open(filepath, 'r') as f:
        content = f.read()

    # Извлекаем frontmatter
    fm_match = re.match(r'^---\n(.*?)\n---', content, re.DOTALL)
    if not fm_match:
        print(f"Ошибка: нет frontmatter в {filepath}")
        sys.exit(1)

    frontmatter = yaml.safe_load(fm_match.group(1))
    body = content[fm_match.end():]

    # Парсим сообщения по разделителю "## День N |"
    messages = []
    parts = re.split(r'---\s*\n\n## День (-?\d+) \|', body)

    # parts[0] — текст до первого сообщения (заголовок)
    # parts[1], parts[2] — день, текст; parts[3], parts[4] — день, текст; ...
    for i in range(1, len(parts), 2):
        day = int(parts[i])
        # Текст: убираем заголовок строки (после " | ...")
        raw_text = parts[i + 1] if i + 1 < len(parts) else ""
        # Убираем первую строку (она содержит "Неделя X — ...")
        lines = raw_text.split('\n', 1)
        text = lines[1].strip() if len(lines) > 1 else lines[0].strip()

        if text:
            messages.append({
                "day": day,
                "message": text,
                "parseMode": frontmatter.get("parse_mode", "markdown"),
                "time": frontmatter.get("send_time", "10:00") + ":00"
            })

    return frontmatter, messages


def list_templates(headers):
    """Показать текущие шаблоны в LMS."""
    resp = requests.get(BASE_URL, headers=headers)
    if resp.status_code != 200:
        print(f"Ошибка: {resp.status_code}")
        return

    templates = resp.json()
    print(f"Шаблоны в LMS ({len(templates)}):\n")
    for t in templates:
        msgs = t.get("groupMessageTemplates", [])
        print(f"  id={t['id']:>3}  msgs={len(msgs):>2}  {t['name']}")
    print()


def upload_template(name, messages, headers, dry_run=False):
    """Загрузить шаблон с сообщениями в LMS."""
    payload = {
        "name": name,
        "groupMessageTemplates": [
            {
                "message": m["message"],
                "parseMode": m["parseMode"],
                "day": m["day"],
                "time": m["time"]
            }
            for m in messages
        ]
    }

    if dry_run:
        print(f"[DRY RUN] '{name}' — {len(messages)} сообщений:")
        for m in sorted(messages, key=lambda x: x["day"]):
            preview = m["message"][:60].replace('\n', ' ')
            print(f"  день {m['day']:>3}, {m['time']} — {preview}...")
        return

    resp = requests.post(BASE_URL, headers=headers, json=payload)
    if resp.status_code == 200:
        data = resp.json()
        print(f"✅ '{name}' (id={data['id']}) — {len(data['groupMessageTemplates'])} сообщений загружено")
    else:
        print(f"❌ Ошибка '{name}': {resp.status_code}")
        print(resp.text[:300])


def main():
    parser = argparse.ArgumentParser(description="Загрузка сообщений практикумов в LMS")
    parser.add_argument("--dry-run", action="store_true", help="Только показать, не загружать")
    parser.add_argument("--list", action="store_true", help="Показать текущие шаблоны в LMS")
    parser.add_argument("--file", type=str, help="Загрузить один конкретный файл")
    args = parser.parse_args()

    token = get_session_token()
    headers = get_headers(token)

    if args.list:
        list_templates(headers)
        return

    # Определяем файлы для загрузки
    if args.file:
        files = [os.path.join(SCRIPT_DIR, args.file) if not os.path.isabs(args.file) else args.file]
    else:
        files = [
            os.path.join(SCRIPT_DIR, "ss-messages.md"),
            os.path.join(SCRIPT_DIR, "ms-messages.md"),
        ]

    for filepath in files:
        if not os.path.exists(filepath):
            print(f"Файл не найден: {filepath}")
            continue

        frontmatter, messages = parse_messages_file(filepath)
        name = frontmatter.get("practicum", os.path.basename(filepath))

        print(f"\n{'[DRY RUN] ' if args.dry_run else ''}Файл: {os.path.basename(filepath)}")
        print(f"  Практикум: {name}")
        print(f"  Сообщений: {len(messages)}")

        upload_template(name, messages, headers, dry_run=args.dry_run)

    if not args.dry_run:
        print("\n⚠️  Создаются НОВЫЕ шаблоны. Старые удалите через интерфейс LMS.")


if __name__ == "__main__":
    main()
