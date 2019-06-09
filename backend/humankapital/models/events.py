from django.db import models
from .person import Person


class AbstractEvent(models.Model):
    class Meta:
        abstract = True
    person = models.ForeignKey(Person, on_delete=models.CASCADE)


class UnfortunateEvent(AbstractEvent):
    death = models.BooleanField()
    reason = models.CharField(max_length=128)
    text = models.TextField()
