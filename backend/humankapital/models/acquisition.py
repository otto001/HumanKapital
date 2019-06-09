from django.db import models
from .player import Player
from .person import Person
from rest_framework import serializers


class Acquisition(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE, related_name="acquisitions")
    person = models.ForeignKey(Person, on_delete=models.CASCADE, related_name="acquisitions")
    percent = models.IntegerField()
    price = models.IntegerField()
    created = models.DateTimeField()
    sold = models.DateTimeField(default=None, null=True, blank=True)

    def __str__(self):
        return self.player.email + " <-> " + self.person.name


class AcquisitionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Acquisition
        fields = ("player", "person", "percent", "price")
        read_only_fields = ("created", "sold")
