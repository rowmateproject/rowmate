FROM node:latest

RUN mkdir -p /opt/rowmate/app
WORKDIR /opt/rowmate/app

COPY . /opt/rowmate/app
RUN npm install

RUN npm run build

EXPOSE 3000

ENV NUXT_HOST=127.0.0.1
ENV NUXT_PORT=3000

CMD [ "npm", "run", "start" ]
