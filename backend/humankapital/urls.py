from django.contrib import admin
from django.urls import path, re_path
from .views import app_view, test_view
from .jwt.rest import RefreshTokenView, ObtainTokenView, DeleteTokenView
# handler404 = app_view
from .tick import start

start()
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', app_view),
    path('test', test_view),
    path("auth/token/obtain", ObtainTokenView.as_view()),
    path("auth/token/refresh", RefreshTokenView.as_view()),
    path("auth/token/delete", DeleteTokenView.as_view()),
]
