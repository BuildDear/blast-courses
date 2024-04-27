from google.oauth2 import id_token
import requests
from rest_framework.exceptions import AuthenticationFailed

from blast_courses import settings
from users import serializers
from users.models import User
from users.services import base_auth


def check_google_auth(google_user: serializers.GoogleAuth) -> dict:
    try:
        id_token.verify_oauth2_token(
            google_user["token"], requests.Request(), settings.GOOGLE_CLIENT_ID
        )
    except ValueError:
        raise AuthenticationFailed(code=403, detail="Dad data google")

    user, _ = User.objects.get_or_create(email=google_user["email"])
    return base_auth.create_token(user.id)
