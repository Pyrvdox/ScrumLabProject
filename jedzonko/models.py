from django.db import models

# Create your models here.
class Recipe(models.Model):
    name = models.CharField(max_length=255)
    ingredients = models.TextField()
    description = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    preparation_time = models.PositiveIntegerField()
    votes = models.IntegerField(default=0)

class Dayname(models.Model):
    DAYSNAME = (
        (1, 'Monday'),
        (2, 'Tuesday'),
        (3, 'Wednesday'),
        (4,'Thursday'),
        (5, 'Friday'),
        (6, 'Saturday'),
        (7, 'Sunday'),

    )
    name = models.IntegerField(choices=DAYSNAME)
    order = models.IntegerField(unique=True)


class Recipeplan(models.Model):
    meal_name = models.CharField(max_length=255)
    order = models.IntegerField()
    recipe = models.ForeignKey('Recipe', on_delete=models.CASCADE)
    plan = models.ForeignKey('Plan', on_delete=models.CASCADE)
    day_name = models.ForeignKey('Dayname', on_delete=models.CASCADE)

class Plan(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    recipes = models.ManyToManyField(Recipe, through=Recipeplan, related_name="recipes")


class Page(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()