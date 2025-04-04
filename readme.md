Создать файл .env в корне проекта и заполнить следующими переменными

```sh
POSTGRES_USER=tracker_db_user
POSTGRES_PASSWORD=tracker_db_pass
POSTGRES_DB=tracker_db
POSTGRES_HOST=postgres
POSTGRES_PORT=5432
SECRET_KEY=09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7
```

Запустить докер команду

`docker-compose up --build`

Свагер с описанием api

`http://localhost:8000/docs`

Все методы защищены авторизацией, кроме
`/sign_up` и `/sign_in`

Метод `/sign_in` автоматически устанавливает авторизационный токен в куки. Но для удобства сейчас токен возвращается в ответе метода `/sign_in`

Вот так выглядит запрос на создание задачи с авторизационным токеном

```sh
curl -X 'POST' \
  'http://localhost:8000/api/v1/tasks' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -H 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6MSwic3ViIjoidXNlckBnbWFpbC5jb20iLCJleHAiOjE3NDM4MDIzOTF9.0DYgVNuq0-mFnYyGjjdBg4KBJa9cnyvPYy4LuCntC0w' \
  -d '{
  "status": "backlog",
  "card_title": "Сходить в магазин",
  "tag": {
    "title": "Личное",
    "color": "red"
  },
  "start_date_time": "2025-04-04T21:07:43.578Z",
  "end_date_time": "2025-04-04T21:07:43.578Z"
}'
```