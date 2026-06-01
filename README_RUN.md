# Restaurant Order Management System

Enterprise information system for a restaurant/service business.

## Main stack

- Backend: Python, Django 4.2, Django REST Framework
- Pattern: Django MVC/MVT + REST API
- Database: MySQL
- Async queue: Celery + RabbitMQ
- Auth: JWT + Google OAuth2-ready login using `social-auth-app-django`
- Payments: Stripe sandbox-ready online payments + deterministic demo sandbox tokens
- Offline payments: admin approval/rejection in Django Admin and REST API
- API docs: Swagger/OpenAPI through drf-spectacular
- Tests: unit/integration tests with coverage target above 50%

## Requirement checklist

| Requirement | Implementation |
|---|---|
| MVC or REST API pattern | Django templates + DRF REST API |
| Backend language not JS/Node/TS | Python/Django only |
| Asynchronous queue | Celery with RabbitMQ broker |
| Enterprise information system | Restaurant ordering, trade/service domain |
| Social OAuth2 login | Google OAuth2 configuration + `/oauth/login/google-oauth2/` + REST demo endpoint |
| Electronic payment sandbox | Stripe sandbox-ready service + `tok_success` / `tok_fail` demo tokens |
| Failed payment handling | `FAILED` status and `failure_reason` stored |
| Offline admin approval | Admin actions + `/api/payments/{id}/approve_offline/` and `/reject_offline/` |
| Tests >= 50% business logic | Current measured coverage: about 90% in this package |
| API docs | `/api/docs/` |

## Local Windows run with your MySQL

Your current local MySQL settings are expected to be:

```text
Database: restaurant_db
User: root
Password: root123
Host: localhost
Port: 3307
```

Commands:

```bash
cd C:\Users\SAGHI\Documents\restaurant_order_system
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py seed_demo
python manage.py runserver
```

Open:

```text
Customer site: http://127.0.0.1:8000/
API docs:      http://127.0.0.1:8000/api/docs/
Admin panel:   http://127.0.0.1:8000/secure-admin-2026/
```

## Start RabbitMQ/Celery

The academic requirement asks for asynchronous message queues. For local development, install RabbitMQ or use Docker. Then run a second terminal:

```bash
venv\Scripts\activate
celery -A restaurant_system worker -l info
```

If RabbitMQ is not running and you only want to test Django pages, you can temporarily set this in `.env`:

```text
CELERY_TASK_ALWAYS_EAGER=True
```

That executes async tasks immediately in development.

## Docker run

```bash
cp .env.example .env
docker compose up --build
```

In another terminal:

```bash
docker compose exec web python manage.py migrate
docker compose exec web python manage.py createsuperuser
docker compose exec web python manage.py seed_demo
docker compose exec web python manage.py test --settings=restaurant_system.test_settings
```

## Tests and coverage

```bash
coverage run --source=accounts,restaurant,orders,payments manage.py test --settings=restaurant_system.test_settings
coverage report -m
```

Verified in this package:

```text
9 tests OK
Coverage: 90%
```

## Payment testing

### Online demo/sandbox through API

Create an online payment:

```json
{
  "order_id": 1,
  "sandbox_token": "tok_success"
}
```

Use this endpoint:

```text
POST /api/payments/online/
```

Use `tok_fail` to force a failed payment:

```json
{
  "order_id": 1,
  "sandbox_token": "tok_fail"
}
```

### Stripe sandbox mode

Set these in `.env`:

```text
STRIPE_DEMO_MODE=False
STRIPE_SECRET_KEY=sk_test_your_key
STRIPE_CURRENCY=pln
```

Then send a Stripe test payment method such as a Stripe sandbox `pm_...` value as `sandbox_token`.

## Google OAuth2 setup

1. Create credentials in Google Cloud Console.
2. Add redirect URI:

```text
http://127.0.0.1:8000/oauth/complete/google-oauth2/
```

3. Set in `.env`:

```text
GOOGLE_OAUTH_CLIENT_ID=your-client-id
GOOGLE_OAUTH_CLIENT_SECRET=your-client-secret
SOCIAL_OAUTH_DEMO_MODE=False
```

4. Open:

```text
http://127.0.0.1:8000/oauth/login/google-oauth2/
```

The login page also contains a Google OAuth2 button.

## Main REST endpoints

### Auth

- `POST /api/auth/register/`
- `POST /api/auth/token/`
- `POST /api/auth/token/refresh/`
- `GET /api/auth/me/`
- `POST /api/auth/social-login/` demo OAuth2/JWT endpoint

### Restaurant

- `GET/POST /api/tables/`
- `GET/POST /api/categories/`
- `GET/POST /api/menu-items/`

### Orders

- `GET/POST /api/orders/`
- `POST /api/orders/{id}/add_item/`
- `POST /api/orders/{id}/submit/`
- `POST /api/orders/{id}/mark_preparing/` staff only
- `POST /api/orders/{id}/mark_ready/` staff only
- `POST /api/orders/{id}/cancel/`

### Payments

- `POST /api/payments/online/`
- `POST /api/payments/offline/`
- `POST /api/payments/{id}/approve_offline/` staff only
- `POST /api/payments/{id}/reject_offline/` staff only

## Notes for evaluation

The project contains a real Django/DRF implementation and is suitable for demonstration without real external credentials. For final instructor review, use demo tokens for repeatable tests, or configure real Google/Stripe sandbox credentials in `.env`.
