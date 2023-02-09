FROM alpine:3.10

RUN apk add --no-cache python3 py3-pip

COPY requirements.txt /usr/src/app/
RUN pip3 install --upgrade pip

RUN apk update && apk add postgresql-dev gcc python3-dev musl-dev && pip3 install psycopg2-binary
RUN pip3 install --no-cache-dir -r /usr/src/app/requirements.txt

COPY main.py /usr/src/app/
COPY create_db.py /usr/src/app/
COPY script.sql /usr/src/app/
WORKDIR /usr/src/app/

EXPOSE 80

CMD ["python3", "/usr/src/app/create_db.py"]

CMD ["python3", "/usr/src/app/main.py"]