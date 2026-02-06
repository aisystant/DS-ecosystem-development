# CLAUDE.md — Ecosystem Development

> **Общие инструкции:** см. `/Users/tserentserenov/Github/CLAUDE.md`
>
> Этот файл содержит только специфику данного репозитория.

---

## 1. Тип репозитория

**Downstream-governance** — управленческая сборка экосистемы, оформленная по S2R.

**НЕ является source-of-truth** — знания берутся из Pack'ов.

---

## 2. Структура ядер (S2R)

```
ecosystem-development/
├── 0.OPS/                    # F0: Метауровень
│   ├── 0.1.Knowledge-Logic/  # Модель ядер, семейства, глоссарий
│   ├── 0.2.Kernels-Bridge/   # Связи между ядрами
│   ├── 0.3.Roles-Matrix-3x3/ # Матрица ролей
│   ├── 0.4.FPF-Integration/  # Интеграция с FPF
│   ├── 0.5.AI-Reports/       # Отчёты ИИ
│   ├── 0.6.Repository-Processes/
│   ├── 0.7.Plans-and-Meetings/
│   └── 0.99.Archive/
├── A.Systems-Builder/        # Ядро A: SoI = Созидатель
├── B.Aisystant-Ecosystem/    # Ядро B: SoI = Экосистема
└── C.IT-Platform/            # Ядро C: SoI = ИТ-платформа
```

---

## 3. Матрица 3×3

Каждое ядро содержит 9 семейств документов (F1-F9):

| Роль ↓ / Система → | Надсистема (X1) | SoI (X2) | Создание (X3) |
|--------------------|-----------------|----------|---------------|
| **Meaning (.1.)** | F1 | F2 | F3 |
| **Architecture (.2.)** | F4 | F5 | F6 |
| **Operations (.3.)** | F7 | F8 | F9 |

---

## 4. Правила работы

### 4.1. Ops-First Rule

**При изменениях в репозитории ВСЕГДА загружай документы из 0.OPS/ ПЕРВЫМИ.**

Priority Queue:
1. `01-kernels-model.md` — структура ядер
2. `02-document-families.md` — семейства F1-F9
3. `07-naming.md` — правила именования
4. `05-glossary.md` — терминология

### 4.2. Правило нумерации X1/X2/X3

```
X1 = Надсистема (физическая вложенность)
X2 = SoI (система интереса)
X3 = Система создания
```

**НЕЛЬЗЯ** менять нумерацию в зависимости от контекста.

### 4.3. Система ≠ Эпистема

**Ядро** — только для систем (физических сущностей).

**ЗАПРЕЩЕНО:** Ядра по эпистемам (`E.Экономика/`, `G.Продвижение/`).

### 4.4. Иерархия источников знаний (Fallback Chain)

Этот репозиторий — **Downstream**. Источники знаний по приоритету:

```
1. Pack'и (source-of-truth)
   └── spf-ecosystem-pack, spf-digital-platform-pack
2. SPF (форма и процесс)
   └── ~/Github/SPF/
3. FPF (первые принципы) — только если нет в SPF
   └── ~/Github/FPF/FPF-Spec.md
```

**Правило:** Если чего-то нет на текущем уровне — смотри выше.

**Когда читать FPF напрямую:**
- Только если вопрос не покрыт в SPF
- Для понимания базовых различений (A.7, A.1.1)

**Документация интеграции S2R↔FPF:** `0.OPS/0.4.FPF-Integration/`

---

## 5. Создание документа

### 5.1. Алгоритм

1. Определи ЯДРО (A/B/C)
2. Определи СЕМЕЙСТВО (F1-F9)
3. Прочитай `0.OPS/0.6.Repository-Processes/02-standards.md`
4. Создай документ с frontmatter

### 5.2. Frontmatter

```yaml
---
family: F5
kernel: A
system: A2
role: Architecture
status: draft
target_audience:
  - "Наставники"
depends_on: []
---
```

### 5.3. Именование файлов

Format: `<номер>-<название>.md`

- ✅ `01-mission-statement.md`
- ❌ `1-mission.md` (нет ведущего нуля)
- ❌ `Mission Statement.md` (пробелы)

---

## 6. Чеклисты

### Перед созданием документа

- [ ] Загружен `01-kernels-model.md`
- [ ] Загружен `02-document-families.md`
- [ ] Определено ядро (A/B/C)
- [ ] Определена система (X1/X2/X3)
- [ ] Определена роль (Meaning/Architecture/Operations)
- [ ] Frontmatter заполнен

### После изменений структуры

- [ ] Обновлён `03-structure.md`
- [ ] Обновлён `03-our-systems-map.md`
- [ ] Проверены ссылки

---

## 7. Ключевые документы

| Тема | Путь |
|------|------|
| Модель ядер | `0.OPS/0.1.Knowledge-Logic/01-kernels-model.md` |
| Семейства | `0.OPS/0.1.Knowledge-Logic/02-document-families.md` |
| Глоссарий | `0.OPS/0.1.Knowledge-Logic/05-glossary.md` |
| Реестр репо | `0.OPS/REPOSITORY-REGISTRY.md` |
| Матрица ролей | `0.OPS/0.3.Roles-Matrix-3x3/roles-matrix.md` |
