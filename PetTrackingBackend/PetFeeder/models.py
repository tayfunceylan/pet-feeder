from django.db import models


class Pet(models.Model):
    name = models.CharField(max_length=30)
    age = models.IntegerField()
    race = models.CharField(max_length=40)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


class Food(models.Model):
    name = models.CharField(max_length=100)
    brand = models.CharField(max_length=30)
    FOOD_CATEGORIES = (
        ('D', 'Dry'),
        ('W', 'Wet'),
        ('S', 'Snack'),
    )
    category = models.CharField(max_length=1, choices=FOOD_CATEGORIES)
    price = models.IntegerField()
    UNIT = (
        ('g', 'g'),
        ('l', 'ml'),
    )
    unit = models.CharField(max_length=1, choices=UNIT)


class Meal(models.Model):
    time = models.DateTimeField(auto_now_add=True)
    food = models.ForeignKey(Food, on_delete=models.CASCADE)
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)

