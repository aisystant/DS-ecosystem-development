#!/usr/bin/env python3
"""
Генератор автоматических отчётов по хранилищу знаний.

Использование:
    python3 ops/build_report.py --report architecture-snapshot
    python3 ops/build_report.py --report content-completeness
    python3 ops/build_report.py --report technical-issues
    python3 ops/build_report.py --report all

Типы отчётов:
    architecture-snapshot   - Архитектурный слепок хранилища
    content-completeness    - Содержательная полнота описания
    technical-issues        - Противоречия и несогласованности хранилища
    terminology             - Терминологическая согласованность
    recommendations         - Рекомендации по развитию
    links-map               - Карта связей между документами
    all                     - Все отчёты
"""

import os
import re
import sys
import json
import yaml
import argparse
import hashlib
from pathlib import Path
from datetime import datetime
from collections import defaultdict
from typing import Dict, List, Optional, Tuple, Any

# Константы
CONTENT_DIR = Path("content")
REPORTS_DIR = CONTENT_DIR / "0. Управление" / "0.4. Автоматические отчёты ИИ"

# Семейства документов F0-F9
FAMILIES = {
    "F0": {"name": "Управление", "level": "Метасистема", "role": "-", "section": "0"},
    "F1": {"name": "Видение и привлечение", "level": "Мир", "role": "Предприниматель", "section": "1.1"},
    "F2": {"name": "Контекст и интерфейсы", "level": "Мир", "role": "Инженер", "section": "1.2"},
    "F3": {"name": "Репутация и партнёрства", "level": "Мир", "role": "Менеджер", "section": "1.3"},
    "F4": {"name": "Ценность и бизнес-модели", "level": "Созидатель", "role": "Предприниматель", "section": "2.1"},
    "F5": {"name": "Модель и компетенции", "level": "Созидатель", "role": "Инженер", "section": "2.2"},
    "F6": {"name": "Путь и сопровождение", "level": "Созидатель", "role": "Менеджер", "section": "2.3"},
    "F7": {"name": "Экономика и инвестиции", "level": "Экосистема", "role": "Предприниматель", "section": "3.1"},
    "F8": {"name": "Платформа и подсистемы", "level": "Экосистема", "role": "Инженер", "section": "3.2"},
    "F9": {"name": "Команда и службы", "level": "Экосистема", "role": "Менеджер", "section": "3.3"},
}

# Соответствие папок семействам
FOLDER_TO_FAMILY = {
    "0. Управление": "F0",
    "1. Мир (Надсистема)": None,  # Определяется по подпапке
    "1.1.": "F1",
    "1.2.": "F2",
    "1.3.": "F3",
    "2. Созидатель (Целевая система)": None,
    "2.1.": "F4",
    "2.2.": "F5",
    "2.3.": "F6",
    "3. Экосистема развития (Система создания)": None,
    "3.1.": "F7",
    "3.2.": "F8",
    "3.3.": "F9",
}


class Document:
    """Представление документа хранилища."""

    def __init__(self, path: Path):
        self.path = path
        self.relative_path = path.relative_to(CONTENT_DIR) if path.is_relative_to(CONTENT_DIR) else path
        self.name = path.stem
        self.content = ""
        self.frontmatter: Dict[str, Any] = {}
        self.body = ""
        self.wikilinks: List[str] = []
        self.headings: List[Tuple[int, str]] = []
        self.family: Optional[str] = None
        self.size = 0
        self._parse()

    def _parse(self):
        """Парсинг документа: frontmatter, контент, ссылки."""
        try:
            self.content = self.path.read_text(encoding="utf-8")
            self.size = len(self.content)
        except Exception as e:
            print(f"⚠️  Ошибка чтения {self.path}: {e}")
            return

        # Парсинг frontmatter
        if self.content.startswith("---"):
            parts = self.content.split("---", 2)
            if len(parts) >= 3:
                try:
                    self.frontmatter = yaml.safe_load(parts[1]) or {}
                except yaml.YAMLError:
                    self.frontmatter = {}
                self.body = parts[2].strip()
            else:
                self.body = self.content
        else:
            self.body = self.content

        # Извлечение wikilinks
        self.wikilinks = re.findall(r'\[\[([^\]|]+)(?:\|[^\]]+)?\]\]', self.body)

        # Извлечение заголовков
        self.headings = [(len(m.group(1)), m.group(2))
                         for m in re.finditer(r'^(#{1,6})\s+(.+)$', self.body, re.MULTILINE)]

        # Определение семейства
        self.family = self._detect_family()

    def _detect_family(self) -> Optional[str]:
        """Определение семейства документа по пути и frontmatter."""
        # Приоритет: frontmatter
        if "family" in self.frontmatter:
            return self.frontmatter["family"]

        # По пути
        path_str = str(self.relative_path)
        for pattern, family in FOLDER_TO_FAMILY.items():
            if pattern in path_str:
                if family:
                    return family
                # Для корневых папок смотрим подпапку
                for sub_pattern, sub_family in FOLDER_TO_FAMILY.items():
                    if sub_pattern in path_str and sub_family:
                        return sub_family

        return None

    @property
    def is_empty(self) -> bool:
        """Документ считается пустым, если контент < 200 символов или содержит только TODO."""
        body_clean = re.sub(r'<!--.*?-->', '', self.body, flags=re.DOTALL)
        body_clean = re.sub(r'TODO|FIXME', '', body_clean, flags=re.IGNORECASE)
        return len(body_clean.strip()) < 200

    @property
    def status(self) -> str:
        return self.frontmatter.get("status", "unknown")

    @property
    def doc_type(self) -> str:
        return self.frontmatter.get("type", "unknown")


