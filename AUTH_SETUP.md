# Auth Setup

## Environment

Create a `.env` file in the project root and provide the existing database settings plus a JWT secret:

```env
user=your_database_user
password=your_database_password
host=your_database_host
port=5432
dbname=your_database_name
JWT_SECRET_KEY=replace-with-a-long-random-secret
APP_PORT=8000
```

## First Super Admin

There is no public signup for `super_admin`. Create the first one manually from a Flask shell after the tables exist.

```python
from auth_models import AuthUser, ROLE_SUPER_ADMIN
from extensions import db

super_admin = AuthUser(
    username="Super Admin",
    email="superadmin@example.com",
    role=ROLE_SUPER_ADMIN,
)
super_admin.set_password("change-this-password")

db.session.add(super_admin)
db.session.commit()
```

After that, the super admin can create admin accounts through `POST /api/auth/admins` with:

```json
{
  "username": "Admin User",
  "email": "admin@example.com",
  "password": "admin-password"
}
```

The API also accepts `name` during admin creation for compatibility, but `username` is the preferred field.

Admins sign in through `POST /api/auth/login` using:

```json
{
  "email": "admin@example.com",
  "password": "admin-password"
}
```

## Logout Behavior

`POST /api/auth/logout` is client-side only in this version. The frontend should remove the stored access and refresh tokens after logout.

## Password Management

Logged-in users can change their own password through `POST /api/auth/change-password`:

```json
{
  "current_password": "old-password",
  "new_password": "new-password"
}
```

Forgot password is handled in two steps:

1. Request a reset token with `POST /api/auth/forgot-password`

```json
{
  "email": "admin@example.com"
}
```

2. Use that token with `POST /api/auth/reset-password`

```json
{
  "token": "reset-token-from-forgot-password",
  "new_password": "new-password"
}
```

For now, the reset token is returned directly by the backend so you can test the flow and wire email delivery later.
