FROM python:3.11
ENV PYTHONUNBUFFERED 1
WORKDIR bot
COPY . /bot
RUN chmod 777 ./entrypoint.sh
RUN pip install -r requirements.txt
CMD ["./entrypoint.sh"]
