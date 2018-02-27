from django.db import models

# Create your models here.
import cocktails


class Cocktail(models.Model):
    name = models.CharField(max_length=250)
    rating = models.IntegerField()
    picture = models.CharField(max_length=100000)

    def __str__(self):
        return "%s is rated %d" % (self.name, self.rating)


class Ingredients(models.Model):
    name = models.ForeignKey("Cocktail", on_delete=models.CASCADE)
    weight = models.FloatField(null=True)
    quantity = models.FloatField(null=True)
