from django.db import models
from django.urls import reverse


# Create your models here.


class Cocktail(models.Model):
    name = models.CharField(max_length=250, unique=True)
    rating = models.IntegerField(null=True)
    picture = models.FileField()

    def get_absolute_url(self):
        try:
            ret = reverse("cocktails:detail", kwargs={'pk': self.pk})
        except:
            ret = "http://localhost:8000/cocktails/6/"

        return ret

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    name = models.CharField(max_length=250)
    weight = models.FloatField(null=True)
    quantity = models.FloatField(null=True)
    cocktail = models.ManyToManyField(Cocktail)
    is_alcohol = models.BooleanField(default=False)

    def __str__(self):
        return self.name  # + ("%s" % self.is_alcohol)
