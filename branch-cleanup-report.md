# Отчёт по очистке веток

**Дата:** 2025-12-30

## Результаты анализа

| Категория | Количество | Статус |
|-----------|------------|--------|
| Локальные смерженные | 1 | ✅ Удалена |
| Удалённые смерженные | 24 | ⏳ Требуют удаления |
| Устаревшие несмерженные | 12 | ⏳ Требуют удаления |
| Активные несмерженные | 3 | 🔒 Оставить |

## Выполненные действия

### Удалённые локальные ветки
- `claude/ai-personalized-recommendations-4o1lh` — смержена в main

---

## Ветки для удаления (требуют прав)

### 1. Смерженные удалённые ветки (24 шт.)

Эти ветки уже полностью интегрированы в main:

```bash
git push origin --delete \
  claude/add-methodology-docs-pKLkG \
  claude/add-outbound-procedure-docs-ZC0E9 \
  claude/clarify-guide-object-ids-KNS3e \
  claude/document-repo-structure-rdfNH \
  claude/homework-checker-docs-QqANG \
  claude/improve-docs-structure-W1enF \
  claude/mcp-architecture-doc-ZhPBe \
  claude/openai-apps-sdk-ui-WjzwX \
  claude/reorganize-docs-PsyXb \
  claude/repo-structure-guides-ZUZHk \
  claude/restructure-folders-mbMYz \
  claude/restructure-guide-folder-pq7hW \
  claude/revert-and-add-indexes-VuamE \
  claude/review-checker-docs-oa95U \
  claude/review-checker-logic-LN5M5 \
  claude/revise-2025-summary-575CF \
  claude/rewrite-mcp-integration-docs-sgeHE \
  claude/update-checker-docs-2ZRAs \
  claude/update-ecosystem-docs-igp6E \
  claude/update-fsm-docs-HnMti \
  claude/update-guide-structure-1Xhjr \
  claude/update-homework-checker-mvp-X8AVC \
  claude/update-repo-structure-guide-niUW2 \
  claude/update-work-plan-YsApN
```

### 2. Устаревшие несмерженные ветки (12 шт.)

Эти ветки отстают от main на 203+ коммитов и не содержат уникальных изменений:

| Ветка | Отставание | Последнее изменение |
|-------|------------|---------------------|
| claude/add-document-purpose-table-4s1KP | 203 | 2025-12-20 |
| claude/add-fpf-compliance-checks-s7NQZ | 203 | 2025-12-20 |
| claude/add-llm-interface-2hms3 | 203 | 2025-12-20 |
| claude/document-code-workflow-LZXPa | 203 | 2025-12-19 |
| claude/github-structure-presentation-Y6mOe | 203 | 2025-12-20 |
| claude/homework-checker-system-tNY5s | 203 | 2025-12-22 |
| claude/improve-mcp-diagram-8OkMY | 203 | 2025-12-22 |
| claude/integrate-assistant-sdk-BQCpc | 203 | 2025-12-23 |
| claude/move-llm-sdk-file-JIqqF | 203 | 2025-12-21 |
| claude/openai-apps-sdk-integration-cZ2ju | 203 | 2025-12-21 |
| claude/route-guide-digital-twin-xghd2 | 203 | 2025-12-20 |
| claude/update-contributing-guide-cTY8q | 203 | 2025-12-20 |

```bash
git push origin --delete \
  claude/add-document-purpose-table-4s1KP \
  claude/add-fpf-compliance-checks-s7NQZ \
  claude/add-llm-interface-2hms3 \
  claude/document-code-workflow-LZXPa \
  claude/github-structure-presentation-Y6mOe \
  claude/homework-checker-system-tNY5s \
  claude/improve-mcp-diagram-8OkMY \
  claude/integrate-assistant-sdk-BQCpc \
  claude/move-llm-sdk-file-JIqqF \
  claude/openai-apps-sdk-integration-cZ2ju \
  claude/route-guide-digital-twin-xghd2 \
  claude/update-contributing-guide-cTY8q
```

---

## Ветки для сохранения (3 шт.)

| Ветка | Отставание | Причина |
|-------|------------|---------|
| claude/ai-personalized-recommendations-4o1lh | 3 | Активная работа |
| claude/analyze-ai-topics-qqYUT | 81 | Уникальные изменения |
| claude/remove-outdated-branches-HPqgM | 63 | Отчёт по очистке |

---

## Сводная команда для полной очистки

```bash
# Все 36 веток одной командой:
git push origin --delete \
  claude/add-methodology-docs-pKLkG \
  claude/add-outbound-procedure-docs-ZC0E9 \
  claude/clarify-guide-object-ids-KNS3e \
  claude/document-repo-structure-rdfNH \
  claude/homework-checker-docs-QqANG \
  claude/improve-docs-structure-W1enF \
  claude/mcp-architecture-doc-ZhPBe \
  claude/openai-apps-sdk-ui-WjzwX \
  claude/reorganize-docs-PsyXb \
  claude/repo-structure-guides-ZUZHk \
  claude/restructure-folders-mbMYz \
  claude/restructure-guide-folder-pq7hW \
  claude/revert-and-add-indexes-VuamE \
  claude/review-checker-docs-oa95U \
  claude/review-checker-logic-LN5M5 \
  claude/revise-2025-summary-575CF \
  claude/rewrite-mcp-integration-docs-sgeHE \
  claude/update-checker-docs-2ZRAs \
  claude/update-ecosystem-docs-igp6E \
  claude/update-fsm-docs-HnMti \
  claude/update-guide-structure-1Xhjr \
  claude/update-homework-checker-mvp-X8AVC \
  claude/update-repo-structure-guide-niUW2 \
  claude/update-work-plan-YsApN \
  claude/add-document-purpose-table-4s1KP \
  claude/add-fpf-compliance-checks-s7NQZ \
  claude/add-llm-interface-2hms3 \
  claude/document-code-workflow-LZXPa \
  claude/github-structure-presentation-Y6mOe \
  claude/homework-checker-system-tNY5s \
  claude/improve-mcp-diagram-8OkMY \
  claude/integrate-assistant-sdk-BQCpc \
  claude/move-llm-sdk-file-JIqqF \
  claude/openai-apps-sdk-integration-cZ2ju \
  claude/route-guide-digital-twin-xghd2 \
  claude/update-contributing-guide-cTY8q
```

## Примечание

Удаление требует прав администратора репозитория. Выполните команды выше с соответствующим доступом или через GitHub UI:
**Settings → Branches → Delete stale branches**
