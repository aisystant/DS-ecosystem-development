# LMS Aisystant — API Reference

> **Источник:** Google Doc (внутренняя документация LMS-команды), сохранено 2026-03-17
> **Владелец API:** LMS-команда (Aisystant)
> **Статус:** актуальное, используется в production

---

## Серверы

| Окружение | URL |
|-----------|-----|
| Тест | `http://188.73.162.175:8064/systemschool/api/` |
| Тест (альт.) | `http://188.73.162.175/systemschool/api/` |
| Прод | `https://aisystant.system-school.ru/api/` |

---

## Аутентификация

При любом обращении к бэку (даже без авторизации) генерируется кука `jsessionid`, если есть `rememberMe` — то ещё и кука `session-token`.

### Auth

#### Login
```
POST /auth/login
{
  "user": "$user",
  "password": "$password",
  "rememberMe": true
}
```

#### Logout
```
POST /auth/logout
```

#### New (регистрация)
```
POST /auth/new
{
  "email": "$email",
  "password": "$password",
  "lastName": "$lastName",
  "firstName": "$firstName",
  "rememberMe": true,
  "server": "$server"
}
```

#### Reset password
Шлёт на почту пользователю ссылку для восстановления пароля.
```
POST /auth/reset-password
{ "email": "$email" }
```

#### Change password (по ссылке)
```
POST /auth/change-password
{ "link": "$link", "password": "$password" }
```

#### Check link
```
GET /auth/check-link?link=$link
→ { "type": "reset-password" }
```

#### Request confirm email
```
POST /auth/request-confirm-email
```

#### Confirm email
```
POST /auth/confirm-email
{ "link": "$link" }
```

---

## Profile

#### Info
С профилем также возвращается `sessionToken` для авторизации.
```
GET /profile/info
```

#### Qualification level
```
GET /profile/qualification-level
```

#### Update
```
POST /profile/update
{ "firstName": "$firstName", "lastName": "$lastName" }
```

#### Change password
```
POST /profile/change-password
{ "password": "$password" }
```

#### Check contact
```
POST /profile/check-contact?contact=$email
→ { "registered": true }
```

#### Metrics
```
POST /profile/metrics?metric-id=$metricId
```

#### Get attributes
`attribute` — необязательный параметр.
```
GET /profile/attributes?attribute=$attribute
→ { "$attribute1": $value1, "$attribute2": $value2 }
```

#### Set attributes
```
POST /profile/attributes
{ "$attribute": $value }
```

#### Find by telegram id
`signature = DigestUtils.sha256Hex(tgId + "+" + LocalDate.now().getYear())`
```
GET /profile/find-by-tg?tg-id=$telegramId&s=$signature
→ { "id": $userId }
```

#### New telegram link
Создать ссылку для привязки telegramId к пользователю.
```
POST /profile/new-tg-link?tg-id=$telegramId&tg-username=$telegramUsername
→ { "path": $path }
```

#### Follow telegram link
Привязать telegramId к пользователю (авторизованному) по ссылке. ID сохраняется в атрибут `tgId`; username — в `tgUsername`.
```
POST /profile/follow-tg-link?path=$path
→ { "attached": true/false }
```

---

## Subscriptions

> Во все запросы (кроме редактирования тарифов), если они выполняются под ролью администратора, можно добавить `user-id=$userId` — запрос отработает от имени указанного userId.
> Параметр `purpose=$purpose`: SUBSCRIPTION (по умолчанию) | DONATION | WORKSHOP.

#### Active tariffs (без авторизации)
```
GET /subscriptions/active-tariffs
```

#### Active subscription
```
GET /subscriptions/active-subscription
```

#### Disable autopay
```
POST /subscriptions/disable-autopay?subscription-id=$subscriptionId
```

#### Create subscription payment
`requestId` — GUID, уникальный для каждого платежа. `code` — код тарифа; `amount` — сумма в рублях; `locale` — ru/en; `autopay` — true/false; `paymentSystem` — yoo/paybox/stripe (default: yoo); `currency` — RUB/EUR (default: RUB).
```
POST /subscriptions/create-subscription-payment?request-id=$requestId
{
  "code": "$code",
  "amount": "$amount",
  "locale": "$locale",
  "autopay": "$autopay",
  "paymentSystem": "$paymentSystem",
  "currency": "$currency"
}
→ { "confirmationUrl": "$confirmationUrl", "id": "$id" }
```

#### Check payment
Пока результат IN_PROGRESS, вызывать не чаще раз в 5 секунд.
```
POST /subscriptions/check-payment?id=$id
→ { "paymentCheckResult": "SUCCEEDED | FAILED | IN_PROGRESS" }
```

