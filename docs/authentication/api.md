# Authentication API

This document describes all authentication-related endpoints available in the Bus Booking API.

**Base URL**

```
/api/auth/
```

---

# Register

Creates a new user account and sends an OTP to the registered email.

### Endpoint

```http
POST /api/auth/register/
```

### Request

```json
{
    "email": "user@example.com",
    "full_name": "John Doe",
    "phone_number": "9876543210",
    "password": "StrongPassword123!"
}
```

### Success Response

**Status:** `201 Created`

```json
{
    "message": "Registration successful. Please verify your email OTP."
}
```

### Possible Errors

- Email already registered
- Phone number already exists
- Invalid email
- Invalid phone number
- Weak password

---

# Verify OTP

Verifies the OTP sent to the user's email.

### Endpoint

```http
POST /api/auth/verify-otp/
```

### Request

```json
{
    "email": "user@example.com",
    "otp": "123456"
}
```

### Success Response

**Status:** `200 OK`

```json
{
    "message": "Email verified successfully."
}
```

### Possible Errors

- Invalid OTP
- OTP expired
- User not found

---

# Login

Authenticates a verified user and returns JWT access and refresh tokens.

### Endpoint

```http
POST /api/auth/login/
```

### Request

```json
{
    "email": "user@example.com",
    "password": "StrongPassword123!"
}
```

### Success Response

**Status:** `200 OK`

```json
{
    "id": "user-id",
    "email": "user@example.com",
    "full_name": "John Doe",
    "access": "<access_token>",
    "refresh": "<refresh_token>",
    "message": "Logged in successfully."
}
```

### Possible Errors

- User doesn't exist
- Incorrect password
- Account not verified
- Account disabled
- Too many failed login attempts

---

# WhoAmI

Returns the authenticated user's profile.

> Authorization Required

### Endpoint

```http
GET /api/auth/whoami/
```

### Headers

```http
Authorization: Bearer <access_token>
```

### Success Response

**Status:** `200 OK`

```json
{
    "id": "user-id",
    "email": "user@example.com",
    "full_name": "John Doe",
    "phone_number": "9876543210",
    "created_at": "2026-07-01T10:00:00Z"
}
```

---

# Logout

Blacklists the refresh token.

> Authorization Required

### Endpoint

```http
POST /api/auth/logout/
```

### Headers

```http
Authorization: Bearer <access_token>
```

### Request

```json
{
    "refresh": "<refresh_token>"
}
```

### Success Response

**Status:** `200 OK`

```json
{
    "message": "Logged out successfully."
}
```

### Possible Errors

- Invalid refresh token
- Expired refresh token

---

# Forgot Password

Generates a password reset token and sends a reset link via email.

### Endpoint

```http
POST /api/auth/forgot-password/
```

### Request

```json
{
    "email": "user@example.com"
}
```

### Success Response

**Status:** `200 OK`

```json
{
    "message": "Password reset link sent successfully."
}
```

### Possible Errors

- User doesn't exist
- Email not verified

---

# Reset Password

Resets the user's password using the password reset token.

### Endpoint

```http
POST /api/auth/reset-password/
```

### Request

```json
{
    "token": "<reset_token>",
    "new_password": "NewPassword123!",
    "confirm_password": "NewPassword123!"
}
```

### Success Response

**Status:** `200 OK`

```json
{
    "message": "Password reset successfully."
}
```

### Possible Errors

- Invalid or expired reset token
- Passwords do not match
- Weak password
- New password cannot be the same as the current password

---

# Authentication

Protected endpoints require the following header:

```http
Authorization: Bearer <access_token>
```

---

# Technologies Used

- Django
- Django REST Framework
- PostgreSQL
- Redis
- Simple JWT

---

# Notes

- Email verification OTPs are stored in Redis.
- Password reset tokens are stored in Redis with automatic expiration.
- Refresh tokens are blacklisted on logout.
- Login attempts are rate limited using Redis.
- Passwords are securely hashed using Django's authentication system.