from django.contrib import admin
from django.urls import path, re_path
from .views import market_view, test_view
from .jwt.rest import RefreshTokenView, ObtainTokenView, DeleteTokenView
# handler404 = app_view
from .tick import start
from .api import ListPersonsApi, ListPersonToBuyApi, ListPersonBoughtApi, ListEventApi, ListPlayerApi, \
    AcquisitionCreateApi, PersonSellApi

start()
urlpatterns = [
    path('admin/', admin.site.urls),
    path('market', market_view),
    path('test', test_view),

    path("api/persons", ListPersonsApi.as_view()),
    path("api/persons/tobuy", ListPersonToBuyApi.as_view()),
    path("api/persons/bought", ListPersonBoughtApi.as_view()),
    path("api/events", ListEventApi.as_view()),
    path("api/player", ListPlayerApi.as_view()),

    path("api/acquisition/create", AcquisitionCreateApi.as_view()),
    path("api/person/<int:person>/sell", PersonSellApi.as_view()),

    path("auth/token/obtain", ObtainTokenView.as_view()),
    path("auth/token/refresh", RefreshTokenView.as_view()),
    path("auth/token/delete", DeleteTokenView.as_view()),
]
