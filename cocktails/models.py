from django.db import models


# Create your models here.


class Cocktail(models.Model):
    name = models.CharField(max_length = 250)
    rating = models.IntegerField()
    picture = models.CharField(max_length = 100000)

    def __str__(self):
        return "%s (Rating: %d)" % (self.name, self.rating)


class Ingredient(models.Model):
    name = models.CharField(max_length = 250)
    weight = models.FloatField(null = True)
    quantity = models.FloatField(null = True)
    cocktails = models.ManyToManyField(Cocktail)
    is_alcohol = models.BooleanField(default = False)

    def __str__(self):
        return self.name

#class Ingredient_Coktail(models.Model):
#   c_name = models.ForeignKey(Cocktail, on_delete = models.CASCADE)
#  i_name = models.ForeignKey(Ingredient, on_delete = models.CASCADE)
  
