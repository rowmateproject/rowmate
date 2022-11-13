# This repo is archived. Please refer to rowmate-v2 on https://github.com/rowmateproject


![license](https://img.shields.io/github/license/maurosbicego/rowmate)
![github build status](https://img.shields.io/github/workflow/status/maurosbicego/rowmate/rowmate)
![repository size](https://img.shields.io/github/repo-size/maurosbicego/rowmate)

# rowmate

> Rowmate ermöglicht es, sich innerhalb des Vereins zum Rudern zu verabreden.


### Project structure

```bash
.
├── api
│   ├── ...
│   └── Dockerfile
├── app
│   ├── ...
│   └── Dockerfile
└── docker-compose.yml
```


[_docker-compose.yml_](docker-compose.yml)

```bash
services:
  db:
    image: mongo:3.6.20-xenial
    ports:
      - '127.0.0.1:27017:27017'
    network_mode: 'host'
    restart: always
  api:
    build:
      dockerfile: Dockerfile
      context: api
    image: rowmate:api
    env_file:
      - api/.env
    depends_on:
      - db
    ports:
      - '127.0.0.1:8000:8000'
    network_mode: 'host'
  app:
    build:
      dockerfile: Dockerfile
      context: app
    image: rowmate:app
    env_file:
      - app/.env
    depends_on:
      - api
    ports:
      - '127.0.0.1:3000:3000'
    network_mode: 'host'
```


### Deploy with docker-compose

```bash
docker-compose up -d
```

```bash
Starting rowmate_db_1 ... done
Starting rowmate_api_1 ... done
Starting rowmate_app_1 ... done
```


### Stop and remove the containers

```bash
docker-compose down
```
