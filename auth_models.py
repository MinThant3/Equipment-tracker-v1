from datetime import datetime
from uuid import uuid4

from werkzeug.security import check_password_hash, generate_password_hash

from extensions import db


ROLE_SUPER_ADMIN = "super_admin"
ROLE_ADMIN = "admin"


def generate_uuid():
    return str(uuid4())


class AuthUser(db.Model):
    __tablename__ = "auth_users"

    id = db.Column(db.String(36), primary_key=True, default=generate_uuid)
    username = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.Text, nullable=False)
    role = db.Column(db.String(20), nullable=False, default=ROLE_ADMIN)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
    )

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    @property
    def name(self):
        return self.username

    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "name": self.username,
            "email": self.email,
            "role": self.role,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }

    @classmethod
    def get_by_email(cls, email):
        return cls.query.filter_by(email=email).first()
