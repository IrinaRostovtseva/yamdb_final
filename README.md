https://github.com/IrinaRostovtseva/yamdb_final/workflows/Yamdb_final%20workflow/badge.svg
<!-- https://github.com/IrinaRostovtseva/yamdb_final/workflows/Yamdb_finalworkflow/badge.svg -->

# **API YaMDb**

Этот проект создан в рамках курсов по API и инфраструктуре бэкенд-разработки Яндекс.Практикума. Проект YaMDb собирает отзывы пользователей на произведения в категориях «Книги», «Фильмы», «Музыка».

## Требования

+  Docker

## Разворачивание проекта на сервере

1.  Склонируйте проект

2.  В корневой директории проекта создайте файл .env со следующим содержимым:

        DB_ENGINE=django.db.backends.postgresql
        DB_NAME=<название-бд>
        DB_USER=<имя-пользователя-бд>
        DB_PASSWORD=<пароль-к-бд>
        DB_HOST=db
        DB_PORT=5432
        POSTGRES_USER=<имя-пользователя-бд-postgresql>
        POSTGRES_PASSWORD=<пароль-к-бд-postgresql>

3.  (Необязательный пункт) При необходимости заполнения базы данных своими данными добавьте файл fixtures.json в корневую директорию проекта

4.  Создайте контейнеры для сервера базы данных и приложения YaMDb

        docker-compose up

5.  Зайдите в контейнер приложения

        docker exec -it <CONTAINER_ID> bash

6.  Выполните миграции

        ./manage.py migrate

7.  (Необязательный пункт) Загрузите данные из fixtures.json в базу данных

        ./manage.py loaddata fixtures.json

8.  Создайте суперпользователя

        ./manage.py createsuperuser


## Документация к API YaMDb

Документация доступна по url в проекте /redoc/