class ReportGenerator:
    """Базовый класс для генерации отчётов."""

    def __init__(self):
        self.documents: List[Document] = []
        self.by_family: Dict[str, List[Document]] = defaultdict(list)
        self.timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.git_hash = self._get_git_hash()

    def _get_git_hash(self) -> str:
        """Получение текущего git commit hash."""
        try:
            import subprocess
            result = subprocess.run(
                ["git", "rev-parse", "--short", "HEAD"],
                capture_output=True, text=True, check=True
            )
            return result.stdout.strip()
        except:
            return "unknown"

    def scan_documents(self):
        """Сканирование всех документов в хранилище."""
        print("📂 Сканирование документов...")

        for md_file in CONTENT_DIR.rglob("*.md"):
            # Пропускаем служебные файлы
            if any(skip in str(md_file) for skip in [".obsidian", "node_modules", ".git"]):
                continue

            doc = Document(md_file)
            self.documents.append(doc)

            if doc.family:
                self.by_family[doc.family].append(doc)

        print(f"   Найдено документов: {len(self.documents)}")
        for family, docs in sorted(self.by_family.items()):
            print(f"   {family}: {len(docs)}")

    def generate(self, report_type: str) -> str:
        """Генерация отчёта указанного типа."""
        generators = {
            "architecture-snapshot": self._generate_architecture_snapshot,
            "content-completeness": self._generate_content_completeness,
            "technical-issues": self._generate_technical_issues,
            "terminology": self._generate_terminology,
            "recommendations": self._generate_recommendations,
            "links-map": self._generate_links_map,
        }

        if report_type not in generators:
            raise ValueError(f"Неизвестный тип отчёта: {report_type}")

        return generators[report_type]()

    def _header(self, title: str, extra: str = "") -> str:
        """Заголовок отчёта."""
        return f"""# {title}

> Автоматически сформирован: {self.timestamp}
> Проанализировано документов: {len(self.documents)}
> Версия хранилища: {self.git_hash}
{extra}
---

"""

    # ==================== АРХИТЕКТУРНЫЙ СЛЕПОК ====================

    def _generate_architecture_snapshot(self) -> str:
        """Генерация отчёта 'Архитектурный слепок хранилища'."""
        report = self._header(
            "Архитектурный слепок хранилища",
            "\n**Структура документа**: Иерархическая — соответствует логике описания экосистемы от целей к реализации.\n"
        )

        # Тепловая карта разделов
        report += self._architecture_heatmap()

        # Разделы
        report += self._architecture_section_1_mission()
        report += self._architecture_section_2_personas()
        report += self._architecture_section_3_goals()
        report += self._architecture_section_4_creator()
        report += self._architecture_section_5_functioning()
        report += self._architecture_section_6_platform()
        report += self._architecture_section_7_data()
        report += self._architecture_section_8_epistemic()
        report += self._architecture_section_9_economy()
        report += self._architecture_section_10_quality()
        report += self._architecture_section_11_metrics()
        report += self._architecture_section_12_stats()
        report += self._architecture_section_13_links()

        return report

    def _architecture_heatmap(self) -> str:
        """Тепловая карта разделов для архитектурного слепка."""
        sections = [
            ("Миссия и ценности", "F1", 5),
            ("Персоны и роли", "F5", 4),
            ("Цели и задачи", "F1", 3),
            ("Целевая система", "F4,F5", 8),
            ("Функционирование", "F6", 6),
            ("Платформа", "F8", 15),
            ("Данные и сущности", "F8", 5),
            ("Эпистемический статус", "F8", 3),
            ("Экономика", "F7", 4),
            ("Качество", "F0", 5),
            ("Метрики", "F0", 3),
        ]

        heatmap = "## Тепловая карта разделов\n\n"
        heatmap += "| Раздел | Статус | Документов |\n"
        heatmap += "|--------|--------|------------|\n"

        for name, families, expected in sections:
            count = sum(len(self.by_family.get(f, [])) for f in families.split(","))
            ratio = count / expected if expected > 0 else 0
            status = "🟢" if ratio >= 0.8 else ("🟡" if ratio >= 0.4 else "🔴")
            heatmap += f"| {name} | {status} | {count} |\n"

        return heatmap + "\n---\n\n"

    def _architecture_section_1_mission(self) -> str:
        """Раздел 1: Зачем, для кого, что мы делаем."""
        section = "## 1. Зачем, для кого, что мы делаем\n\n"

        # Ищем манифест
        manifesto = self._find_doc_by_pattern("Манифест")
        if manifesto:
            section += "### 1.1. Миссия экосистемы\n\n"
            section += self._extract_summary(manifesto, max_sentences=3)
            section += "\n\n"

        section += "### 1.2. Три инварианта (конституционный слой)\n\n"
        section += "- **Эволюционность** — любой процесс способен к непрерывному улучшению через циклы обратной связи\n"
        section += "- **Сквозная целостность** — от личных целей до глобальных систем единая трассировка\n"
        section += "- **Дидактическая прозрачность** — каждый артефакт показывает свою причинно-следственную дорожку\n\n"

        section += "### 1.3. Принципы реализации\n\n"
        section += "- C4+ADR для архитектурного описания\n"
        section += "- Минимально достаточная документация\n"
        section += "- Разделение Method / MethodDescription / Work\n\n"

        sources = [d.name for d in self.by_family.get("F1", [])[:3]]
        section += f"**Источники:** {', '.join(f'[[{s}]]' for s in sources)}\n\n"

        return section + "---\n\n"

    def _architecture_section_2_personas(self) -> str:
        """Раздел 2: Персоны и роли."""
        section = "## 2. Персоны и роли\n\n"

        section += "### 2.1. Целевые аудитории\n\n"
        ta_doc = self._find_doc_by_pattern("Целевые аудитории")
        if ta_doc:
            section += self._extract_summary(ta_doc, max_sentences=3)
        else:
            section += "*Документ не найден*\n"
        section += "\n\n"

        section += "### 2.2. Роли в экосистеме\n\n"
        section += "- Ученик/Стажёр\n"
        section += "- Создатель/Методист\n"
        section += "- Куратор/Ментор\n"
        section += "- Разработчик ИИ-агентов\n"
        section += "- Организатор/Оунер проекта\n"
        section += "- Эпистемический совет\n\n"

        return section + "---\n\n"

    def _architecture_section_3_goals(self) -> str:
        """Раздел 3: Проблемы, гипотезы и цели."""
        section = "## 3. Проблемы, гипотезы и цели\n\n"

        section += "### 3.1. Ключевые проблемы\n\n"
        problems_doc = self._find_doc_by_pattern("Проблемы")
        if problems_doc:
            section += self._extract_summary(problems_doc, max_sentences=5)
        else:
            section += "- Свобода без «грамматики» личной траектории\n"
            section += "- «Интеллект как узкое место»\n"
            section += "- Обучение «рядом», а не внутри производства\n"
        section += "\n\n"

        section += "### 3.2. Гипотезы решения\n\n"
        hypotheses_doc = self._find_doc_by_pattern("Гипотезы")
        if hypotheses_doc:
            section += self._extract_summary(hypotheses_doc, max_sentences=5)
        section += "\n\n"

        section += "### 3.3. Цели по горизонтам\n\n"
        section += "- **2026** — доказательства и сборка ядра\n"
        section += "- **2027–2030** — масштабирование и стандарты\n"
        section += "- **После 2030** — культурная норма\n\n"

        return section + "---\n\n"

    def _architecture_section_4_creator(self) -> str:
        """Раздел 4: Целевая система - Созидатель."""
        section = "## 4. Целевая система: Созидатель\n\n"

        section += "### 4.1. Что такое Созидатель\n\n"
        creator_doc = self._find_doc_by_pattern("Концепция созидателя")
        if creator_doc:
            section += self._extract_summary(creator_doc, max_sentences=3)
        section += "\n\n"

        section += "### 4.2. Модель компетенций и уровни мастерства\n\n"
        competencies_doc = self._find_doc_by_pattern("Карта компетенций|Компетенции")
        if competencies_doc:
            section += self._extract_summary(competencies_doc, max_sentences=3)
        section += "\n\n"

        section += "### 4.3. Ценностное предложение\n\n"
        value_doc = self._find_doc_by_pattern("Ценностное предложение")
        if value_doc:
            section += self._extract_summary(value_doc, max_sentences=3)
        section += "\n\n"

        section += "### 4.4. Ролевая траектория\n\n"
        section += "Ученик → Интеллектуал → Профессионал → Исследователь → Просветитель\n\n"

        return section + "---\n\n"

    def _architecture_section_5_functioning(self) -> str:
        """Раздел 5: Функционирование экосистемы."""
        section = "## 5. Функционирование экосистемы\n\n"

        section += "### 5.1. Главные процессы (сквозные циклы)\n\n"
        section += "- **C1.** Онбординг и инициализация двойника\n"
        section += "- **C2.** Обучение → Артефакт → Перенос\n"
        section += "- **C3.** Производство руководств\n"
        section += "- **C4.** Конструирование и эксплуатация ИИ-агентов\n"
        section += "- **C5.** Продвижение (просвещение, маркетинг, продажи)\n"
        section += "- **C6.** Товарообмен и расчёты (фиат + токен)\n"
        section += "- **C7.** Экономика вклада (токен)\n"
        section += "- **C8.** Исследование научного фронтира\n"
        section += "- **C9.** Наблюдаемость/качество\n"
        section += "- **C10.** Подтверждение эпистемического статуса\n\n"

        section += "### 5.2. Концепция использования для ролей\n\n"
        conops_doc = self._find_doc_by_pattern("Концепция функционирования")
        if conops_doc:
            section += self._extract_summary(conops_doc, max_sentences=5)
        section += "\n\n"

        return section + "---\n\n"

    def _architecture_section_6_platform(self) -> str:
        """Раздел 6: Структура ИИ-платформы."""
        section = "## 6. Структура ИИ-платформы\n\n"

        section += "### 6.1. Карта подсистем\n\n"

        # Ищем документы подсистем
        subsystems = [d for d in self.by_family.get("F8", [])
                      if any(kw in d.name.lower() for kw in ["подсистем", "система", "платформа"])]

        if subsystems:
            section += "| № | Подсистема | Описание |\n"
            section += "|---|------------|----------|\n"
            for i, doc in enumerate(subsystems[:10], 1):
                desc = self._extract_first_sentence(doc)
                section += f"| {i} | [[{doc.name}]] | {desc[:80]}... |\n"
        section += "\n"

        section += "### 6.2. Мультиагентная ОС: компоненты\n\n"
        section += "- **Reasoning Core** — планирование и выбор инструментов\n"
        section += "- **Memory Store** — хранилище знаний и контекста\n"
        section += "- **Tool/Action Interface** — декларативные действия (Apps SDK)\n"
        section += "- **Goal Manager** — цели, ограничения, бюджеты\n"
        section += "- **Dialogue Layer** — коммуникация с пользователем\n\n"

        section += "### 6.3. Стадии жизненного цикла агента\n\n"
        section += "1. **Инициализация** — цель, метрики, контекст\n"
        section += "2. **Планирование** — выбор инструментов, план вызовов\n"
        section += "3. **Выполнение** — вызовы инструментов, протоколирование\n"
        section += "4. **Оценка** — пересчёт ценности, самокритика\n\n"

        return section + "---\n\n"

    def _architecture_section_7_data(self) -> str:
        """Раздел 7: Данные и сущности."""
        section = "## 7. Данные и сущности\n\n"

        section += "### 7.1. Сквозные модели данных\n\n"
        section += "- **Digital Twin** — цели, навыки, предпочтения, расписание\n"
        section += "- **Epistemic Graph** — эпистемы и их статусы/связи/доказательства\n"
        section += "- **Activity Ledger** — все события (обучение, проекты, публикации)\n"
        section += "- **Token Ledger** — начисления/списания, заморозки, тарифы\n\n"

        section += "### 7.2. Основные сущности\n\n"
        section += "`User`, `DigitalTwin`, `Program`, `Guide/Step/Task`, `Artifact`, "
        section += "`ActionEvent`, `Qualification`, `Episteme`, `Work`, `MethodDescription`, `Evidence`\n\n"

        section += "### 7.3. Политика библиотеки\n\n"
        section += "- **curated/** — строго через PR/ревью\n"
        section += "- **derived/** — только автоматом (агенты/ETL)\n\n"

        return section + "---\n\n"

    def _architecture_section_8_epistemic(self) -> str:
        """Раздел 8: Эпистемический статус."""
        section = "## 8. Эпистемический статус и доказательства\n\n"

        section += "### 8.1. ESG (Epistemic Status Graph)\n\n"
        section += "**Draft** → **PeerChecked** → **Accepted** → **Superseded**\n\n"

        section += "### 8.2. Сигналы для статуса\n\n"
        section += "- Подтверждённые артефакты и их перенос\n"
        section += "- Рецензии наставников\n"
        section += "- Использование другими\n"
        section += "- Стабильность недельных инкрементов\n"
        section += "- Evidence-bindings к утверждениям\n\n"

        section += "### 8.3. Процедура присвоения и обновления\n\n"
        section += "1. Сбор сигналов из событийной шины\n"
        section += "2. Нормировка по сложности задачи\n"
        section += "3. Предварительный рейтинг\n"
        section += "4. Человеческое подтверждение (по порогу риска)\n"
        section += "5. Публикация статуса и логика «старения»\n\n"

        return section + "---\n\n"

    def _architecture_section_9_economy(self) -> str:
        """Раздел 9: Экономика вклада."""
        section = "## 9. Экономика вклада: Proof-of-Impact и токеномика\n\n"

        section += "### 9.1. Идея и пайплайн начисления\n\n"
        section += "События → Work → Episteme → Evidence → Начисление → Заморозка\n\n"

        section += "### 9.2. Как зарабатывать и тратить токены\n\n"
        section += "**Заработок:**\n"
        section += "- За подтверждённые уроки/сертификации\n"
        section += "- За ревью чужих артефактов\n"
        section += "- За публикации с доказанным охватом\n"
        section += "- За вклад в проекты с измеримым эффектом\n\n"
        section += "**Расход:**\n"
        section += "- Доступ к премиум-курсам\n"
        section += "- Вычислительные квоты агентов\n"
        section += "- Маркетплейс ИИ-ассистентов\n"
        section += "- Сессии с наставниками\n\n"

        section += "### 9.3. Внутренняя биржа и управление treasury\n\n"
        tokenomics_doc = self._find_doc_by_pattern("Токеномика")
        if tokenomics_doc:
            section += self._extract_summary(tokenomics_doc, max_sentences=3)
        section += "\n\n"

        return section + "---\n\n"

    def _architecture_section_10_quality(self) -> str:
        """Раздел 10: Культура и стандарты качества."""
        section = "## 10. Культура и стандарты качества\n\n"

        section += "### 10.1. Принципы качества\n\n"
        section += "- **Делать-показывать-мерить-улучшать** — недельные инкременты и peer-review\n"
        section += "- **Воспроизводимость** — логи, версии, источники, критерии приёмки\n"
        section += "- **Curated vs Derived** — ручная зона отделена от авто-зоны\n"
        section += "- **Минимальные привилегии** — Policy-as-code в Apps SDK\n\n"

        section += "### 10.2. Архитектурные границы и принятие решений\n\n"
        section += "- **C4 Model** — контекст → контейнеры → компоненты\n"
        section += "- **ADR** — контекст → решение → trade-offs → ссылки\n\n"

        return section + "---\n\n"

    def _architecture_section_11_metrics(self) -> str:
        """Раздел 11: Метрики."""
        section = "## 11. Метрики\n\n"

        section += "### 11.1. Ключевые метрики\n\n"
        section += "- **Time-to-Master (TTM)** — время до достижения уровня мастера\n"
        section += "- **Cost-to-Master (CTM)** — суммарные затраты (фиат + токены)\n"
        section += "- **Время онбординга** — <30 минут до первого значимого действия\n"
        section += "- **Качество и перенос** — доля задач с переносом (7–14 дней)\n"
        section += "- **Экономика** — MRR/NRR, оборот токена\n"
        section += "- **Репутация** — динамика эпистемического статуса\n\n"

        return section + "---\n\n"

    def _architecture_section_12_stats(self) -> str:
        """Раздел 12: Статистика хранилища."""
        section = "## 12. Статистика хранилища\n\n"

        section += "| Метрика | Значение |\n"
        section += "|---------|----------|\n"
        section += f"| Всего документов | {len(self.documents)} |\n"

        by_family_str = ", ".join(f"{f}: {len(docs)}" for f, docs in sorted(self.by_family.items()))
        section += f"| По семействам | {by_family_str} |\n"

        active = sum(1 for d in self.documents if d.status == "active")
        draft = sum(1 for d in self.documents if d.status == "draft")
        section += f"| Активных | {active} |\n"
        section += f"| Черновиков | {draft} |\n\n"

        return section + "---\n\n"

    def _architecture_section_13_links(self) -> str:
        """Раздел 13: Связанные документы."""
        return """## 13. Связанные документы

- [[Концепция автоматических отчётов ИИ 0.4.1]]
- [[Содержательная полнота описания 0.4]]
- [[Модель семейств документов 0.1]]
"""

    # ==================== СОДЕРЖАТЕЛЬНАЯ ПОЛНОТА ====================

    def _generate_content_completeness(self) -> str:
        """Генерация отчёта 'Содержательная полнота описания'."""
        report = self._header("Содержательная полнота описания")

        # Тепловая карта 3x3
        report += self._completeness_heatmap()

        # Executive Summary
        report += self._completeness_summary()

        # Анализ по ячейкам
        report += self._completeness_by_cells()

        # Применение SoTA-методов
        report += self._completeness_sota()

        # Интересы стейкхолдеров
        report += self._completeness_stakeholders()

        # Приоритизированные пробелы
        report += self._completeness_gaps()

        # Связанные документы
        report += self._completeness_links()

        return report

    def _completeness_heatmap(self) -> str:
        """Тепловая карта 3x3 для содержательной полноты."""
        heatmap = "## Тепловая карта содержательной полноты\n\n"

        # Ожидаемое количество документов по семействам
        expected = {"F1": 8, "F2": 6, "F3": 6, "F4": 6, "F5": 8, "F6": 6, "F7": 6, "F8": 15, "F9": 10}

        def status(family):
            count = len(self.by_family.get(family, []))
            exp = expected.get(family, 5)
            ratio = count / exp
            return "🟢" if ratio >= 0.8 else ("🟡" if ratio >= 0.4 else "🔴")

        heatmap += "|                    | Предприниматель | Инженер | Менеджер |\n"
        heatmap += "|                    | (Смыслы)        | (Архитектура) | (Операции) |\n"
        heatmap += "|--------------------|-----------------|---------|----------|\n"
        heatmap += f"| **Мир (Надсистема)** | {status('F1')} F1 ({len(self.by_family.get('F1', []))}) | {status('F2')} F2 ({len(self.by_family.get('F2', []))}) | {status('F3')} F3 ({len(self.by_family.get('F3', []))}) |\n"
        heatmap += f"| **Созидатель (Целевая)** | {status('F4')} F4 ({len(self.by_family.get('F4', []))}) | {status('F5')} F5 ({len(self.by_family.get('F5', []))}) | {status('F6')} F6 ({len(self.by_family.get('F6', []))}) |\n"
        heatmap += f"| **Экосистема (Создания)** | {status('F7')} F7 ({len(self.by_family.get('F7', []))}) | {status('F8')} F8 ({len(self.by_family.get('F8', []))}) | {status('F9')} F9 ({len(self.by_family.get('F9', []))}) |\n"

        return heatmap + "\n---\n\n"

    def _completeness_summary(self) -> str:
        """Executive Summary для содержательной полноты."""
        total_docs = len(self.documents)
        expected_total = 71  # Сумма ожидаемых
        completeness = min(100, int(total_docs / expected_total * 100))

        # Найти самые полные и самые пустые семейства
        family_ratios = {}
        expected = {"F1": 8, "F2": 6, "F3": 6, "F4": 6, "F5": 8, "F6": 6, "F7": 6, "F8": 15, "F9": 10}
        for f, exp in expected.items():
            count = len(self.by_family.get(f, []))
            family_ratios[f] = count / exp

        best = max(family_ratios, key=family_ratios.get)
        worst = min(family_ratios, key=family_ratios.get)

        gaps = [f for f, ratio in family_ratios.items() if ratio < 0.4]

        summary = "## 1. Executive Summary\n\n"
        summary += f"- **Общая содержательная полнота:** {completeness}%\n"
        summary += f"- **Наиболее полное семейство:** {best} ({FAMILIES[best]['name']}) — {int(family_ratios[best]*100)}%\n"
        summary += f"- **Наименее полное семейство:** {worst} ({FAMILIES[worst]['name']}) — {int(family_ratios[worst]*100)}%\n"
        summary += f"- **Критические пробелы:** {', '.join(gaps) if gaps else 'нет'}\n\n"

        return summary + "---\n\n"

    def _completeness_by_cells(self) -> str:
        """Анализ по ячейкам матрицы 3x3."""
        cells = ""

        for family_id in ["F1", "F2", "F3", "F4", "F5", "F6", "F7", "F8", "F9"]:
            family = FAMILIES[family_id]
            docs = self.by_family.get(family_id, [])

            cells += f"### 2.{family_id[1]}. {family['level']} × {family['role']} ({family_id}: {family['name']})\n\n"

            expected = {"F1": 8, "F2": 6, "F3": 6, "F4": 6, "F5": 8, "F6": 6, "F7": 6, "F8": 15, "F9": 10}
            ratio = len(docs) / expected.get(family_id, 5)
            status = "🟢" if ratio >= 0.8 else ("🟡" if ratio >= 0.4 else "🔴")

            cells += f"**Статус:** {status} ({len(docs)} документов)\n\n"

            if docs:
                cells += "**Документы:**\n"
                for doc in docs[:5]:
                    cells += f"- [[{doc.name}]]\n"
                if len(docs) > 5:
                    cells += f"- ... и ещё {len(docs) - 5}\n"
            else:
                cells += "*Документы отсутствуют*\n"

            cells += "\n"

        return "## 2. Анализ по ячейкам матрицы 3×3\n\n" + cells + "---\n\n"

    def _completeness_sota(self) -> str:
        """Проверка применения SoTA-методов."""
        sota = "## 3. Применение SoTA-методов\n\n"

        # Проверяем наличие артефактов методов
        methods = {
            "JTBD": self._find_doc_by_pattern("JTBD|Jobs.to.be.done"),
            "Value Proposition": self._find_doc_by_pattern("Ценностное предложение|Value Proposition"),
            "C4 Model": self._find_doc_by_pattern("C4|Контекст.*контейнер|архитектур"),
            "ADR": self._find_doc_by_pattern("ADR|Architecture Decision"),
            "ConOps": self._find_doc_by_pattern("ConOps|Концепция.*использования|Concept.*Operations"),
            "OKR": self._find_doc_by_pattern("OKR|Objectives.*Key.*Results|Цели.*задачи"),
        }

        sota += "| Метод | Статус | Документ |\n"
        sota += "|-------|--------|----------|\n"

        for method, doc in methods.items():
            if doc:
                sota += f"| {method} | ✅ Применён | [[{doc.name}]] |\n"
            else:
                sota += f"| {method} | ❌ Не найден | — |\n"

        return sota + "\n---\n\n"

    def _completeness_stakeholders(self) -> str:
        """Ответы на интересы заинтересованных лиц."""
        stakeholders = "## 4. Ответы на интересы заинтересованных лиц\n\n"

        questions = [
            ("Ученик", "Что я получу?", "F4", "Ценностное предложение"),
            ("Ученик", "Как начать?", "F6", "Онбординг"),
            ("Наставник", "Как работать с учениками?", "F6", "Деканат|наставник"),
            ("Инвестор", "Какова бизнес-модель?", "F7", "Экономическ|бизнес.модел"),
            ("Разработчик", "Как устроена платформа?", "F8", "Архитектур|платформ"),
            ("Партнёр", "Как интегрироваться?", "F2", "Интеграц|партнёр"),
        ]

        stakeholders += "| Стейкхолдер | Вопрос | Статус | Где ответ |\n"
        stakeholders += "|-------------|--------|--------|----------|\n"

        for stakeholder, question, family, pattern in questions:
            doc = self._find_doc_by_pattern(pattern)
            if doc:
                stakeholders += f"| {stakeholder} | {question} | ✅ | [[{doc.name}]] |\n"
            else:
                stakeholders += f"| {stakeholder} | {question} | ❌ | *Не найден* |\n"

        return stakeholders + "\n---\n\n"

    def _completeness_gaps(self) -> str:
        """Приоритизированные пробелы."""
        gaps = "## 5. Приоритизированные пробелы\n\n"

        expected = {"F1": 8, "F2": 6, "F3": 6, "F4": 6, "F5": 8, "F6": 6, "F7": 6, "F8": 15, "F9": 10}

        critical = []
        important = []

        for f, exp in expected.items():
            count = len(self.by_family.get(f, []))
            ratio = count / exp
            if ratio < 0.4:
                critical.append((f, FAMILIES[f]['name'], int(ratio * 100)))
            elif ratio < 0.8:
                important.append((f, FAMILIES[f]['name'], int(ratio * 100)))

        gaps += "### 5.1. Критические 🔴\n\n"
        if critical:
            for f, name, pct in critical:
                gaps += f"- **{f} ({name})** — {pct}% заполненности\n"
        else:
            gaps += "*Критических пробелов нет*\n"
        gaps += "\n"

        gaps += "### 5.2. Важные 🟡\n\n"
        if important:
            for f, name, pct in important:
                gaps += f"- **{f} ({name})** — {pct}% заполненности\n"
        else:
            gaps += "*Важных пробелов нет*\n"

        return gaps + "\n---\n\n"

    def _completeness_links(self) -> str:
        return """## 6. Связанные документы

- [[Концепция автоматических отчётов ИИ 0.4.1]]
- [[Модель семейств документов 0.1]]
- [[Структура хранилища 0.1]]
"""

    # ==================== ТЕХНИЧЕСКИЕ ПРОБЛЕМЫ ====================

    def _generate_technical_issues(self) -> str:
        """Генерация отчёта 'Противоречия и несогласованности хранилища'."""
        report = self._header("Противоречия и несогласованности хранилища")

        # Собираем проблемы
        dup_folders = self._find_duplicate_folders()
        dup_docs = self._find_duplicate_documents()
        broken_links = self._find_broken_links()
        missing_metadata = self._find_missing_metadata()

        # Тепловая карта
        report += self._technical_heatmap(dup_folders, dup_docs, broken_links, missing_metadata)

        # Executive Summary
        total = len(dup_folders) + len(dup_docs) + len(broken_links) + len(missing_metadata)
        critical = len(dup_folders) + len([d for d in dup_docs if d[2] == "exact"])

        report += "## 1. Executive Summary\n\n"
        report += f"- **Всего технических проблем:** {total}\n"
        report += f"- **Критических:** {critical}\n"
        report += f"- **Требуют внимания:** {total - critical}\n\n"
        report += "---\n\n"

        # Дублирование папок
        report += self._technical_dup_folders(dup_folders)

        # Дублирование документов
        report += self._technical_dup_docs(dup_docs)

        # Битые ссылки
        report += self._technical_broken_links(broken_links)

        # Отсутствующие метаданные
        report += self._technical_missing_metadata(missing_metadata)

        # Связанные документы
        report += """## 7. Связанные документы

- [[Концепция автоматических отчётов ИИ 0.4.1]]
- [[Терминологическая согласованность 0.4]]
- [[Структура хранилища 0.1]]
"""

        return report

    def _technical_heatmap(self, dup_folders, dup_docs, broken_links, missing_metadata) -> str:
        heatmap = "## Тепловая карта технических проблем\n\n"
        heatmap += "| Тип проблемы | Количество | Статус |\n"
        heatmap += "|--------------|------------|--------|\n"

        def status(count, threshold_red=1, threshold_yellow=5):
            if count >= threshold_red:
                return "🔴"
            elif count >= threshold_yellow:
                return "🟡"
            return "🟢"

        heatmap += f"| Дублирование названий папок | {len(dup_folders)} | {status(len(dup_folders))} |\n"
        heatmap += f"| Дублирование названий документов | {len(dup_docs)} | {status(len(dup_docs), 3, 10)} |\n"
        heatmap += f"| Битые wikilinks | {len(broken_links)} | {status(len(broken_links), 5, 15)} |\n"
        heatmap += f"| Несогласованность метаданных | {len(missing_metadata)} | {status(len(missing_metadata), 10, 30)} |\n"

        total = len(dup_folders) + len(dup_docs) + len(broken_links) + len(missing_metadata)
        heatmap += f"| **Итого проблем** | **{total}** | — |\n"

        return heatmap + "\n---\n\n"

    def _find_duplicate_folders(self) -> List[Tuple[str, List[str]]]:
        """Поиск папок с одинаковыми названиями."""
        folder_names = defaultdict(list)

        for doc in self.documents:
            for parent in doc.path.parents:
                if parent == CONTENT_DIR or not parent.is_relative_to(CONTENT_DIR):
                    continue
                # Убираем номер из названия папки
                name = re.sub(r'^\d+\.?\d*\.?\s*', '', parent.name).lower().strip()
                if name:
                    folder_names[name].append(str(parent.relative_to(CONTENT_DIR)))

        duplicates = []
        for name, paths in folder_names.items():
            unique_paths = list(set(paths))
            if len(unique_paths) > 1:
                duplicates.append((name, unique_paths))

        return duplicates

    def _find_duplicate_documents(self) -> List[Tuple[str, List[str], str]]:
        """Поиск документов с одинаковыми названиями."""
        doc_names = defaultdict(list)

        for doc in self.documents:
            # Убираем номер раздела из названия
            name = re.sub(r'\s*\d+\.\d+\.?$', '', doc.name).lower().strip()
            doc_names[name].append(str(doc.relative_path))

        duplicates = []
        for name, paths in doc_names.items():
            if len(paths) > 1:
                # Определяем тип дубля
                dup_type = "exact" if len(set(paths)) == len(paths) else "similar"
                duplicates.append((name, paths, dup_type))

        return duplicates

    def _find_broken_links(self) -> List[Tuple[str, str, str]]:
        """Поиск битых wikilinks."""
        # Собираем все имена документов
        doc_names = {doc.name.lower(): doc.name for doc in self.documents}

        broken = []
        for doc in self.documents:
            for link in doc.wikilinks:
                link_lower = link.lower()
                # Проверяем существование
                if link_lower not in doc_names:
                    # Ищем похожие
                    similar = self._find_similar_name(link, doc_names.values())
                    broken.append((str(doc.relative_path), link, similar or "не найден"))

        return broken[:50]  # Ограничиваем вывод

    def _find_missing_metadata(self) -> List[Tuple[str, List[str]]]:
        """Поиск документов без обязательных метаданных."""
        required_fields = ["type", "status"]

        missing = []
        for doc in self.documents:
            absent = [f for f in required_fields if f not in doc.frontmatter]
            if absent:
                missing.append((str(doc.relative_path), absent))

        return missing[:30]  # Ограничиваем вывод

    def _technical_dup_folders(self, duplicates) -> str:
        section = "## 2. Дублирование названий папок\n\n"

        if not duplicates:
            return section + "*Дублирования не обнаружено* 🟢\n\n---\n\n"

        for i, (name, paths) in enumerate(duplicates[:10], 1):
            section += f"### 2.{i}. [DUP-F{i:03d}] Дублирование «{name}»\n\n"
            section += "**Найдены папки:**\n"
            for path in paths[:5]:
                section += f"- `{path}`\n"
            section += "\n**Рекомендация:** Объединить или переименовать\n\n"

        return section + "---\n\n"

    def _technical_dup_docs(self, duplicates) -> str:
        section = "## 3. Дублирование названий документов\n\n"

        if not duplicates:
            return section + "*Дублирования не обнаружено* 🟢\n\n---\n\n"

        section += "| № | Название | Количество | Пути |\n"
        section += "|---|----------|------------|------|\n"

        for i, (name, paths, dup_type) in enumerate(duplicates[:15], 1):
            paths_str = "; ".join(paths[:3])
            if len(paths) > 3:
                paths_str += f" и ещё {len(paths) - 3}"
            section += f"| {i} | {name[:40]} | {len(paths)} | {paths_str[:60]}... |\n"

        return section + "\n---\n\n"

    def _technical_broken_links(self, broken) -> str:
        section = "## 4. Битые wikilinks\n\n"

        if not broken:
            return section + "*Битых ссылок не обнаружено* 🟢\n\n---\n\n"

        section += "| № | Документ | Ссылка | Рекомендация |\n"
        section += "|---|----------|--------|-------------|\n"

        for i, (doc_path, link, suggestion) in enumerate(broken[:20], 1):
            doc_short = doc_path.split("/")[-1][:30]
            section += f"| {i} | {doc_short} | `[[{link[:30]}]]` | {suggestion[:30]} |\n"

        if len(broken) > 20:
            section += f"\n*... и ещё {len(broken) - 20} битых ссылок*\n"

        return section + "\n---\n\n"

    def _technical_missing_metadata(self, missing) -> str:
        section = "## 5. Документы без обязательных метаданных\n\n"

        if not missing:
            return section + "*Все документы имеют обязательные метаданные* 🟢\n\n---\n\n"

        section += "| № | Документ | Отсутствуют поля |\n"
        section += "|---|----------|------------------|\n"

        for i, (doc_path, fields) in enumerate(missing[:20], 1):
            doc_short = doc_path.split("/")[-1][:40]
            section += f"| {i} | {doc_short} | {', '.join(fields)} |\n"

        if len(missing) > 20:
            section += f"\n*... и ещё {len(missing) - 20} документов*\n"

        return section + "\n---\n\n"

    # ==================== ВСПОМОГАТЕЛЬНЫЕ ОТЧЁТЫ ====================

    def _generate_terminology(self) -> str:
        """Заглушка для отчёта по терминологии."""
        return self._header("Терминологическая согласованность") + \
            "*Этот отчёт требует AI-анализа для сравнения определений терминов.*\n\n" + \
            "Запустите с флагом `--ai-analysis` для полного анализа.\n"

    def _generate_recommendations(self) -> str:
        """Заглушка для отчёта с рекомендациями."""
        return self._header("Рекомендации по развитию") + \
            "*Этот отчёт требует AI-анализа для формирования рекомендаций.*\n\n" + \
            "Запустите с флагом `--ai-analysis` для полного анализа.\n"

    def _generate_links_map(self) -> str:
        """Генерация карты связей между документами."""
        report = self._header("Карта связей между документами")

        # Статистика связей
        total_links = sum(len(d.wikilinks) for d in self.documents)
        docs_with_links = sum(1 for d in self.documents if d.wikilinks)

        report += "## 1. Общая статистика\n\n"
        report += f"- Всего ссылок: {total_links}\n"
        report += f"- Документов со ссылками: {docs_with_links}\n"
        report += f"- Среднее ссылок на документ: {total_links / len(self.documents):.1f}\n\n"

        # Топ документов по входящим ссылкам
        incoming = defaultdict(int)
        for doc in self.documents:
            for link in doc.wikilinks:
                incoming[link.lower()] += 1

        report += "## 2. Топ-10 документов по входящим ссылкам\n\n"
        report += "| № | Документ | Входящих ссылок |\n"
        report += "|---|----------|----------------|\n"

        for i, (name, count) in enumerate(sorted(incoming.items(), key=lambda x: -x[1])[:10], 1):
            report += f"| {i} | {name[:50]} | {count} |\n"

        report += "\n## 3. Изолированные документы (без ссылок)\n\n"
        isolated = [d for d in self.documents if not d.wikilinks]
        report += f"Найдено {len(isolated)} документов без исходящих ссылок.\n\n"

        return report

    # ==================== УТИЛИТЫ ====================

    def _find_doc_by_pattern(self, pattern: str) -> Optional[Document]:
        """Поиск документа по паттерну в названии."""
        regex = re.compile(pattern, re.IGNORECASE)
        for doc in self.documents:
            if regex.search(doc.name):
                return doc
        return None

    def _extract_summary(self, doc: Document, max_sentences: int = 3) -> str:
        """Извлечение краткого резюме из документа."""
        # Убираем заголовки и служебные элементы
        text = re.sub(r'^#.*$', '', doc.body, flags=re.MULTILINE)
        text = re.sub(r'\|.*\|', '', text)  # Убираем таблицы
        text = re.sub(r'```.*?```', '', text, flags=re.DOTALL)  # Убираем код
        text = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', text)  # Убираем ссылки
        text = re.sub(r'\[\[([^\]|]+)(?:\|[^\]]+)?\]\]', r'\1', text)  # Убираем wikilinks

        # Находим предложения
        sentences = re.split(r'(?<=[.!?])\s+', text.strip())
        sentences = [s.strip() for s in sentences if len(s.strip()) > 20]

        return " ".join(sentences[:max_sentences])

    def _extract_first_sentence(self, doc: Document) -> str:
        """Извлечение первого предложения из документа."""
        summary = self._extract_summary(doc, max_sentences=1)
        return summary[:100] if summary else ""

    def _find_similar_name(self, name: str, candidates: List[str], threshold: float = 0.8) -> Optional[str]:
        """Поиск похожего названия (простой алгоритм)."""
        name_lower = name.lower()
        for candidate in candidates:
            candidate_lower = candidate.lower()
            # Простая проверка на вхождение
            if name_lower in candidate_lower or candidate_lower in name_lower:
                return candidate
        return None


