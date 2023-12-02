FROM python:3.10.10-buster

WORKDIR /tubes-tst-app

COPY requirements.txt /tubes-tst-app/requirements.txt

RUN pip3 install -r requirements.txt

COPY ./app /tubes-tst-app/app

CMD ["uvicorn", "app.main:app" , "--host", "0.0.0.0", "--port", "80"]