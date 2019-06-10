from django.db import models
from .person import Person
from rest_framework import serializers


class Event(models.Model):
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    text = models.TextField()
    positive = models.BooleanField()
    death = models.BooleanField()
    reason = models.CharField(max_length=128)
    decision = models.BooleanField()

    def __str__(self):
        return self.person.name


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ("id", "person", "text", "positive", "death", "reason", "decision")
