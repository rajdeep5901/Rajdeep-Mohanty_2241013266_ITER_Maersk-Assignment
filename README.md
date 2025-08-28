# NDAC Alarm Email Notifications Service

## Overview
Polls NDAC alarms, filters Critical/Major, emails stakeholders, logs and retries. Includes minimal dashboard and admin endpoints.

## Quick Start
1. Python 3.10+
2. `pip install -r requirements.txt`
3. Copy `.env.example` to `.env` and edit values.
4. `python run.py`
5. Open `http://127.0.0.1:8000/dashboard`

## ENV
- NDAC_BASE_URL, NDAC_TOKEN, NDAC_MOCK (1 to use mock data)
- SMTP_* and FROM_ADDR
- DB_URL (default sqlite:///ndac.db)
- POLL_INTERVAL_MIN (default 60)
- STAKEHOLDERS (comma emails)
- ADMIN_TOKEN

## Endpoints
- `GET /health`
- `GET /metrics`
- `POST /trigger` (Header: `Authorization: Bearer {ADMIN_TOKEN}`)
- `GET /dashboard`
- `GET /recipients` (auth)
- `POST /recipients` (auth) body: `{"email":"a@b.c","name":"X"}`
- `DELETE /recipients/{email}` (auth)

## Dev Notes
- Scheduler runs background job at fixed interval from `POLL_INTERVAL_MIN`.
- First run seeds recipients from `STAKEHOLDERS` if DB is empty.
- Mock NDAC server optional: `python mock_ndac.py` on :5055.

## Run Mock NDAC (optional)
In another shell: `python mock_ndac.py` then set `NDAC_MOCK=1` or use the endpoint.

## Docker (optional)
- Build: `docker build -t ndac-svc .`
- Run: `docker run -p 8000:8000 --env-file .env ndac-svc`

## Testing
- Manual trigger: `curl -XPOST -H "Authorization: Bearer $ADMIN_TOKEN" http://127.0.0.1:8000/trigger`