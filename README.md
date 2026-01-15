# Hotel Admin Platform

Minimal internal hotel admin tool with FastAPI + React.


## Prerequisites
- Python 3.11+ with `venv`
- Node 18+

## Backend setup
```...
cd backend
python -m venv .venv
venv\\Scripts\\activate
pip install -r requirements.txt
# apply migrations 
alembic upgrade head
# start the backend
uvicorn app.main:app --reload --port 8000
```

### User Credentials
- Username/Email: `admin@hotel.local` (also accepts `admin`)
- Password: `Admin@123`




## Frontend setup
```bash
cd frontend
npm install
npm run dev -- --port 5173
```
App expects API at `http://localhost:8000` (override with `VITE_API_URL`).

## Usage
1. Visit `http://localhost:5173/login`
2. Log in with seeded user
3. Start using

## Design notes / trade-offs
- SQLite chosen for simplicity; replace `DATABASE_URL` for other engines.
- Money values stored as `Decimal`/`Numeric(10,2)` and serialized as floats in responses.
- JWT access token only; stored client-side in `localStorage` for quick re-auth across refreshes.
- Effective-rate rule implemented once in `rate_adjustment_service.compute_effective_rate`; adjustments validated to prevent negative effective rates.
- Alembic follow-up migration `0002_add_hotel_status` adds `status` column + index to hotels (default `"active"`).
- CORS allows `http://localhost:5173` for local dev.



## Notes
- Run migrations before launching the API to keep schema aligned with models.
- Error handling returns JSON with clear messages and HTTP status codes (401/404/409/400 as appropriate).