#### Payments (список)
```
GET /subscriptions/payments
```

#### Auto pay details
```
GET /subscriptions/auto-pay-details
```

#### Subscriptions (все, включая старые)
```
GET /subscriptions/subscriptions
```

#### Increase amounts (повышение тарифов)
`periodicity` — m, 3m, 6m, y, 2y; `delta` — сумма повышения за 1 месяц.
```
POST /subscriptions/increase-amounts
{
  "tariffPeriodAmountDeltas": {
    "$periodicity1": $delta1,
    "$periodicity2": $delta2
  }
}
```

---

## Courses

#### Courses (список)
`online` — необязательный фильтр (false = только очные). `add-versions` — добавить список версий.
```
GET /courses/courses?online=false&add-versions=true
```

#### Course versions
`course-path` — необязательный фильтр. `online` — необязательный фильтр.
```
GET /courses/course-versions?course-path=$coursePath&online=false
```

#### Course version (по id)
```
GET /courses/course-versions/$courseVersionId
```

#### Course version stats
```
GET /courses/course-versions/$courseVersionId/stats
```

#### Course version tests
Все кейсы, таблицы, чек-листы версии.
```
GET /courses/course-versions/$courseVersionId/tests
```

#### Courses access
```
GET /courses/courses-access
→ { "$courseId": "NONE | READ | WRITE" }
```

---

## Programs

#### Список программ
```
GET /courses/programs
```

#### Добавление программы
```
POST /courses/programs
{
  "path": $path, "name": $name, "description": $description, "index": $index,
  "programCourses": [
    { "coursePath": $coursePath1, "semesterName": null, "index": 10 }
  ]
}
```

#### Редактирование программы
```
PUT /courses/programs/{path}
```

#### Удаление программы
```
DELETE /courses/programs/{path}
```

#### Добавление/удаление курса в программу
```
POST /courses/programs/{path}/courses?course-path={coursePath}
DELETE /courses/programs/{path}/courses?course-path={coursePath}
```

---

## Courses Passing (прохождение)

#### Courses passing (список, без разделов)
```
GET /courses/courses-passing
```

#### Course passing (одно прохождение, с разделами)
```
GET /courses/courses-passing/$coursePassingId
```

#### Courses passing progress (все)
```
GET /courses/courses-passing/progress
```

#### Course passing progress (одно)
```
GET /courses/courses-passing/$coursePassingId/progress
```

**Объект прогресса:**
```json
{
  "coursePassingId": "ID прохождения",
  "passedSections": "кол-во пройденных текстовых разделов",
  "totalSections": "всего текстовых разделов",
  "passedSectionsPercent": "процент пройденных",
  "passedQuestions": "кол-во пройденных заданий",
  "totalQuestions": "всего заданий",
  "passedQuestionsPercent": "процент выполненных",
  "remainingDays": "предполагаемое кол-во оставшихся дней",
  "hours": "кол-во затраченных часов (указанное пользователем)",
  "activeDays": "кол-во активных дней",
  "passedTestSections": "кол-во пройденных разделов с заданиями",
  "courseName": "название курса",
  "courseId": "ID курса",
  "courseVersionId": "ID версии курса"
}
```

#### Course passing answers (все ответы, без текстов)
```
GET /courses/courses-passing/$coursePassingId/answers
```

#### Course passing validation required
```
GET /courses/courses-passing/$coursePassingId/validation-required
→ { "validationRequired": true/false }
```

#### Progress (по user-ids)
```
GET /courses/progress?user-ids=$userId1,$userId2
```

#### Course passing certificate link
```
GET /courses/courses-passing/$coursePassingId/certificate-link
→ { "certificateLink": "https://aisystant.system-school.ru/cert/cpid=534645767" }
```

#### Start course
`copyActions` — true/false (копировать ответы из предыдущих прохождений). `newCoursePassing` — true/false.
```
POST /courses/start/$courseVersionId?copy-actions=$copyActions&new-course-passing=$newCoursePassing
```

---

## Section (разделы курса)

#### Section text
```
GET /courses/text/$sectionId?course-passing=$coursePassingId
```

#### Section test
```
GET /courses/test/$sectionId?course-passing=$coursePassingId
```

#### Complete section (отметить прочитанным)
```
POST /courses/complete-section/$sectionId?course-passing=$coursePassingId
```

#### Case answers / Section answers
```
GET /courses/answers/$caseId?course-passing=$coursePassingId
GET /courses/section-answers/$sectionId?course-passing=$coursePassingId
```

