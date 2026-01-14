---
# === БАЗОВЫЕ МЕТАДАННЫЕ ===
type: doc
family: F5                    # F1-F9 по матрице ролей
cell: "X.X.X"                 # Номер ячейки в хранилище
status: stub                  # stub | draft | active | deprecated
created: 2025-12-19
modified: 2025-12-19

# === FPF: TRUST CALCULUS (B.3) ===
trust:
  F: 2                        # Formality: 0-9 (0=скетч, 9=формальное доказательство)
  G: "local-edge"             # ClaimScope: где применимо (universal | domain | local-edge)
  R: 0.5                      # Reliability: 0.0-1.0 (уверенность в утверждениях)

# === FPF: EPISTEMIC STAGE (B.5.1) ===
epistemic_stage: explore      # explore | shape | evidence | operate

# === FPF: EVIDENCE GRAPH (A.10) ===
depends_on:                   # От каких документов зависит
  - "Родительский документ"
provides_evidence_for:        # Для каких документов является evidence
  - "Целевой документ"

# === КОНТЕКСТ (A.1.1 Bounded Context) ===
developer_role: Методолог     # Кто разрабатывает
target_audience:              # Для кого предназначен
  - Методологи
  - Наставники
layer: architecture           # methodology | architecture | operations
scope: local-edge             # universal | domain | local-edge
aliases:                      # Альтернативные названия
  - альтернативное имя
---


# Название документа

## 0. Назначение документа

Краткое описание назначения документа (1-2 предложения).

---

## 1. Основное содержание

> Основной контент документа

---

## 2. Связанные документы

- [[Связанный документ 1]]
- [[Связанный документ 2]]

---

## Changelog

| Дата       | Версия | Автор  | Изменения                         |
|------------|--------|--------|-----------------------------------|
| 2025-12-19 | v0.1   | —      | Создание документа                |
