FROM node:20-alpine3.16
WORKDIR /usr/src/app
COPY . ./
RUN yarn install
RUN yarn build
ENV HOST=0.0.0.0