# Создать сеть
docker network create canalservis-network

# Собрать контейнер Джанго
docker build -t canalservis-django ./Kanalservis_Test_Task

# Собрать контейнер Telegrambot
docker build -t canalservis-telegram ./Telegram_Bot

# Собрать контейнер обновления базы
docker build -t canalservis-script ./DB_update_script

# Запустить контейнер PostgreSQL
docker run -d --name canalservis-postgresql --network canalservis-network -p 5432:5432 -e POSTGRES_PASSWORD=canalservis -e POSTGRES_USER=dev -e POSTGRES_DB=canalservis -d postgres:15.2

# Запустить контейнер обновления базы
docker run -d --name canalservis-script-container --network canalservis-network canalservis-script

# Запустить контейнер Django
docker run -d --name canalservis-django-container --network canalservis-network -p 8000:8000 canalservis-django

# Запустить контейнер Telegrambot
docker run -d --name canalservis-telegram-container --network canalservis-network canalservis-telegram
