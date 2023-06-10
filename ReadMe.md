# Проект "Викторина" (quiz)

Веб сервис реализующий API для получения и сохранения в БД вопросов полученных от ресурса https://jservice.io/
Для установки и запуска данного проекта используется docker-окружение.

## Используемые технологии
- _Python 3_
- _FastAPI_
- _Uvicorn_
- _PostgresSQL_
- _Docker_

## Как установить
Клонировать репозиторий в целевую папку на машине с установленным ПО Docker.
В терминале зайти в каталог с файлом "docker-compose.yml". Выполнить команду:
```
docker-compose up
```
## Как использовать
После развертывания и запуска docker-контейнеров (контейнеры: app и postgres), можно обращаться к сервису по адресу http://localhost:8000
API cервиса реализует один запрос: получение вопроса для викторины

Пример запроса:

  request: POST http://localhost:8000/quiz    body: {"questions_num": 3}
  
  где параметр "questions_num" определяет количество случайных вопросов, которые нужно получить от ресурса https://jservice.io/
  
  response:
  
     либо пустой json, если ранее в БД не было сохранено ни одного вопроса: {}
     либо предыдущий сохраненный в БД вопрос:
     
        {
        "id": 213037,
        "question": "The wearer of this wouldn't likely know that its name goes back to a Scottish scholar & his followers after he fell out of favor",
        "answer": "a dunce cap",
        "created_at": "2022-12-30T22:02:46.123000+00:00",
        "category": "word origins"
        }





