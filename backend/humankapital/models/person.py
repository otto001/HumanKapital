from django.db import models


social_backgrounds = ["upper", "middle", "lower"]


class BaseAttribute(models.Model):
    class Meta:
        abstract = True
    name = models.CharField(max_length=64)
    risk = models.FloatField()

    def __str__(self):
        return self.name


class Habit(BaseAttribute):
    pass


class Job(BaseAttribute):
    pass


class PsychologicalAttributes(BaseAttribute):
    pass


class Person(models.Model):
    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64)
    age = models.IntegerField()
    salary_year = models.IntegerField()
    gender = models.CharField(max_length=1, choices=list(zip(*(2*[("m", "f", "d")]))))

    social_background = models.CharField(max_length=6, choices=list(zip(*(2*[social_backgrounds]))))

    job = models.ForeignKey(Job, default=None, on_delete=models.SET_DEFAULT)

    habits = models.ManyToManyField(Habit)
    psychological_attributes = models.ManyToManyField(PsychologicalAttributes)

    alive = models.BooleanField(default=True)

    def __str__(self):
        return " ".join((self.first_name, self.last_name))
