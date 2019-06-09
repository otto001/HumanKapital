from rest_framework import generics
from .models.person import Person, PersonSerializer
from django.db.models import Q


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


class List(generics.ListAPIView):
    queryset = Person.objects.all()
    serializer_class = PersonSerializer

    def filter_queryset(self, queryset):
        return queryset.filter(Q(acquisitions__sold__isnull=True) & Q(acquisitions__isnull=False))
