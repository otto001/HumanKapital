from rest_framework import generics
from rest_framework import views
from .models.person import Person, PersonSerializer
from django.db.models import Q
from .models.events import Event, EventSerializer
from .models.player import Player, PlayerSerializer
from .models.acquisition import Acquisition, AcquisitionSerializer
from django.utils import timezone


class ListPersonsApi(generics.ListAPIView):
    queryset = Person.objects.all()
    serializer_class = PersonSerializer


class ListPersonToBuyApi(generics.ListAPIView):
    queryset = Person.objects.all()
    serializer_class = PersonSerializer

    def filter_queryset(self, queryset):
        return queryset.filter(Q(acquisitions__sold__isnull=False) | Q(acquisitions__isnull=True))


class ListPersonBoughtApi(generics.ListAPIView):
    queryset = Person.objects.all()
    serializer_class = PersonSerializer

    def filter_queryset(self, queryset):
        return queryset.filter(Q(acquisitions__sold__isnull=True) & Q(acquisitions__isnull=False))


class ListEventApi(generics.ListAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer


class ListPlayerApi(generics.ListAPIView):
    queryset = Player.objects.all()
    serializer_class = PlayerSerializer


class AcquisitionCreateApi(generics.CreateAPIView):
    queryset = Acquisition.objects.all()
    serializer_class = AcquisitionSerializer

    def perform_create(self, serializer):
        return serializer.save(created=timezone.now())


class PersonSellApi(views.APIView):

    def post(self, request, *args, **kwargs):
        person_id = kwargs["person"]
        acquisitions = Acquisition.objects.filter(person_id=person_id, sold__isnull=True)
        acquisitions.update(sold=timezone.now())
