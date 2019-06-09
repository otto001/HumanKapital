from django.db import models
from .player import Player
from .person import Person


class Acquisition(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE, related_name="acquisitions")
    person = models.ForeignKey(Person, on_delete=models.CASCADE, related_name="acquired_by")
    percent = models.IntegerField()
    price = models.IntegerField()
    created = models.DateTimeField(auto_created=True)
    sold = models.DateTimeField(default=None, null=True)

