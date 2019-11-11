from django.db import models

class FavouritePlan(models.Model):

    from_location = models.CharField(max_length=100)
    to_location   = models.CharField(max_length=100)
