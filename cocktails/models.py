from django.db import models


# Create your models here.


class Cocktail(models.Model):
    name = models.CharField(max_length=250)
    rating = models.IntegerField()
    picture = models.CharField(max_length=100000)

    def __str__(self):
        return "%s (Rating: %d)" % (self.name, self.rating)


class Ingredients(models.Model):
    name = models.CharField(max_length=250)
    weight = models.FloatField(null=True)
    quantity = models.FloatField(null=True)
