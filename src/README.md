# indoor-climate-data-storage

### To set up local:

```bash
cp .env.example .env
```

```bash
docker compose build
```

```bash
docker compose run -w /code/ fastapi make migrate
```

```bash
docker compose up
```

### Enabling CORS:
* open `.env` file
* add `ALLOWED_CORS=<your host>`
* rebuild docker container
