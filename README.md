# Анализатор страниц (Page analyzer)


Приложение ["Анализатор страниц или Page_analyzer"](https://python-project-83-i57z.onrender.com) — анализирует веб-страницы на их SEO-пригодность по аналогии с [PageSpeed Insights](https://pagespeed.web.dev/).
Проект реализаван на Python, Flask и PostgreSQL.
Проект предоставляет пользователям возможность извлекать ключевую информацию о страницах, проверять доступность веб-сайтов и анализировать такие элементы, как теги H1, заголовки и описания сайтов.
Результаты проверок сохраняются в базе данных.

## Установка

### Предварительные требования
1. Установленный [Python](https://www.python.org/downloads/) версии 3.10 и выше
2. Установленный [Flask](https://flask.palletsprojects.com) версии 3.0.3 и выше
3. Установленный [PostgreSQL](https://www.postgresql.org/download/) версии 16.4 и выше
4. Установленный [Poetry](https://python-poetry.org/docs/#installation) версии 1.8.4 и выше

### Клонирование репозитория и конфигурирование

```bash
git clone https://github.com/akasmall/python-project-83
cd page-analyzer

# Конфигурирование

Перед запуском приложения вам необходимо настроить переменные среды. Дублируйте файл `.env.example` и переименуйте его в `.env`. Затем измените его с вашими фактическими данными для следующих переменных:
- `SECRET_KEY`: секретный ключ для вашего приложения.
- `DATABASE_URL`: строка подключения к вашей базе PostgreSQL, отформатрованная как `postgresql://username:password@localhost:5432/database_name`.

# Для сборки приложения и создания таблиц базы данных используйте баш-скрипт
build.sh

Используйте `Makefile` для упрощения процесса установки и запуска:

# Запуск локального сервер разработки
make dev

# Запуск производственного (рабочего) сервера
make start
```

## Как работать с анализатором страниц

Нужно:
1. На главной странице ввести адрес сайта и нажать "Проверить", после этого откроется страница для проверки.
![Screenshot_31](https://github.com/user-attachments/assets/2c03ddc2-1693-4a5b-9be6-b77d094db9bc)
2. На странице для проверки нажать кнопку "Запустить проверку" и дождаться результата.
![Screenshot_32](https://github.com/user-attachments/assets/0c965f82-5028-4ce3-9b51-201786f0deac)
3. Вверху страницы, в навигации, можно перейти на список введенных и сохраненных сайтов.
![Screenshot_33](https://github.com/user-attachments/assets/9607b654-7586-452f-a8de-5b1b242162d0)

### Hexlet tests and linter status:
[![Actions Status](https://github.com/akasmall/python-project-83/actions/workflows/hexlet-check.yml/badge.svg)](https://github.com/akasmall/python-project-83/actions)
[![Maintainability](https://api.codeclimate.com/v1/badges/0f7aff68e1d19cafdb0f/maintainability)](https://codeclimate.com/github/akasmall/python-project-83/maintainability)
