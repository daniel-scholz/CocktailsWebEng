from django.db import models


# Create your models here.
class Cocktails(models.Model):
    name = models.CharField(max_length=250)
    rating = models.IntegerField()
    picture = models.CharField(max_length=100000)


class Ingredients(models.Model):
    name = models.ForeignKey(Cocktails, on_delete=models.CASCADE())
