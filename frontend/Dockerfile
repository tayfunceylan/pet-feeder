FROM node:20-alpine3.16
WORKDIR /app
COPY package.json nuxt.config.ts yarn.lock ./
RUN yarn install
ENV HOST=0.0.0.0