---
title: "MCP-серверы для руководств 3.2"
family: F8
cell: "3.2"
status: active
updated: 2025-12-16
links:
  - path: "content/3. Экосистема развития (Система создания)/3.2. Архитектура — Платформа и подсистемы/3.2.3. Детерминированные ИТ-системы/3.2.3.1. Цифровой двойник/MCP-сервер цифрового двойника 3.2.md"
    note: "MCP Twin — взаимодействие с персональными данными"
  - path: "content/3. Экосистема развития (Система создания)/3.2. Архитектура — Платформа и подсистемы/3.2.3. Детерминированные ИТ-системы/Централизованное хранилище 3.2.md"
    note: "Артефакты и индексы руководств"
---

Ниже — набор архитектурных вариантов **MCP-серверов для руководств** (универсальных и персональных) + перечень функций (tools/resources) и рекомендуемый контур «ежедневное задание» на стыке **руководств** и **цифрового двойника**.

---

## 1) Разделение на два MCP-сервера (минимальный “правильный” контур)

### A. MCP-сервер универсальных руководств (GuideRepo MCP)

**Назначение:** дать агентам быстрый, версионированный доступ к содержимому руководств, которые лежат в Git (разделы/подразделы, поиск, ссылки, концепты).

### B. MCP-сервер персональных руководств (PersonalGuide MCP)

**Назначение:** на основе (1) структуры универсального руководства, (2) данных цифрового двойника, (3) прогресса обучения — **выдавать ежедневные задания** и «пакеты контекста» для персонализированного текста.

Практически полезно держать их раздельно: универсальный сервер — почти всегда **read-only**, персональный — **stateful** (прогресс, планы, очереди повторения).

---

## 2) Универсальные руководства: варианты реализации (в порядке усложнения)

### Вариант U1 — “Git-файлы как источник истины” (самый простой)
- Сервер читает Markdown по `path + ref` (ветка/тег/SHA).    
- Умеет парсить заголовки, извлекать секции, делать простой поиск (grep/regex).    
- Подходит, если руководств немного и нагрузка невысокая.    

### Вариант U2 — “Синхронизация + индексация” (рекомендованный по умолчанию)
- Периодически или по webhook подтягивает изменения из Git.    
- Строит:    
    - **TOC/anchors** (структура по заголовкам),        
    - **инвертированный индекс** (быстрый полнотекст),        
    - **векторный индекс** (семантический поиск по чанкам).        
- Дает стабильные `section_id` и быстрый `search_semantic`.    

### Вариант U3 — “Компиляция руководств в артефакты” (лучший для масштабирования)
- В CI вы «собираете» руководства в единый артефакт: `toc.json`, `concept_graph.json`, `chunks.jsonl`.    
- MCP-сервер только сервит артефакты (быстро, предсказуемо, одинаково везде).    
- Плюс: легко гарантировать воспроизводимость (версия = commit SHA).    

### Вариант U4 — “Прокси поверх готового GitHub MCP”
- Если вы уже используете GitHub-MCP (или аналог), то GuideRepo MCP может стать тонким слоем: «получить markdown → распарсить → отдать section/chunks».    
- Удобно для быстрого старта, но обычно хуже по latency и контролю индексации.    

---

## 3) Универсальные руководства: рекомендуемый набор MCP-функций

### Resources (чтение контента)
- `guide://universal/{guide_id}@{ref}/toc`    
- `guide://universal/{guide_id}@{ref}/section/{section_id}`    
- `guide://universal/{guide_id}@{ref}/chunk/{chunk_id}`    

### Tools (операции)
1. `guides.list_guides(ref?) -> [{guide_id, title, ref, updated_at}]`  
2. `guides.get_toc(guide_id, ref?) -> toc_tree`    
3. `guides.get_section(guide_id, section_id, ref?, format=md|text|ast, include_subsections?) -> {content, anchors, concepts}`    
4. `guides.resolve_anchor(guide_id, anchor, ref?) -> {section_id, offset}`    
5. `guides.search_text(query, guide_id?, ref?, filters?) -> hits[]`    
6. `guides.search_semantic(query, guide_id?, ref?, top_k, filters?) -> hits[]`    
7. `guides.get_concept_graph(guide_id, ref?) -> graph` (если есть концепты/пререквизиты)    

---

## 4) Персональные руководства: что именно должен уметь MCP-сервер
Здесь важно разделить:
- **планирование обучения** (что делать дальше),    
- **персонализацию изложения** (как объяснить именно этому человеку),    
- **учет прогресса и повторения**.    

### Почему это работает (опора на доказательные эффекты)

