# Bus Booking API

A scalable and secure backend API for a Bus Booking System built with **Django**, **Django REST Framework**, **PostgreSQL**, **Redis**, and **JWT Authentication**.

The project follows a clean architecture by separating business logic into service layers, serializers, and views for better maintainability and scalability.

---

## Features

### Authentication

- User Registration
- Email OTP Verification
- JWT Authentication
- Login
- Logout (Token Blacklisting)
- Forgot Password
- Password Reset
- Password Validation
- Login Attempt Rate Limiting
- Redis-based OTP Storage

### Security

- Custom User Model
- JWT Access & Refresh Tokens
- Password Hashing
- Django Password Validators
- Redis Token Expiration
- Environment Variable Configuration

### Backend

- Django REST Framework
- PostgreSQL Database
- Redis Cache
- Service Layer Architecture
- Clean API Responses

---

## 🛠 Tech Stack

| Technology            | Purpose               |
| --------------------- | --------------------- |
| Python                | Programming Language  |
| Django                | Backend Framework     |
| Django REST Framework | REST API              |
| PostgreSQL            | Database              |
| Redis                 | OTP & Cache           |
| Simple JWT            | Authentication        |
| python-decouple       | Environment Variables |

---

## Project Structure

```text
bus-booking-api/
│
├── authentication/
│   ├── managers.py
│   ├── models.py
│   ├── serializers.py
│   ├── services.py
│   ├── views.py
│   ├── urls.py
│   └── migrations/
│
├── core/
│
├── docs/
│
├── requirements.txt
├── manage.py
└── README.md
```

---

## Authentication Flow

```text
Register
      │
      ▼
Generate OTP
      │
      ▼
Store OTP in Redis
      │
      ▼
Send OTP Email
      │
      ▼
Verify OTP
      │
      ▼
Activate Account
      │
      ▼
Login
      │
      ▼
JWT Access & Refresh Token
      │
      ▼
Protected APIs
```

---

## Authentication Endpoints

| Method | Endpoint                     | Description              |
| ------ | ---------------------------- | ------------------------ |
| POST   | `/api/auth/register/`        | Register User            |
| POST   | `/api/auth/verify-otp/`      | Verify Email OTP         |
| POST   | `/api/auth/login/`           | User Login               |
| POST   | `/api/auth/logout/`          | User Logout              |
| GET    | `/api/auth/whoami/`          | Current User             |
| POST   | `/api/auth/forgot-password/` | Send Password Reset Link |
| POST   | `/api/auth/reset-password/`  | Reset Password           |

---

## Environment Variables

Create a `.env` file.

```env
SECRET_KEY=

DEBUG=True

DB_NAME=
DB_USER=
DB_PASSWORD=
DB_HOST=
DB_PORT=

REDIS_URL=

LOGIN_ATTEMPT_LIMIT=5
LOGIN_ATTEMPT_TIMEOUT=300

OTP_TIMEOUT=300

FORGOT_TOKEN_TIMEOUT=900
```

---

## Installation

Clone the repository

```bash
git clone <repository-url>
```

Move into the project

```bash
cd bus-booking-api
```

Create virtual environment

```bash
python -m venv .venv
```

Activate virtual environment

Linux / macOS

```bash
source .venv/bin/activate
```

Windows

```bash
.venv\Scripts\activate
```

Install dependencies

```bash
pip install -r requirements.txt
```

Apply migrations

```bash
python manage.py migrate
```

Run the server

```bash
python manage.py runserver
```

---

## Testing

The API can be tested using:

- Bruno
- Postman
- Insomnia
- cURL

---

## Future Roadmap

- Bus Management
- Route Management
- Seat Management
- Booking System
- Payment Integration
- Ticket Generation
- Admin Dashboard
- Notifications

---

## Author

**Arun**

Backend Developer focused on building scalable REST APIs with Django and Python.

---
