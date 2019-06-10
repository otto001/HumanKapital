from django.db import models
from rest_framework import serializers


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
    value = models.IntegerField()
    percent = models.IntegerField()

    bio = models.TextField(blank=True)

    @property
    def name(self):
        return self.first_name + " " + self.last_name

    def __str__(self):
        return self.name


class JobSerializer(serializers.ModelSerializer):
    class Meta:
        model = Job
        fields = ("id", "risk", "name")


class HabitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Habit
        fields = ("id", "risk", "name")


class PsychologicalAttributesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Habit
        fields = ("id", "risk", "name")


class PersonSerializer(serializers.ModelSerializer):
    job = JobSerializer()
    psychological_attributes = PsychologicalAttributesSerializer(many=True)
    habits = HabitSerializer(many=True)

    class Meta:
        model = Person
        fields = ("id", "first_name", "last_name", "age", "salary_year", "gender", "social_background", "job", "alive",
                  "psychological_attributes", "habits")

