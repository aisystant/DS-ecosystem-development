#!/usr/bin/env python3
"""
Скрипт для анализа динамики роста репозитория.
Собирает метрики по дням: количество файлов, строк и символов в .md документах.
"""

import subprocess
import os
from datetime import datetime, timedelta
from collections import defaultdict
import json

def run_git_command(cmd):
    """Выполнить git команду и вернуть результат."""
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    return result.stdout.strip()

def get_commit_dates():
    """Получить список уникальных дат с коммитами."""
    output = run_git_command("git log --format='%ad' --date=short")
    dates = sorted(set(output.split('\n')))
    return [d for d in dates if d]

def get_last_commit_of_day(date):
    """Получить последний коммит за указанную дату."""
    cmd = f"git log --format='%H' --date=short --until='{date} 23:59:59' -1"
    return run_git_command(cmd)

def count_metrics_at_commit(commit_hash):
    """Подсчитать метрики для .md файлов в конкретном коммите."""
    # Получаем список .md файлов
    cmd = f"git ls-tree -r --name-only {commit_hash} | grep '\\.md$'"
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    md_files = [f for f in result.stdout.strip().split('\n') if f]

    total_files = len(md_files)
    total_lines = 0
    total_chars = 0

    # Подсчитываем строки и символы для каждого файла
    for file_path in md_files:
        cmd = f"git show {commit_hash}:{file_path} 2>/dev/null"
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            content = result.stdout
            total_lines += len(content.split('\n'))
            total_chars += len(content)

    return {
        'files': total_files,
        'lines': total_lines,
        'chars': total_chars
    }

def collect_metrics():
    """Собрать метрики по всем дням с коммитами."""
    dates = get_commit_dates()
    metrics = []

    print(f"Найдено {len(dates)} дней с коммитами")
    print("-" * 60)

    for date in dates:
        commit = get_last_commit_of_day(date)
        if commit:
            data = count_metrics_at_commit(commit)
            data['date'] = date
            data['commit'] = commit[:7]
            metrics.append(data)
            print(f"{date}: {data['files']} файлов, {data['lines']:,} строк, {data['chars']:,} символов")

    return metrics

def print_summary(metrics):
    """Вывести сводку по росту."""
    if len(metrics) < 2:
        print("\nНедостаточно данных для расчёта динамики")
        return

    first = metrics[0]
    last = metrics[-1]

    files_growth = last['files'] - first['files']
    lines_growth = last['lines'] - first['lines']
    chars_growth = last['chars'] - first['chars']

    days = (datetime.strptime(last['date'], '%Y-%m-%d') -
            datetime.strptime(first['date'], '%Y-%m-%d')).days or 1

    print("\n" + "=" * 60)
    print("ДИНАМИКА РОСТА РЕПОЗИТОРИЯ")
    print("=" * 60)
    print(f"Период: {first['date']} — {last['date']} ({days} дней)")
    print()
    print(f"{'Метрика':<20} {'Начало':>12} {'Конец':>12} {'Прирост':>12} {'В день':>10}")
    print("-" * 66)
    print(f"{'Документов (.md)':<20} {first['files']:>12,} {last['files']:>12,} {files_growth:>+12,} {files_growth/days:>+10.1f}")
    print(f"{'Строк':<20} {first['lines']:>12,} {last['lines']:>12,} {lines_growth:>+12,} {lines_growth/days:>+10.1f}")
    print(f"{'Символов':<20} {first['chars']:>12,} {last['chars']:>12,} {chars_growth:>+12,} {chars_growth/days:>+10.1f}")

    if first['files'] > 0:
        files_pct = (last['files'] / first['files'] - 1) * 100
        lines_pct = (last['lines'] / first['lines'] - 1) * 100 if first['lines'] > 0 else 0
        chars_pct = (last['chars'] / first['chars'] - 1) * 100 if first['chars'] > 0 else 0

        print()
        print(f"{'Рост за период:':<20} {files_pct:>+.1f}% файлов, {lines_pct:>+.1f}% строк, {chars_pct:>+.1f}% символов")

def print_daily_chart(metrics, metric='files', width=50):
    """Вывести ASCII-график изменения метрики по дням."""
    if not metrics:
        return

    values = [m[metric] for m in metrics]
    max_val = max(values)
    min_val = min(values)
    range_val = max_val - min_val or 1

    labels = {'files': 'Документы (.md)', 'lines': 'Строки', 'chars': 'Символы'}

    print(f"\n{'=' * 60}")
    print(f"ГРАФИК: {labels.get(metric, metric)}")
    print("=" * 60)

    for m in metrics:
        val = m[metric]
        bar_len = int((val - min_val) / range_val * width) if range_val > 0 else width
        bar = '█' * bar_len
        print(f"{m['date'][5:]}: {bar} {val:,}")

def save_to_json(metrics, filename='repo_growth_metrics.json'):
    """Сохранить метрики в JSON файл."""
    output_path = os.path.join(os.path.dirname(__file__), '..', 'artifacts', filename)
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump({
            'generated_at': datetime.now().isoformat(),
            'metrics': metrics
        }, f, ensure_ascii=False, indent=2)

    print(f"\nДанные сохранены в: {output_path}")
    return output_path

def main():
    """Основная функция."""
    print("Анализ динамики роста репозитория")
    print("=" * 60)

    # Собираем метрики
    metrics = collect_metrics()

    # Выводим сводку
    print_summary(metrics)

    # Выводим графики
    print_daily_chart(metrics, 'files')
    print_daily_chart(metrics, 'lines')
    print_daily_chart(metrics, 'chars')

    # Сохраняем данные
    save_to_json(metrics)

if __name__ == '__main__':
    main()
