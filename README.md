# Django Stripe API

[![Python](https://img.shields.io/badge/-Python-464646?style=flat-square&logo=Python)](https://www.python.org/)
[![Django](https://img.shields.io/badge/-Django-464646?style=flat-square&logo=Django)](https://www.djangoproject.com/)
[![PostgreSQL](https://img.shields.io/badge/-PostgreSQL-464646?style=flat-square&logo=PostgreSQL)](https://www.postgresql.org/)
[![docker](https://img.shields.io/badge/-Docker-464646?style=flat-square&logo=docker)](https://www.docker.com/)
[![GitHub%20Actions](https://img.shields.io/badge/-GitHub%20Actions-464646?style=flat-square&logo=GitHub%20actions)](https://github.com/features/actions)


## Локальный запуск

Склонируйте репозиторий.

Находясь в папке с кодом создайте виртуальное окружение `python -m venv venv`, активируйте его (Windows: `source venv\scripts\activate`; Linux/Mac: `source venv/bin/activate`), установите зависимости `python -m pip install -r requirements.txt`.
Переименуйте `.env.example` в `.env` и заполните его.

Для локального запуска, находясь в директории проекта выполните команды:

```
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

## Запуск проекта через Docker

Перейдите в корневую папку проекта где находится файл `docker-compose.yaml` и выполните команду:

```
docker-compose up -d --build
```

При первом запуске проекта выполняться миграции в базу данных. Для создания `superuser` выполните команду:

```
docker exec project_django_stripe-api python manage.py createsuperuser
```

## Маршруты API
### Основные
```
http://127.0.0.1:8000/ - Страница списка предметов
http://127.0.0.1:8000/buy/<int:pk>/ - Получить id сессии stripe при покупке предмета
http://127.0.0.1:8000/item/<int:pk>/ - Страница предмета
http://127.0.0.1:8000/success/ - Страница успешной оплаты
http://127.0.0.1:8000/cancel/ - Страница отмены оплаты

```

### Бонусные
```
http://127.0.0.1:8000/admin/ - Панель администратора
http://127.0.0.1:8000/order/<int:order_pk>/ - Страница заказа
http://127.0.0.1:8000/buy_order/<int:order_pk>/ - Получить id сессии stripe при покупке заказа
```

```
4242 4242 4242 4242 - тестовые данные номера карты для успешного платежа
```

## Деплой на удаленный сервер

Необходимо создать переменные окружения в вашем репозитории github в разделе `secrets`

```
DOCKER_PASSWORD - Пароль от Docker Hub
DOCKER_USERNAME - Логин от Docker Hub
HOST - Публичный ip адрес сервера
SSР_USERNAME - Пользователь сервера
SSH_PASSWORD - Пароль пользователя для сервера
STRIPE_PUBLISHABLE_KEY - Ваш Publishable key с сайта stripe.com
STRIPE_SECRET_KEY - Ваш Secret key с сайта stripe.com

POSTGRES_USER - Пользователь postgresql
POSTGRES_PASSWORD - Пароль postgresql
POSTGRES_NAME - База данных postgresql
```

## Деплой на удаленный сервер

Необходимо создать переменные окружения в вашем репозитории github в разделе `secrets`

```
DOCKER_PASSWORD # Пароль от Docker Hub
DOCKER_USERNAME # Логин от Docker Hub
HOST # Публичный ip адрес сервера
USER # Пользователь сервера
PASSPHRASE # Если ssh-ключ защищен фразой-паролем
SSH_KEY # Приватный ssh-ключ
TELEGRAM_TO # ID телеграм-аккаунта (для оправки уведомления об успешном деплое)
TELEGRAM_TOKEN # Токен бота (для оправки уведомления об успешном деплое)
STRIPE_PUBLISHABLE_KEY # Ваш Publishable key с сайта stripe.com
STRIPE_SECRET_KEY # Ваш Secret key с сайта stripe.com
```

При каждом обновлении репозитория (git push) будет происходит сборка и обновление образа на сервисе Docker Hub.
