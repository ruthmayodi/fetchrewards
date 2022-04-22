from django.db import models


class Points(models.Model):
    payer = models.CharField(max_length=60)
    points = models.IntegerField(default=0)
    timestamp = models.DateTimeField()

