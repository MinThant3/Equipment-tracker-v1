from functools import wraps

from flask import Blueprint, jsonify, request
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    current_user,
    get_jwt_identity,
    jwt_required,
)

from auth_models import (
    AuthUser,
    ROLE_ADMIN,
    ROLE_SUPER_ADMIN,
)
from extensions import db, jwt


auth_bp = Blueprint("auth", __name__)


def normalize_text(value):
    if not isinstance(value, str):
        return None
    normalized_value = value.strip()
    return normalized_value or None


def normalize_email(value):
    normalized_email = normalize_text(value)
    if normalized_email is None:
        return None
    return normalized_email.lower()


def error_response(message, status_code, error=None):
    payload = {"message": message}
    if error:
        payload["error"] = error
    return jsonify(payload), status_code


def get_login_credentials():
    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        return None, None, error_response("Request body must be valid JSON", 400, "invalid_payload")

    email = normalize_email(data.get("email"))
    password = data.get("password")

    if email is None:
        return None, None, error_response("Email is required", 400, "email_required")
    if not isinstance(password, str) or not password.strip():
        return None, None, error_response("Password is required", 400, "password_required")

    return email, password, None


def get_admin_creation_payload():
    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        return None, None, None, error_response("Request body must be valid JSON", 400, "invalid_payload")

    username = normalize_text(data.get("username")) or normalize_text(data.get("name"))
    email = normalize_email(data.get("email"))
    password = data.get("password")

    if username is None:
        return None, None, None, error_response("Username is required", 400, "username_required")
    if email is None:
        return None, None, None, error_response("Email is required", 400, "email_required")
    if not isinstance(password, str) or not password.strip():
        return None, None, None, error_response("Password is required", 400, "password_required")

    return username, email, password, None


def get_change_password_payload():
    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        return None, None, error_response("Request body must be valid JSON", 400, "invalid_payload")

    current_password = data.get("current_password")
    new_password = data.get("new_password")

    if not isinstance(current_password, str) or not current_password.strip():
        return None, None, error_response("Current password is required", 400, "current_password_required")
    if not isinstance(new_password, str) or not new_password.strip():
        return None, None, error_response("New password is required", 400, "new_password_required")

    return current_password, new_password, None


def super_admin_required(view):
    @wraps(view)
    @jwt_required()
    def wrapped_view(*args, **kwargs):
        if current_user is None:
            return error_response("Authenticated user no longer exists", 401, "user_not_found")
        if current_user.role != ROLE_SUPER_ADMIN:
            return error_response("Super admin access required", 403, "super_admin_required")
        return view(*args, **kwargs)

    return wrapped_view


@jwt.user_lookup_loader
def user_lookup_callback(_jwt_headers, jwt_data):
    identity = jwt_data["sub"]
    return db.session.get(AuthUser, identity)


@jwt.user_lookup_error_loader
def user_lookup_error_callback(_jwt_headers, _jwt_data):
    return error_response("Authenticated user no longer exists", 401, "user_not_found")


@jwt.additional_claims_loader
def add_claims_to_access_token(identity):
    user = db.session.get(AuthUser, identity)
    if user is None:
        return {}
    return {
        "role": user.role,
        "email": user.email,
        "username": user.username,
    }


@jwt.expired_token_loader
def expired_token_callback(_jwt_header, _jwt_data):
    return error_response("Token has expired", 401, "token_expired")


@jwt.invalid_token_loader
def invalid_token_callback(_error):
    return error_response("Token is invalid", 401, "invalid_token")


@jwt.unauthorized_loader
def missing_token_callback(_error):
    return error_response("Request is missing an authorization token", 401, "authorization_header")


@auth_bp.post("/admins")
@super_admin_required
def create_admin():
    username, email, password, validation_error = get_admin_creation_payload()
    if validation_error:
        return validation_error

    existing_user = AuthUser.get_by_email(email)
    if existing_user:
        return error_response("An account with this email already exists", 409, "account_exists")

    new_user = AuthUser(username=username, email=email, role=ROLE_ADMIN)
    new_user.set_password(password)
    db.session.add(new_user)
    db.session.commit()

    return (
        jsonify(
            {
                "message": "Admin account created successfully",
                "user": new_user.to_dict(),
            }
        ),
        201,
    )


@auth_bp.post("/login")
def login():
    email, password, validation_error = get_login_credentials()
    if validation_error:
        return validation_error

    user = AuthUser.get_by_email(email)
    if user is None or not user.check_password(password):
        return error_response("Invalid email or password", 401, "invalid_credentials")

    access_token = create_access_token(identity=user.id)
    refresh_token = create_refresh_token(identity=user.id)

    return (
        jsonify(
            {
                "message": "Logged in successfully",
                "tokens": {"access": access_token, "refresh": refresh_token},
                "user": user.to_dict(),
            }
        ),
        200,
    )
@auth_bp.get("/whoami")
@jwt_required()
def whoami():
    return jsonify({"user": current_user.to_dict()}), 200


@auth_bp.post("/change-password")
@jwt_required()
def change_password():
    current_password, new_password, validation_error = get_change_password_payload()
    if validation_error:
        return validation_error

    user = current_user
    if user is None:
        return error_response("Authenticated user no longer exists", 401, "user_not_found")
    if not user.check_password(current_password):
        return error_response("Current password is incorrect", 401, "invalid_current_password")

    user.set_password(new_password)
    db.session.commit()

    return jsonify({"message": "Password changed successfully"}), 200


@auth_bp.post("/refresh")
@jwt_required(refresh=True)
def refresh_access_token():
    user = current_user
    if user is None:
        return error_response("Authenticated user no longer exists", 401, "user_not_found")

    access_token = create_access_token(identity=get_jwt_identity())
    return jsonify({"access_token": access_token}), 200


@auth_bp.post("/logout")
@jwt_required(verify_type=False)
def logout():
    return jsonify({"message": "Logout successful. Remove the token on the client."}), 200
