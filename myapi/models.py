from django.db import models
from django.utils import timezone


class Hero(models.Model):
    name = models.CharField(max_length=60)
    alias = models.CharField(max_length=60)

    creation_date = models.DateTimeField("created",
                                         default=timezone.now(),
                                         help_text="creation datetime")
    modified_date = models.DateTimeField("modified",
                                         auto_now=True,
                                         help_text="last modified datetime")

    def to_dict(self):
        return dict(name=self.name, alias=self.alias)

    def __str__(self):
        return str(self.to_dict())