# Используем python 3.11
FROM python:3.11

# Ставим рабочую директорию
WORKDIR /usr/src/app

# Виртуальные переменные
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

# Установка зависимостей
RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt

# Копируем entrypoint.sh
COPY ./entrypoint.sh .
RUN sed -i 's/\r$//g' /usr/src/app/entrypoint.sh
RUN chmod +x /usr/src/app/entrypoint.sh

# Копируем проект
COPY . .

# entrypoint.sh
ENTRYPOINT ["/usr/src/app/entrypoint.sh"]