#### Old answers link
```
GET /courses/old-section-answers-link/$sectionId?course-passing=$coursePassingId
```

---

## Answer (ответы на задания)

#### Answer question
```
POST /courses/answer/question
{
  "questionId": $questionId,
  "coursePassingId": $coursePassingId,
  "answers": [true, false],
  "arguments": ["arg1", ""],
  "comment": "comment"
}
```

#### Answer table
```
POST /courses/answer/fill-table
{
  "questionId": $questionId,
  "coursePassingId": $coursePassingId,
  "rows": [["1.1", "1.2"], ["2.1", "2.2"]],
  "submit": $submit
}
```

#### Answer task
```
POST /courses/answer/task
{
  "questionId": $questionId,
  "coursePassingId": $coursePassingId,
  "checked": $checked,
  "comment": "comment"
}
```

#### Validate task / table (преподаватель)
```
POST /courses/validate-answer/task
POST /courses/validate-answer/fill-table
{
  "answerId": $answerId,
  "status": "DECLINED | COMPLETED",
  "teacherComment": $teacherComment
}
```

---

## Section spent time

#### Get
```
GET /courses/section-spent-time/$sectionId?course-passing=$coursePassingId
→ { "hours": 4.5 }
```

#### Set
```
POST /courses/section-spent-time/$sectionId?course-passing=$coursePassingId&hours=$hours
```

---

## Passing Actions (ключевой для интеграции с ЦД)

> **Действия пользователя** во всех прохождениях курсов. `from` и `to` — даты ISO (yyyy-MM-dd). `user-ids` — необязательный (если не указан — только авторизованный). `brief` — true/false, упрощённая статистика за весь год.

```
GET /courses/passing-actions?from=$from&to=$to&user-ids=$userId1,$userId2&brief=$brief
```

#### Answer symbol count
Количество символов в ответах с группировкой по датам.
```
GET /courses/answer-symbol-count?from=$from&to=$to
```

#### Section versions
```
GET /courses/section-versions/$coursePath/$sectionPath
```

---

## Search

```
POST /api/search/
{
  "coursePath": $coursePath,
  "courseVersion": $courseVersion,
  "query": $query,
  "findSnippets": $findSnippets
}
→ {
    "sectionsAndCases": [{"sectionId": 1, "caseId": 1}],
    "stringsToHighlight": ["Строка 1"]
  }
```

#### Search request history
```
POST /api/search/history
{ "type": $type, "query": $query }
```

---

## Pomodoro

#### Начать
```
POST /api/pomodoro/new
{ "coursePassingId": $coursePassingId, "sectionIdOnStart": $sectionIdOnStart }
→ { "pomodoroId": 1 }
```

#### Остановить
```
POST /api/pomodoro/stop
{ "pomodoroId": $pomodoroId, "sectionIdOnFinish": $sectionIdOnFinish }
```

#### Закончить
```
POST /api/pomodoro/complete
{ "pomodoroId": $pomodoroId, "sectionIdOnFinish": $sectionIdOnFinish }
```

---

## Gaming

#### Награды
`reward.name` — одно из: Systematicity, WeekWithoutGap, MonthWithoutGap.
```
GET /api/gaming/rewards
```

#### Добавить награду (только для админов)
```
POST /api/gaming/rewards
{ "userId": $userId, "name": $name, "description": $description }
```

#### Рейтинг
```
GET /api/gaming/rating?from=$fromDate
```

#### Рейтинг по активному времени прохождений
```
GET /api/gaming/rating-learning-session-time?from=$fromDate
```

#### Рейтинг по кол-ву символов в текстах
```
GET /api/gaming/rating-symbol-count?from=$fromDate
```

#### Создание сессии активного времени
```
POST /api/gaming/learning-sessions
{
  "coursePassingId": $coursePassingId,
  "sectionId": $sectionId,
  "testCaseId": $testCaseId,
  "scrollMode": $scrollMode
}
```

#### Добавление времени к сессии
```
POST /api/gaming/learning-sessions/$id/delta
{ "delta": $delta }
```

#### Обновление времени сессии
```
PUT /api/gaming/learning-sessions/$id
{ "value": $value }
```

#### Суммарное время прохождения
```
GET /api/gaming/learning-session-time
```

#### Статистика по написанным текстам по дням
```
GET /api/gaming/symbol-count?from=$from&to=$to
```

---

## Author

#### Список курсов автора
```
GET /api/author/courses
```

#### Список файлов автора
```
GET /api/author/files
```

