from django.db import models


class Delivery(models.Model):

    status = models.CharField(max_length=100)
    details = models.CharField(max_length=500)
