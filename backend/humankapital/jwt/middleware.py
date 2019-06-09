from rest_framework_jwt.serializers import VerifyJSONWebTokenSerializer
from rest_framework_jwt.settings import api_settings
from channels.security.websocket import WebsocketDenier
from rest_framework.exceptions import ValidationError
from channels.auth import CookieMiddleware


class JwtTokenAuthMiddleware:
    """
    JWT token authorization middleware for Django Channels 2
    """

    def __init__(self, application):
        self.application = application

    def __call__(self, scope):
        try:
            token = scope["cookies"][api_settings.JWT_AUTH_COOKIE]
        except KeyError:
            return WebsocketDenier(scope)

        try:
            data = {'token': token}
            valid_data = VerifyJSONWebTokenSerializer().validate(data)
            user = valid_data['user']
            scope['user'] = user
        except ValidationError:  # invalid token
            return WebsocketDenier(scope)
        except KeyError:  # No user found
            return WebsocketDenier(scope)

        return self.application(scope)


JwtTokenAuthMiddlewareStack = lambda inner: CookieMiddleware(JwtTokenAuthMiddleware(inner))
