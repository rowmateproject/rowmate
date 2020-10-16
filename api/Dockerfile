FROM python:3.8.5

RUN mkdir -p /opt/rowmate/api
WORKDIR /opt/rowmate/api

COPY . /opt/rowmate/api

RUN pip3 install -r requirements.txt --use-feature=2020-resolver

EXPOSE 8000

CMD [ "uvicorn", "asgi:app", "--host", "127.0.0.1", "--port", "8000" ]
