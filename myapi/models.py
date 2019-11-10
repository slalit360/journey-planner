from __future__ import unicode_literals
from django.db import models
from django.utils import timezone


class Journey(models.Model):
    journey_from = models.CharField(max_length=30)
    journey_to = models.CharField(max_length=30)
    journey_date = models.DateTimeField(default=timezone.now())

    class Meta:
        db_table = "journey"