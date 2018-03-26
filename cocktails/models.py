from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.urls import reverse


# Create your models here.


class Cocktail(models.Model):
    name = models.CharField(max_length=250, unique=True)
    picture = models.ImageField()
    drunk_scale = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(5)])
    taste_scale = models.IntegerField(default=0)
    creator = models.ForeignKey(User, null=True, on_delete=models.CASCADE)

    def get_absolute_url(self):
        return reverse("cocktails:detail", kwargs={'pk': self.pk})

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    name = models.CharField(max_length=250)
    weight = models.FloatField(null=True, blank=True)
    quantity = models.FloatField(null=True, blank=True)
    volume = models.FloatField(null=True, blank=True)
    cocktail = models.ForeignKey(Cocktail, null=True, blank=True, on_delete=models.CASCADE)
    is_alcohol = models.BooleanField(default=False)

    def __str__(self):
        return self.name
