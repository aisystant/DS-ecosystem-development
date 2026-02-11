# Инструкция для Windows PowerShell

> **Для пользователей Windows**: Используйте команды из этого файла!
> **Для пользователей Linux/WSL**: Используйте `USAGE.md`

---

## 📍 ГДЕ запускать

**ВСЕГДА** из корневой директории проекта в PowerShell:

```powershell
# ✅ ПРАВИЛЬНО
cd C:\DS-ecosystem-development
python ops\classify_documents.py
python ops\save_manual_edits.py
python ops\validate_classifications.py
```

```powershell
# ❌ НЕПРАВИЛЬНО
cd C:\DS-ecosystem-development\ops
python classify_documents.py  # Не сработает!
```

⚠️ **ВАЖНО:** Используйте `python` (не `python3`!) и обратные слеши `\` (не `/`)

---

## 🔄 Полный workflow

### 1️⃣ Первый запуск (AI классификация)

```powershell
cd C:\DS-ecosystem-development
python ops\classify_documents.py
```

**Результат:** Таблица в документе 0.6 заполнена желтыми (AI) предложениями

---

### 2️⃣ Ручная правка

1. Откройте `C:\DS-ecosystem-development\content\0. Управление\0.6. Структура этого хранилища.md` в Obsidian
2. Найдите документ, который хотите отредактировать
3. **ВАЖНО:** Уберите **ВСЕ** теги `<mark>...</mark>` в строке

**Пример:**

Было (AI-предложение):
```markdown
| 5 | test.md | folder | <mark>doc</mark> | <mark>manual</mark> | <mark>mixed</mark> | ...
```

Стало (ручная правка - все теги убраны):
```markdown
| 5 | test.md | folder | doc | manual | mixed | methodology | global-core | public |
```

4. Сохраните файл (Ctrl+S в Obsidian)

---

### 3️⃣ Сохранение ручных правок (желтое → зеленое)

```powershell
cd C:\DS-ecosystem-development
python ops\save_manual_edits.py
```

**Результат:**
- Создан/обновлен файл `ops\manual_classifications.json`
- Отредактированные строки сохранены

---

### 4️⃣ Повторная классификация (проверка защиты)

```powershell
cd C:\DS-ecosystem-development
python ops\classify_documents.py
```

**Результат:**
- Новые документы получат желтые (AI) предложения
- Сохраненные правки станут ЗЕЛЕНЫМИ
- **AI НЕ ИЗМЕНИТ зеленые значения**

---

### 5️⃣ Проверка валидности

```powershell
cd C:\DS-ecosystem-development
python ops\validate_classifications.py
```

**Результат:** Проверка что все значения соответствуют допустимым из документа 0.7

---

## ⚠️ Частые ошибки в Windows

### Ошибка 1: Используется `python3` вместо `python`

```powershell
PS C:\DS-ecosystem-development> python3 ops\classify_documents.py
Python  # ← Открывается интерпретатор, а не запускается скрипт!
```

**Причина:** В Windows команда называется `python`, не `python3`

**Решение:**
```powershell
python ops\classify_documents.py
```

Или попробуйте:
```powershell
py ops\classify_documents.py
```

---

### Ошибка 2: Используются Linux пути

```powershell
PS C:\DS-ecosystem-development> cd /mnt/c/DS-ecosystem-development
Cannot find path 'C:\mnt\c\DS-ecosystem-development' because it does not exist.
```

**Причина:** `/mnt/c/` - это путь для WSL (Linux), не для PowerShell

**Решение:** Используйте Windows пути:
```powershell
cd C:\DS-ecosystem-development
```

---

### Ошибка 3: "Документ не найден"

```powershell
❌ Документ не найден: C:\DS-ecosystem-development\content\0. Управление\0.6...
```

**Причина:** Скрипт запущен не из корневой директории

**Решение:**
```powershell
# Проверьте где вы находитесь:
pwd

# Должно быть: C:\DS-ecosystem-development

# Если нет - перейдите в корень:
cd C:\DS-ecosystem-development
python ops\save_manual_edits.py
```

---

### Ошибка 4: "Ручных правок: 0"

```powershell
📊 Статистика:
  ✅ Ручных правок (зеленые): 0
  🤖 AI-предложений (желтые): 39
```

**Причина:** В таблице нет строк, где **ВСЕ** значения без `<mark>` тегов

**Решение:** Убедитесь, что в строке убраны **ВСЕ 6** тегов `<mark>`:
- Type
- Audience
- Edit Mode
- Layer
- Scope
- Security

---

### Ошибка 5: Python не установлен

```powershell
PS C:\DS-ecosystem-development> python ops\classify_documents.py
python : The term 'python' is not recognized...
```

**Решение 1:** Попробуйте команду `py`:
```powershell
py ops\classify_documents.py
```

**Решение 2:** Установите Python:
1. Скачайте с https://www.python.org/downloads/
2. При установке отметьте "Add Python to PATH"
3. Перезапустите PowerShell

---

## 🎯 Проверка текущего состояния

### Проверить версию Python:

```powershell
python --version
# или
py --version
```

### Сколько ручных правок сохранено?

```powershell
Get-Content ops\manual_classifications.json
```

### Проверить валидность:

```powershell
python ops\validate_classifications.py
```

---

## 💡 Полезные команды PowerShell

### Показать текущую директорию:

```powershell
pwd
```

### Перейти в корень проекта:

```powershell
cd C:\DS-ecosystem-development
```

### Открыть папку в проводнике:

```powershell
explorer .
```

### Открыть файл в Notepad:

```powershell
notepad "content\0. Управление\0.6. Структура этого хранилища.md"
```

### Сбросить все ручные правки (вернуть к AI):

```powershell
# ВНИМАНИЕ: Это удалит ВСЕ сохраненные правки!
Remove-Item ops\manual_classifications.json
python ops\classify_documents.py
```

### Резервная копия ручных правок:

```powershell
Copy-Item ops\manual_classifications.json ops\manual_classifications.backup.json
```

### Восстановить из резервной копии:

```powershell
Copy-Item ops\manual_classifications.backup.json ops\manual_classifications.json
```

---

## 🆚 Windows vs WSL (Linux)

Если у вас установлен WSL (Windows Subsystem for Linux), вы можете использовать Linux команды:

### Запуск в WSL bash:

```bash
# Открыть WSL:
wsl

# В WSL используйте Linux пути:
cd /mnt/c/DS-ecosystem-development
python3 .ops/classify_documents.py
```

### Запуск в PowerShell (Windows):

```powershell
# В PowerShell используйте Windows пути:
cd C:\DS-ecosystem-development
python ops\classify_documents.py
```

**Рекомендация:** Используйте **один** способ постоянно (или WSL, или PowerShell), чтобы избежать путаницы.

---

## 📞 Нужна помощь?

- **Linux/WSL инструкция:** `ops\USAGE.md`
- **Полная документация:** `ops\README_CLASSIFICATION.md`
- **Windows проблемы:** Проверьте что Python установлен и добавлен в PATH

---

## 🚀 Быстрый старт для нетерпеливых

Если вы просто хотите запустить классификацию прямо сейчас:

```powershell
# 1. Откройте PowerShell
# 2. Скопируйте и выполните эти команды:

cd C:\DS-ecosystem-development
python ops\classify_documents.py

# 3. Откройте результат в Obsidian:
# content\0. Управление\0.6. Структура этого хранилища.md

# 4. Проверьте валидность:
python ops\validate_classifications.py
```

Готово! 🎉
