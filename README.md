# wedding

## порты

- база: 5432
- приложение: 8000

## локальный запуск для дебага

```bash
cp env/.env.local .env
docker-compose -f docker-compose.local.yml up -d db
python wedding/app.py
```

## локальный запуск в docker-compose

```bash
docker-compose -f docker-compose.local.yml up -d
```
