<div align="center">

# Halt API

**A scalable, production-ready Bus Booking REST API**

Built with Django, Django REST Framework, PostgreSQL, Redis, and JWT Authentication.

![Python](https://img.shields.io/badge/Python-3.14-blue?logo=python)
![Django](https://img.shields.io/badge/Django-5.x-092E20?logo=django)
![Django REST Framework](https://img.shields.io/badge/DRF-REST%20API-red)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Database-336791?logo=postgresql)
![Redis](https://img.shields.io/badge/Redis-Cache-DC382D?logo=redis)
![Celery](https://img.shields.io/badge/Celery-Task%20Queue-37814A?logo=celery&logoColor=white)
![Stripe](https://img.shields.io/badge/Stripe-Payments-635BFF?logo=stripe&logoColor=white)
![JWT](https://img.shields.io/badge/JWT-SimpleJWT-black)
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
- [Testing](#testing)
- [Roadmap](#roadmap)
- [Author](#author)

---

## Overview

Halt is a scalable, production-ready Bus Booking REST API built with Django, Django REST Framework, PostgreSQL, Redis, and JWT Authentication.

The project follows a clean architecture that separates business logic into **services**, **serializers**, and **views**, ensuring maintainability, scalability, and testability.

---

## Features

### Authentication

- User registration
- Email OTP verification
- JWT authentication
- Login / logout with token blacklisting
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

### Performance

- Redis-based trip search caching
- Optimized database queries
- Service layer architecture

### Security

- Custom user model
- Password hashing
- Django password validators
- Environment-based configuration
- JWT access and refresh tokens
- Redis-backed caching

---

## Tech Stack

| Category       | Technology            |
| -------------- | --------------------- |
| Language       | Python                |
| Framework      | Django                |
| API            | Django REST Framework |
| Database       | PostgreSQL            |
| Cache          | Redis                 |
| Task Queue     | Celery                |
| Authentication | SimpleJWT             |
| Stripe         | Payment               |

---

## Architecture

```text
Client
  │
Views
  │
Services
  │
Models
  │
PostgreSQL
```

---

## Project Structure

```text
src/
├── authentication/
├── bookings/
├── buses/
├── cities/
├── operators/
├── routes/
├── trips/
├── core/
│   ├── cache/
│   ├── constants/
│   └── settings.py
└── manage.py
```

---

## Authentication Flow

```text
Register
  │
Generate OTP
  │
Store OTP (Redis)
  │
Verify OTP
  │
Activate Account
  │
Login
  │
JWT Authentication
  │
Protected APIs
```

---

## Booking Flow

```text
Search Trip
  │
View Seats
  │
Select Seats
  │
Create Booking
  │
Reserve Seats
  │
Cancel Booking
  │
Release Seats
```

---

## API Documentation

Full API documentation is available in the [`docs/`](./docs) directory, covering:

- Authentication
- Cities
- Operators
- Routes
- Buses
- Trips
- Bookings

Each module includes endpoint documentation and testing guides.

---

## Environment Variables

Create a `.env` file in the project root with the following variables:

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

```bash
git clone <repository-url>
cd halt-api

python -m venv .venv
source .venv/bin/activate

pip install -r requirements.txt

python manage.py migrate
python manage.py runserver
```

---

## Testing

API testing can be performed using any of the following tools:

- Bruno
- Postman
- Insomnia
- cURL
- Thunder Client

---

## Roadmap

- [x] Payment integration
- [x] Ticket generation
- [ ] Notifications
- [ ] Pagination
- [ ] Filtering
- [ ] Docker
- [ ] CI/CD
- [ ] Deployment

---

## Author

**Arun**

Software Engineer
