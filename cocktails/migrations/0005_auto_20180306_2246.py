# Generated by Django 2.0.2 on 2018-03-06 21:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cocktails', '0004_ingredients_coktails'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Ingredients',
            new_name='Ingredient',
        ),
        migrations.RenameModel(
            old_name='Ingredients_Coktails',
            new_name='Ingredient_Coktail',
        ),
    ]

    atomic = False