#### Файл версии
```
GET /api/author/version-file?course-path=$coursePath&course-version=$courseVersion
```

#### Данные файла версии
```
GET /api/author/version-file-info?course-path=$coursePath&course-version=$courseVersion
```

#### Загрузка файла
```
POST /api/author/upload (multipart-data, file=$file)
```

#### Просмотр изменений и замечаний
`task` — start | status | result.
```
POST /api/author/preview?task=$task
{ "coursePath": $coursePath, "file": $fileName }
```

#### Конвертация
```
POST /api/author/convert
{ "coursePath": $coursePath, "file": $fileName, "changeLog": $changeLog }
```

#### Публикация
```
POST /api/author/publish?course-path=$coursePath&course-version=$courseVersion
{ "changeLog": $changeLog }
```

#### Отмена (удаление неопубликованной версии)
```
POST /api/author/discard?course-path=$coursePath&course-version=$courseVersion
```

#### Изменение курса
```
POST /api/author/update-course?course-path=$coursePath
{
  "name": $name, "authors": $authors, "index": $index, "testIndex": $testIndex,
  "qlBegin": $qlBegin, "qlFinish": $qlFinish, "discussion": $discussion,
  "roleRestriction": ["$role1"], "deprecated": $deprecated
}
```

#### Создание курса
```
POST /api/author/create-course?course-path=$coursePath
```

#### Изменение версии
```
POST /api/author/update-version?course-path=$coursePath&course-version=$courseVersion
{ "changeLog": $changeLog, "test": $test }
```

#### Доступ на редактирование курса
```
GET /api/author/course-authors?course-path=$coursePath
POST /api/author/course-authors?course-path=$coursePath
[$userId1, $userId2]
```

#### Список пользователей с ролью Автор
```
GET /api/author/authors
```

---

## CRM

### CRM Course Passings
```
GET /api/crm/crm-course-passings?user-id=$userId
```

### Potok Lessons
```
GET /api/crm/potok-lessons?potok-ids=$potokId1,$potokId2&format=$format&user-id=$userId
```

### Контрагент (КА)
```
GET, POST /api/crm/ka?query=$query&user-id=$userId
GET, PUT /api/crm/ka/{id}
```

### Контакт
```
POST /api/crm/ka/$kontragentId/contact
PUT, DELETE /api/crm/ka/$kontragentId/contact/{id}
```
`contactType` — EMAIL | PHONE | TEAMS | TG_USERNAME.

### Присвоение квалификации
```
GET, POST /api/crm/ka/$kontragentId/ql
DELETE /api/crm/ka/$kontragentId/ql/{id}
```
`level` — L05, L08, L1, L2...L8.

```
GET /api/crm/ql?from=$from&to=$to&ka=$kontragentId1,$kontragentId2
```

### Список курсов контрагента
```
GET /api/crm/ka/$kontragentId/courses
```

### Поток
```
GET, POST /api/crm/potok?active=$active
GET, PUT /api/crm/potok/{id}
```

### Участие в потоке
```
GET, POST /api/crm/potok/$potokId/course-passing
GET, PUT, DELETE /api/crm/potok/$potokId/course-passing/{id}
GET /api/crm/ka/$kontragentId/crm-course-passings
```

### Список пользователей потока
```
GET /api/crm/potok/$potokId/users?charge-off-list=true/false
```

### Продление подписки в связи с участием в потоке
```
POST /api/crm/potok/$potokId/extend-subscriptions
```

### Онлайн-курсы для потока
```
GET /api/crm/potok/$potokId/online-courses-of-course-version
GET /api/crm/potok/$potokId/online-courses
PUT /api/crm/potok/$potokId/online-courses?course-ids=$courseId1,$courseId2
```

### Проверка кандидатов
```
POST /api/crm/potok/$potokId/check-candidates
```

### Регистрация платежа за стажировку
```
POST /api/crm/potok/$potokId/register-payment
{ "email": $email, "amount": $amount, "currency": $currency, "paymentIndex": $paymentIndex }
```

### Списания средств за стажировку
```
GET /api/crm/potok/$potokId/charge-off-list
DELETE /api/crm/potok/$potokId/charge-off-list/$chargeOffId
```

### Событие
```
GET, POST /api/crm/event
GET, PUT /api/crm/event/{id}
```
`type` — CONFERENCE | METHOD_SOVET | WEBINAR.

### Событие контрагента
```
GET, POST /api/crm/ka/$kontragentId/user-event
GET, PUT /api/crm/ka/$kontragentId/user-event/{id}
GET, POST /api/crm/event/$eventId/user-event
GET, DELETE /api/crm/event/$eventId/user-event/{id}
```

