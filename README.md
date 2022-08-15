### Проект Foodgram: ![Build status](https://github.com/Ivanr2000/foodgram-project-react/actions/workflows/foodgram_workflow.yml/badge.svg)
Дипломный проект Яндекс Практикум - предназначен для ведения рецептов пользователями.

Проект развернут по адресу http://84.201.139.203/ , фронтенд получает данные от бэкенда с помощью API. Документация к API доступна по конечной точке - /api/docs/

### Технологии:

```
Django v.2.2
Django-rest-framework
Python 3.8
PostgreSQL
Docker
```

### Как запустить проект самостоятельно:

Сделать форк репозитория:

```
git clone https://github.com/Ivanr2000/foodgram-project-react
```

Прописать в настройках репозитория в разделе SECRETS все необходимые переменные в соответствии с файлом foodgram_workflow.yml (после равно приведены примеры или описания того, что должен содержать ключ):
```
DB_ENGINE=django.db.backends.postgresql
DB_NAME=postgres
POSTGRES_USER=<имя пользователя postgress>
POSTGRES_PASSWORD=<пароль postgress>
DB_HOST=db
DB_PORT=<port_number> - порт для базы данных
DOCKER_PASSWORD=<пароль докера>
DOCKER_USERNAME=<пользователь докера>
HOST=<адрес сервера>
PASSPHRASE=<парольная фраза ssh>
SSH_KEY=<ssh ключ сервера>
TELEGRAM_TO=<id чата телеграмм для отправки сообщений>
TELEGRAM_TOKEN=<токен бота телеграмм>
USER=<пользователь на сервере>
```

В файле README скорревктировать бейдж и сделать push на сервер в векту мастер, после этого будет запущено workflow и произойдет запуск проекта.

Подключиться к серверу, сделать миграции, завести пользователей, обновить статику.

```
sudo docker-compose exec web python manage.py migrate
sudo docker-compose exec web python manage.py createsuperuser
sudo docker-compose exec web python manage.py collectstatic --no-input
```
