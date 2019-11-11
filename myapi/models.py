from django.db import models

class FavouritePlan(models.Model):

    from_location = models.CharField(max_length=100)
    to_location   = models.CharField(max_length=100)
    fav_flag = models.BooleanField(default=False)

    def to_dict(self):
        return dict(from_location=self.from_location, to_location=self.to_location, fav=self.fav_flag)

    def __str__(self):
        return str(self.to_dict())