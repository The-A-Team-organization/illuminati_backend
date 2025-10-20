from .models import User, InvitedUser
from .passwords import hash_password, check_password
import jwt
from django.conf import settings
from datetime import datetime, timedelta
from enums.roles import Role


def generate_jwt(user, lifetime_minutes = 60):
    payload = {
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "exp": datetime.utcnow() + timedelta(minutes = lifetime_minutes)
    }

    token = jwt.encode(payload, settings.SECRET_KEY, algorithm = "HS256")
    return token


def register_user(username, email, password, role=None):
    invited_record = InvitedUser.objects.filter(email = email).first()

    if not invited_record:
        raise ValueError("Email is not invited")

    hashed_password = hash_password(password)

    user = User.objects.create(
        username = username,
        email = email,
        password = hashed_password,
        role = Role.MASON.value
    )


    invited_record.delete()

    token = generate_jwt(user)
    return user, token


def authenticate_user(email, password):
    try:
        user = User.objects.get(email = email)

        if check_password(password, user.password):
            token = generate_jwt(user)
            return user, token

        return None, None

    except User.DoesNotExist:
        return None, None
