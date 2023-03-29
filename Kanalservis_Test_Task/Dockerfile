# Указывает Docker использовать официальный образ python 3 с dockerhub в качестве базового образа
FROM python:3.10.10

# Python не будет пытаться создавать файлы .pyc,
ENV PYTHONDONTWRITEBYTECODE 1
# Устанавливает переменную окружения, которая гарантирует, что вывод из python будет отправлен прямо в терминал без предварительной буферизации
ENV PYTHONUNBUFFERED 1

ENV DB_HOST canalservis-postgresql

ENV TZ=Europe/Moscow

RUN python3 -V
RUN apt update

# Устанавливает рабочий каталог контейнера

WORKDIR /Django

# Копирует все файлы из нашего локального проекта в контейнер
COPY . .

# Запускает команду pip install для всех библиотек, перечисленных в requirements.txt
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]
