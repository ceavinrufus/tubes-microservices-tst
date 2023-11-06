FROM python:3.11

WORKDIR /tubes-tst-app

COPY requirements.txt /tubes-tst-app/requirements.txt

RUN pip3 install -r requirements.txt

COPY ./app /tubes-tst-app/app

COPY .env /tubes-tst-app/.env

CMD ["uvicorn", "app.main:app" , "--host", "0.0.0.0", "--port", "8080", "--reload"]