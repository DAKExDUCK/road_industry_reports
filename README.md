# Road Industry Reports

Monorepo with:

- `api server/` - FastAPI backend + Postgres
- `client/` - Expo React Native app (web + mobile)

Quick start (docker-compose):

```bash
# from repo root
cp "api server/.env.example" "api server/.env"   # edit if needed
docker-compose up --build
```

Backend will be available at http://localhost:8000
Client: go into `client/`, run `npm install` and `npm run start` (requires Node + Expo).
