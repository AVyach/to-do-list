# Инструкция по запуску

## Инициализация окружения
В корне проекта создать файл .env и занести в него следующие значения:  
POSTGRES_USER=<пользователь postgres>  
POSTGRES_PASSWORD=<пароль postgres>  
POSTGRES_DBNAME=<имя базы данных postgres>  
POSTGRES_DBNAME_KEYCLOAK=<имя базы данных пользователей postgres>  
KEYCLOAK_ADMIN=<администратор keycloak>  
KEYCLOAK_ADMIN_PASSWORD=<пароль keycloak>  
POSTGRES_PORT=<порт postgres>(обычно 5432)  
POSTGRES_HOST=<хост postgres>(для локального запуска 0.0.0.0)  

После проделанных шагов выполнить команду `source .env`  

## Запуск бекенда
1. `pip install pdm`
2. `pdm install --frozen-lockfile`
3. `pdm run src/main.py`

## Запуск фронтенда
1. `cd vue-app`
2. `npm install`
3. `npm run dev`
