FROM python:3.10.10-buster

WORKDIR /tubes-tst-app

COPY . /tubes-tst-app

RUN pip3 install -r requirements.txt

CMD ["uvicorn", "app.main:app" , "--host", "0.0.0.0", "--port", "80"]