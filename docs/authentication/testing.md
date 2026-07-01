# Authentication Testing

## Register

- [x] Register with valid details
- [x] Register with existing email
- [x] Register with existing phone
- [x] Register with invalid email

---

## OTP Verification

- [x] Verify with correct OTP
- [x] Verify with incorrect OTP
- [x] Verify with expired OTP
- [x] Verify OTP twice

---

## Login

- [x] Login with valid credentials
- [x] Login with wrong password
- [x] Login with unknown email
- [x] Login with unverified account
- [x] Login rate limit (3 attempts)

---

## WhoAmI

- [x] Valid access token
- [x] No token
- [x] Invalid token
- [x] Expired token

---

## Logout

- [x] Valid refresh token
- [x] Reuse blacklisted refresh token

---

## Forgot Password

- [x] Existing verified user
- [x] User doesn't exist
- [x] User not verified

---

## Reset Password

- [x] Valid reset token
- [x] Invalid token
- [x] Expired token
- [x] Reused token
- [x] Same as old password
- [x] Password mismatch