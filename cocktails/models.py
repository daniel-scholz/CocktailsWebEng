
from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse

# all tables which are represented in the database via a orm model


class Cocktail(models.Model):
    name = models.CharField(max_length=250, unique=True)
    picture = models.ImageField()
    drunk_rating = models.FloatField(default=0)
    taste_rating = models.IntegerField(default=0)
    creator = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    timestamp = models.DateField(auto_now_add=True)

    def get_absolute_url(self):
        return reverse("cocktails:detail", kwargs={'pk': self.pk})

    def __str__(self):
        return self.name

# 
class Ingredient(models.Model):
    name = models.CharField(max_length=250)
    amount = models.FloatField(default=0)
    unit = models.CharField(max_length=10)
    cocktail = models.ForeignKey(
        Cocktail, null=True, blank=True, on_delete=models.CASCADE)
    is_alcohol = models.BooleanField(default=False)
    on_shopping_list_of = models.ForeignKey(
        User, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return "%d %s in %s" % (self.id, self.name, self.cocktail)


class Vote(models.Model):
    voter = models.ForeignKey(User, on_delete=models.CASCADE)
    cocktail = models.ForeignKey(Cocktail, on_delete=models.CASCADE)
    is_upvote = models.BooleanField(default=False)

    def __str__(self):
        if self.is_upvote:
            vote = "up"
        else:
            vote = "down"
        return "%s on %s by %s" % (vote, self.cocktail, self.voter)
