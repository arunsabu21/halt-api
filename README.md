<div align="center">

# Halt API

**A scalable Bus Booking REST API**

Built with Django, Django REST Framework, PostgreSQL, Redis, Celery, Stripe, Resend, and JWT Authentication.

![Python](https://img.shields.io/badge/Python-3.14-blue?logo=python)
![Django](https://img.shields.io/badge/Django-5.x-092E20?logo=django)
![DRF](https://img.shields.io/badge/DRF-REST%20API-red)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Database-336791?logo=postgresql)
![Redis](https://img.shields.io/badge/Redis-Cache-DC382D?logo=redis)
![Celery](https://img.shields.io/badge/Celery-Task%20Queue-37814A?logo=celery)
![Stripe](https://img.shields.io/badge/Stripe-Payments-635BFF?logo=stripe)
![Resend](https://img.shields.io/badge/Resend-Email-black?logo=resend)
![JWT](https://img.shields.io/badge/JWT-SimpleJWT-black)
![Docker](https://img.shields.io/badge/Docker-Containerization-2496ED?logo=docker)

</div>

---

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Architecture](#architecture)
- [Project Structure](#project-structure)
- [Authentication Flow](#authentication-flow)
- [Booking Flow](#booking-flow)
- [API Documentation](#api-documentation)
- [Environment Variables](#environment-variables)
- [Installation](#installation)
- [Docker](#docker)
- [Testing](#testing)
- [Roadmap](#roadmap)
- [Author](#author)

---

## Overview

Halt is a scalable Bus Booking REST API built with Django and Django REST Framework.

The project follows a service-oriented architecture that separates business logic into services, serializers, and views for better maintainability, scalability, and testability.

---

## Features

### Authentication

- User registration
- Email OTP verification
- JWT authentication
- Login and logout
- JWT token blacklisting
- Forgot password and password reset
- Login attempt rate limiting
- Redis-based OTP storage

### Bus Management

- Cities
- Operators
- Routes
- Buses
- Trips
- Trip search

### Booking System

- Seat availability
- Seat selection
- Booking creation and cancellation
- Booking history
- Booking reference generation
- Seat validation

### Payments

- Stripe Payment Intents
- Stripe Webhooks
- Payment status handling

### Email

- Resend email integration
- OTP verification emails
- Password reset emails
- Email attachments

### Performance

- Redis-based caching
- Cached trip search
- Optimized database queries
- Celery background tasks

### Security

- Custom user model
- Password hashing
- Django password validators
- JWT authentication
- Token blacklisting
- Environment-based configuration
- Login rate limiting

### Production

- Gunicorn production server
- Docker configuration
- Dockerfile
- `.dockerignore`
- Entrypoint script

---

## Tech Stack

| Category          | Technology            |
| ----------------- | --------------------- |
| Language          | Python 3.14           |
| Framework         | Django 5.x            |
| API               | Django REST Framework |
| Database          | PostgreSQL            |
| Cache             | Redis                 |
| Task Queue        | Celery                |
| Authentication    | SimpleJWT             |
| Email             | Resend                |
| Payments          | Stripe                |
| Production Server | Gunicorn              |
| Containerization  | Docker                |
| API Testing       | Bruno / Postman       |

---

## Architecture

```text
Client
  │
  ▼
Views
  │
  ▼
Services
  │
  ▼
Models
  │
  ▼
PostgreSQL

Redis ──► Caching / OTP / Celery
Celery ──► Background Tasks
Resend ──► Email
Stripe ──► Payments
```

---

## Project Structure

```text
halt-api/
├── src/
│   ├── authentication/
│   ├── bookings/
│   ├── buses/
│   ├── cities/
│   ├── operators/
│   ├── routes/
│   ├── trips/
│   ├── core/
│   │   ├── cache/
│   │   ├── constants/
│   │   └── settings.py
│   └── manage.py
│
├── docs/
├── Dockerfile
├── .dockerignore
├── entrypoint.sh
├── requirements.txt
├── .env.example
├── .gitignore
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
Send OTP with Resend
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
JWT Authentication
  │
  ▼
Protected APIs
```

---

## Booking Flow

```text
Search Trip
  │
  ▼
View Seats
  │
  ▼
Select Seats
  │
  ▼
Validate Seats
  │
  ▼
Create Booking
  │
  ▼
Reserve Seats
  │
  ▼
Payment
  │
  ▼
Booking Confirmed
```

---

## API Documentation

Full API documentation is available in the [`docs/`](./docs) directory.

Documentation includes:

- Authentication
- Cities
- Operators
- Routes
- Buses
- Trips
- Bookings

---

## Environment Variables

Create a `.env` file in the project root.

```env
SECRET_KEY=
DEBUG=True

DB_NAME=
DB_USER=
DB_PASSWORD=
DB_HOST=
DB_PORT=

REDIS_URL=

RESEND_API_KEY=
RESEND_FROM_EMAIL=

STRIPE_SECRET_KEY=
STRIPE_WEBHOOK_SECRET=

LOGIN_ATTEMPT_LIMIT=5
LOGIN_ATTEMPT_TIMEOUT=300

OTP_TIMEOUT=300
FORGOT_TOKEN_TIMEOUT=900
```

> Never commit `.env` or production secrets to Git.

---

## Installation

### Clone the Repository

```bash
git clone <repository-url>
cd halt-api
```

### Create Virtual Environment

```bash
python -m venv .venv
```

### Activate Virtual Environment

Linux / macOS:

```bash
source .venv/bin/activate
```

Windows:

```powershell
.venv\Scripts\activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Run Migrations

```bash
python manage.py migrate
```

### Start Development Server

```bash
python manage.py runserver
```

---

## Docker

Halt includes Docker configuration for containerized deployment.

### Docker Files

```text
Dockerfile
.dockerignore
entrypoint.sh
```

### Build Image

```bash
docker build -t halt-api .
```

### Run Container

```bash
docker run --env-file .env -p 8000:8000 halt-api
```

Gunicorn is used as the production application server.

---

## Testing

API testing can be performed using:

- Bruno
- Postman
- Insomnia
- cURL
- Thunder Client

Run Django tests with:

```bash
python manage.py test
```

---

## Roadmap

- [x] Authentication
- [x] Email OTP verification
- [x] Redis integration
- [x] Celery integration
- [x] Resend email integration
- [x] Email attachments
- [x] Stripe payments
- [x] Stripe webhooks
- [x] Ticket generation
- [x] Gunicorn
- [x] Docker configuration
- [ ] Pagination
- [ ] Filtering
- [ ] Notifications
- [ ] CI/CD
- [ ] Production deployment
- [ ] Monitoring and logging

---

## Author

**Arun**

Software Engineer

Backend-focused developer working with Python, Django, REST APIs, PostgreSQL, Redis, Docker, and cloud technologies.
