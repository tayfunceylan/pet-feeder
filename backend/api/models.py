from django.db import models
from django.utils.timezone import now as time_zone_now


class Pet(models.Model):
    name = models.CharField(max_length=30)
    age = models.IntegerField()
    race = models.CharField(max_length=40)
    color = models.CharField(max_length=7, default="#ffffff")

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["name"]
        db_table = "Pet"


class Food(models.Model):
    name = models.CharField(max_length=100)
    brand = models.CharField(max_length=30)
    FOOD_CATEGORIES = (
        ("D", "Trockenfutter"),
        ("W", "Nassfutter"),
        ("S", "Snacks"),
    )
    category = models.CharField(max_length=1, choices=FOOD_CATEGORIES)
    price = models.IntegerField()
    UNIT = (
        ("g", "g"),
        ("l", "ml"),
    )
    unit = models.CharField(max_length=1, choices=UNIT)

    class Meta:
        db_table = "Food"


class Meal(models.Model):
    time = models.DateTimeField(default=time_zone_now, blank=True)
    food = models.ForeignKey(Food, on_delete=models.CASCADE, related_name="meals")
    pets = models.ManyToManyField(Pet)
    quantity = models.IntegerField()

    class Meta:
        db_table = "Meal"