### Курс (офлайн, CRM)
```
POST /api/crm/course
PUT /api/crm/course/{id}
```

### Версия курса (офлайн, CRM)
```
POST /api/crm/course-version
PUT /api/crm/course-version/{id}
```

### Онлайн-курсы для версии очного курса
```
GET /api/crm/course-version/$courseVersionId/online-courses
PUT /api/crm/course-version/$courseVersionId/online-courses?course-ids=$courseId1,$courseId2
GET /api/crm/online-courses?course-version-ids=$courseVersionId1,$courseVersionId2
```

### Занятие
```
GET /api/crm/lesson
GET, POST /api/crm/potok/$potokId/lesson
PUT, DELETE /api/crm/potok/$potokId/lesson/{id}
GET /api/crm/ka/$kontragentId/lesson
```

### Задача для потока
```
GET, POST /api/crm/potok/$potokId/issue
GET, PUT, DELETE /api/crm/potok/$potokId/issue/$issueId
```

### Шаблон списка задач
```
GET, POST /api/crm/issues-template
GET, PUT, DELETE /api/crm/issues-template/$issuesTemplateId
POST /api/crm/potok-to-issues-template?potok-id=$potokId
POST /api/crm/issues-template-to-potok?issues-template-id=$issuesTemplateId&potok-id=$potokId
```

### Сообщение в телеграм для потока
```
GET, POST /api/crm/potok/$potokId/group-message
GET, PUT, DELETE /api/crm/potok/$potokId/group-message/$groupMessageId
```
`datetime` — по MSK, ISO, до полчаса. `parseMode` — MarkdownV2 | HTML.

### Шаблон сообщения в телеграм
```
GET, POST /api/crm/group-messages-template
GET, PUT, DELETE /api/crm/group-messages-template/$issuesTemplateId
POST /api/crm/potok-to-group-messages-template?potok-id=$potokId
POST /api/crm/group-messages-template-to-potok?group-messages-template-id=$groupMessagesTemplateId&potok-id=$potokId
```

### Пользователь и контрагент по email
```
GET /api/crm/email-data?email=$email
```

---

## Ambassadors

#### Список кодов амбассадора
```
GET /api/ambassador/ambassador-codes
```

#### Список амбассадоров
```
GET /api/ambassador/ambassadors
```

#### Список последователей
```
GET /api/ambassador/users
```

#### Амбассадор по коду
```
GET /api/ambassador/ambassador?code=$code
```

#### Изменение кодов
```
POST /api/ambassador/codes
[$code1, $code2]
```

#### Стать последователем
```
POST /api/ambassador/ambassador
{ "code": $code }
```

---

## Homepage

```
GET /api/homepage/stats
```

---

## Teacher (преподаватель)

#### Прохождения версии курса по потоку
```
GET /api/teacher/course-passings?course-version=$courseVersionId&potok=$potokId
```

#### Статистика прохождения по главам
```
GET /api/teacher/progress?course-version=$courseVersionId&potok=$potokId
```

#### Все ответы по прохождениям
```
GET /teacher/answers?course-passings=$coursePassingId1,$coursePassingId2
```

#### Пройденные/отправленные на проверку разделы
```
GET /api/teacher/sections-to-validate
```

---

## Telegram

> Без префикса `/api`

#### Присутствие в группе стажировки
```
GET /tg/check-internship-users?potok-id=$potokId&tg-ids=$tgId1,$tgId2
```

#### Информация о телеграм-аккаунтах в группе
```
GET /tg/internship-chat-members?potok-id=$potokId
```

---

## Ошибки

HTTP 4xx/5xx → JSON с `code` (обязательное) и `message` (может быть null).

| Код | Описание |
|-----|----------|
| `ex.auth.no_credentials` | Не указаны пользователь или пароль |
| `ex.auth.authenticated` | Пользователь уже аутентифицирован |
| `ex.auth.incorrect_email` | Некорректный E-mail |
| `ex.auth.incorrect_password` | Некорректный пароль |
| `ex.auth.email_already_exists` | E-mail уже существует |
| `ex.auth.email_not_exists` | E-mail не существует |
| `ex.auth.not_created.name_is_empty` | Не введены имя или фамилия |
| `ex.auth.not_updated.incorrect_link` | Некорректная ссылка |
| `ex.auth.not_updated.already_confirmed` | E-mail уже подтверждён |

---

*Сохранено: 2026-03-17. Источник: внутренний Google Doc LMS-команды.*