def save_report(content: str, filename: str):
    """Сохранение отчёта в файл."""
    output_path = REPORTS_DIR / filename
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(content, encoding="utf-8")
    print(f"✅ Отчёт сохранён: {output_path}")


def main():
    parser = argparse.ArgumentParser(description="Генератор автоматических отчётов")
    parser.add_argument(
        "--report", "-r",
        required=True,
        choices=["architecture-snapshot", "content-completeness", "technical-issues",
                 "terminology", "recommendations", "links-map", "all"],
        help="Тип отчёта для генерации"
    )
    parser.add_argument(
        "--output", "-o",
        help="Путь для сохранения отчёта (по умолчанию: в папку отчётов)"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Только показать отчёт, не сохранять"
    )

    args = parser.parse_args()

    # Проверяем, что запущено из корня проекта
    if not CONTENT_DIR.exists():
        print(f"❌ Папка {CONTENT_DIR} не найдена. Запустите скрипт из корня проекта.")
        sys.exit(1)

    generator = ReportGenerator()
    generator.scan_documents()

    report_files = {
        "architecture-snapshot": "Архитектурный слепок хранилища 0.4.md",
        "content-completeness": "Содержательная полнота описания 0.4.md",
        "technical-issues": "Противоречия и несогласованности 0.4.md",
        "terminology": "Терминологическая согласованность 0.4.md",
        "recommendations": "Рекомендации по развитию 0.4.md",
        "links-map": "Карта связей между документами 0.4.md",
    }

    if args.report == "all":
        reports_to_generate = list(report_files.keys())
    else:
        reports_to_generate = [args.report]

    for report_type in reports_to_generate:
        print(f"\n📝 Генерация отчёта: {report_type}")

        try:
            content = generator.generate(report_type)

            if args.dry_run:
                print("\n" + "=" * 60)
                print(content[:2000])
                print("..." if len(content) > 2000 else "")
                print("=" * 60)
            else:
                filename = args.output if args.output and args.report != "all" else report_files[report_type]
                save_report(content, filename)

        except Exception as e:
            print(f"❌ Ошибка при генерации {report_type}: {e}")
            import traceback
            traceback.print_exc()

    print("\n✅ Готово!")


if __name__ == "__main__":
    main()
