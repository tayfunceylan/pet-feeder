# pet-tracking

## Get Started

First rename `.env.example` to `.env` and adjust the environment vars to your liking.
Then use `docker compose` to easily run the dev setup (Django, Nuxt, Nginx Proxy).

```sh
docker compose -f dev.yml up
```

## Production

For production, there are two steps:

1. backend:
   1. use `docker compose up -d` to start the backend
   2. make sure `DJANGO_DEBUG` is set to 0 and `DJANGO_SECRET_KEY` is set to a long and random value
   3. to create super user run `docker exec -ti django python manage.py createsuperuser --no-input`. Set `DJANGO_SUPERUSER_USERNAME`, `DJANGO_SUPERUSER_PASSWORD` and `DJANGO_SUPERUSER_EMAIL` in docker compose file before running the command.

2. frontend:
   1. run `npx nuxi generate` in the frontend folder to generate .output/public and serve the public folder with an nginx/apache server
