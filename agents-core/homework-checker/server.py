#!/usr/bin/env python3
"""
HTTP-сервер ДЗ-чекера v0.1.

Синхронный endpoint для приёма запросов от LMS.

Использование:
    python3 server.py --port 8080
"""

import argparse
import json
import sys
from http.server import HTTPServer, BaseHTTPRequestHandler
from pathlib import Path

# Импортируем функции из check.py
from check import check_answer, load_config, load_prompts

AGENT_ROOT = Path(__file__).parent
DEFAULT_CONFIG = AGENT_ROOT / "config.yaml"


class CheckHandler(BaseHTTPRequestHandler):
    """HTTP-обработчик запросов на проверку."""

    # Загружаем конфигурацию и промпты один раз
    config = None
    prompts = None

    @classmethod
    def initialize(cls, config_path: Path = DEFAULT_CONFIG):
        """Инициализация конфигурации."""
        cls.config = load_config(config_path)
        cls.prompts = load_prompts(cls.config)
        print(f"[INFO] Конфигурация загружена из {config_path}", file=sys.stderr)

    def do_POST(self):
        """Обработка POST-запроса на /check."""
        if self.path != "/check":
            self.send_error(404, "Not Found")
            return

        # Читаем тело запроса
        content_length = int(self.headers.get("Content-Length", 0))
        if content_length == 0:
            self.send_error(400, "Empty request body")
            return

        try:
            body = self.rfile.read(content_length)
            request = json.loads(body.decode("utf-8"))
        except json.JSONDecodeError as e:
            self.send_error(400, f"Invalid JSON: {e}")
            return

        # Валидация обязательных полей
        required_fields = ["answer_text", "question_text", "course_name", "section_name"]
        missing = [f for f in required_fields if f not in request]
        if missing:
            self.send_error(400, f"Missing required fields: {missing}")
            return

        # Проверка
        try:
            result = check_answer(request, self.config, self.prompts)
        except Exception as e:
            print(f"[ERROR] Ошибка проверки: {e}", file=sys.stderr)
            self.send_error(500, f"Internal error: {e}")
            return

        # Отправляем ответ
        response_body = json.dumps(result, ensure_ascii=False).encode("utf-8")

        self.send_response(200)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", len(response_body))
        self.end_headers()
        self.wfile.write(response_body)

    def do_GET(self):
        """Обработка GET-запроса (health check)."""
        if self.path == "/health":
            response = {"status": "ok", "version": "0.1"}
            response_body = json.dumps(response).encode("utf-8")

            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", len(response_body))
            self.end_headers()
            self.wfile.write(response_body)
        else:
            self.send_error(404, "Not Found")

    def log_message(self, format, *args):
        """Переопределяем логирование."""
        print(f"[HTTP] {self.address_string()} - {format % args}", file=sys.stderr)


def main():
    parser = argparse.ArgumentParser(description="HTTP-сервер ДЗ-чекера v0.1")
    parser.add_argument("--port", "-p", type=int, default=8080, help="Порт сервера")
    parser.add_argument("--host", type=str, default="0.0.0.0", help="Хост сервера")
    parser.add_argument("--config", "-c", type=str, help="Путь к конфигурации")

    args = parser.parse_args()

    # Инициализация
    config_path = Path(args.config) if args.config else DEFAULT_CONFIG
    CheckHandler.initialize(config_path)

    # Запуск сервера
    server = HTTPServer((args.host, args.port), CheckHandler)
    print(f"[INFO] ДЗ-чекер v0.1 запущен на http://{args.host}:{args.port}", file=sys.stderr)
    print(f"[INFO] Endpoint: POST /check", file=sys.stderr)
    print(f"[INFO] Health: GET /health", file=sys.stderr)

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n[INFO] Остановка сервера...", file=sys.stderr)
        server.shutdown()


if __name__ == "__main__":
    main()
