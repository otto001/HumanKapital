from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_jwt.views import JSONWebTokenAPIView
from rest_framework_jwt.serializers import JSONWebTokenSerializer, RefreshJSONWebTokenSerializer
from rest_framework_jwt.settings import api_settings
from datetime import datetime


class CookieTokenView(JSONWebTokenAPIView):
    def post(self, request, *args, **kwargs):
        try:
            token = request.COOKIES["jwt"]
        except KeyError:
            return Response("No Token", status=status.HTTP_400_BAD_REQUEST)
        request.data["token"] = token
        return super().post(request, *args, **kwargs)


class RefreshTokenView(CookieTokenView):
    serializer_class = RefreshJSONWebTokenSerializer


class ObtainTokenView(JSONWebTokenAPIView):
    serializer_class = JSONWebTokenSerializer


class DeleteTokenView(APIView):
    permission_classes = ()
    authentication_classes = ()

    def post(self, request, *args, **kwargs):
        try:
            token = request.COOKIES["jwt"]
        except KeyError:
            return Response("No Token", status=status.HTTP_400_BAD_REQUEST)

        response = Response("", status=status.HTTP_200_OK)
        expiration = (datetime.utcnow() +
                      api_settings.JWT_EXPIRATION_DELTA)
        response.set_cookie(api_settings.JWT_AUTH_COOKIE,
                            "loggedout",
                            expires=expiration,
                            httponly=True)
        return response

