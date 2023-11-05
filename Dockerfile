FROM python:3.11

WORKDIR /tubes-tst-app

COPY requirements.txt .

RUN pip3 install -r requirements.txt

COPY ./app ./app

COPY .env .

CMD ["python3", "./app/main.py"],