- **Распределенная практика (spaced practice)** статистически надежно улучшает удержание знаний. ([Ovid](https://www.ovid.com/journals/plbul/abstract/00006823-200605000-00002~distributed-practice-in-verbal-recall-tasks-a-review-and?utm_source=chatgpt.com "Distributed Practice in Verbal Recall Tasks : Psychological Bulletin"))    
- **Practice testing / testing effect** (вытаскивание из памяти) повышает долговременное запоминание лучше, чем повторное перечитывание при сопоставимых затратах времени. ([CoLab](https://colab.ws/articles/10.1111%2Fj.1467-9280.2006.01693.x?utm_source=chatgpt.com "Test-Enhanced Learning | CoLab"))    
- Обзоры по учебным техникам выделяют practice testing и distributed practice как одни из наиболее полезных в широком спектре условий. ([Scholars@Duke](https://scholars.duke.edu/individual/pub954654?utm_source=chatgpt.com "Scholars@Duke publication: Improving Students' Learning With Effective Learning Techniques: Promising Directions From Cognitive and Educational Psychology."))    
- Логика **mastery learning** (не гнать дальше без освоения) — классическая и хорошо описанная рамка для адаптивного обучения. ([ERIC](https://files.eric.ed.gov/fulltext/ED037405.pdf?utm_source=chatgpt.com "DOCUMENT RESUME"))    
- Для учета освоения по шагам (skills/концептам) применяют модели knowledge tracing / BKT как основу адаптивной выдачи заданий. ([Researchr](https://researchr.org/publication/CorbettA95%3A0/bibtex?utm_source=chatgpt.com "Knowledge Tracing: Modelling the Acquisition of Procedural Knowledge - researchr publication bibtex"))    

---

## 5) Персональные руководства: варианты реализации

### Вариант P1 — “Планировщик + пакет контекста” (самый управляемый)
PersonalGuide MCP **не генерирует** финальный учебный текст, а отдает агенту:
- выбранные `concept_ids/section_ids`,    
- «что повторить» (spacing queue),    
- параметры персонализации (стиль/сложность/доменные примеры),    
- список релевантных чанков из универсального руководства,    
- формат задания и критерии.   

Финальный текст формирует ваш LLM-агент (R.GrowthGuide / Tutor), что проще контролировать и улучшать.

### Вариант P2 — “Сервер-рендерер” (максимум автоматизации)

PersonalGuide MCP сам генерирует персонализированный учебный текст (встроенный LLM вызов).  
Плюсы: единый API “дай задание”. Минусы: сложнее наблюдаемость, версионирование промптов, стоимость, отладка.

### Вариант P3 — “Гибрид: шаблон + вариативные вставки”

- Тело объяснения — по шаблону.    
- Вставки (примеры, аналогии, задачи) — выбираются/генерируются под человека.  
    Хорошо, если вы хотите единый стиль руководства и контролируемую сложность.    

---

## 6) Персональные руководства: функции MCP (то, что вы просили “для ежедневного задания”)

### Входные данные (интеграция с цифровым двойником)
- `twin.get_state(user_id, date?)` — режим, доступное время, контекст, ограничения    
- `twin.get_activity(user_id, range)` — факты: слоты, выполненные задания    
- `twin.get_profile(user_id)` — сфера деятельности, стиль, уровень, цели   

(Если ваш Twin MCP уже существует — PersonalGuide MCP просто вызывает его tools.)

### Ключевые tools PersonalGuide MCP
1. `learning.get_mastery(user_id, guide_id) -> mastery_map`    
    - по концептам/разделам: `p_mastery`, ошибки, давность, уверенность (можно heuristics → потом BKT).        
2. `learning.get_review_queue(user_id, date) -> [concept_id...]`    
    - очередь повторения по spaced practice. ([Ovid](https://www.ovid.com/journals/plbul/abstract/00006823-200605000-00002~distributed-practice-in-verbal-recall-tasks-a-review-and?utm_source=chatgpt.com "Distributed Practice in Verbal Recall Tasks : Psychological Bulletin"))        
3. `curriculum.next_concepts(user_id, guide_id, date, constraints) -> {new:[], review:[], rationale}`    
    - выбирает «что новое» + «что повторить» с учетом пререквизитов, мастерства, времени.        
4. `assignment.build_daily(user_id, guide_id, date, constraints) -> DailyAssignment`  
    **DailyAssignment (пример схемы):**    
    - `objective` (1–2 учебные цели)        
    - `reading_sections[]` (section_id + почему)        
    - `practice[]` (retrieval questions / мини-кейс / моделирование)        
    - `expected_artifacts[]` (заметка, модель, чек-лист и т.п.)        
    - `time_budget_minutes`        
    - `success_criteria`        
    - `personalization_pack` (тон, сложность, доменные примеры, терминология)        
5. `personalization.get_pack(user_id) -> {domain, style, level, forbidden_examples, preferred_formats}`    
6. `progress.record(user_id, assignment_id, outcomes, artifacts_meta)`  
    - фиксация факта выполнения и сигналов качества.        
7. (опционально) `content.get_context_chunks(guide_id, section_ids, top_k) -> chunks[]`    
    - чтобы агент не делал повторный поиск.        

---

## 7) Типовой workflow “выдать задание на день”
1. Агент вызывает `twin.get_state` / `twin.get_profile` / `learning.get_mastery`.    
2. PersonalGuide MCP делает `curriculum.next_concepts` + `learning.get_review_queue`.    
3. Собирает `assignment.build_daily`:    
    - часть времени — **повторение** (distributed practice),        
    - часть — **извлечение** (practice testing),        
    - часть — **новый материал** (1 небольшой шаг). ([Scholars@Duke](https://scholars.duke.edu/individual/pub954654?utm_source=chatgpt.com "Scholars@Duke publication: Improving Students' Learning With Effective Learning Techniques: Promising Directions From Cognitive and Educational Psychology."))        
4. Агент рендерит человеку персонализированное объяснение (примеры из его деятельности, нужный стиль/сложность).    
5. После ответа пользователя агент/оценщик пишет результат через `progress.record`, обновляя “мастерство”.    

---

## 8) Практическая рекомендация “что делать первым”
Если вам нужно быстро запуститься без риска:
1. **U2 (синхронизация + индексы)** для универсальных руководств.    
2. **P1 (планировщик + пакет контекста)** для персональных (генерация — в агенте).    

Это даст максимальную управляемость и позволит дальше усложнять (BKT/knowledge tracing, richer concept graph, более умная персонализация) без переделки основы. ([Researchr](https://researchr.org/publication/CorbettA95%3A0/bibtex?utm_source=chatgpt.com "Knowledge Tracing: Modelling the Acquisition of Procedural Knowledge - researchr publication bibtex"))