import math
from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now as time_zone_now
from django.db.models import Sum
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

class Pet(models.Model):
    name = models.CharField(max_length=30)
    birthday_on = models.DateField(blank=True)
    race = models.CharField(max_length=40)
    color = models.CharField(max_length=7, default="#ffffff")
    description = models.TextField(default="")
    picture = models.ImageField(upload_to="images/", default="images/default.png")
    created_at = models.DateTimeField(default=time_zone_now, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["name"]
        db_table = "Pet"

    # trigger on modifaication of pet
    def save(self, *args, **kwargs):
        # on successfull save do the following
        super(Pet, self).save(*args, **kwargs)
        # send a notification to the frontend
        async_to_sync(get_channel_layer().group_send)('notify', {
            'type': 'notify.message',
            'message': 'newPet'
        })
    
    # trigger on deletion of pet
    def delete(self, *args, **kwargs):
        # on successfull deletion do the following
        super(Pet, self).delete(*args, **kwargs)
        # send a notification to the frontend
        async_to_sync(get_channel_layer().group_send)('notify', {
            'type': 'notify.message',
            'message': 'newPet'
        })


class Food(models.Model):
    UNIT = (
        ("g", "Gramm"),
        ("ml", "Milliliter"),
        ("stk", "Stück"),
    )
    FOOD_CATEGORIES = (
        ("W", "Nassfutter"),
        ("D", "Trockenfutter"),
        ("S", "Snacks"),
    )

    name = models.CharField(max_length=100)
    brand = models.CharField(max_length=30)
    amount = models.IntegerField()
    num_packets = models.IntegerField()
    packet_size = models.IntegerField()
    category = models.CharField(max_length=1, choices=FOOD_CATEGORIES)
    price = models.FloatField()
    unit = models.CharField(max_length=3, choices=UNIT)
    created_at = models.DateTimeField(default=time_zone_now, blank=True)
    active = models.BooleanField(default=True) # if no food left, set to false
    pl = models.CharField(max_length=100, default="", blank=True) # preis leistung

    @property
    def left(self):
        eaten = self.meals.all().aggregate(Sum('quantity'))['quantity__sum']
        eaten = eaten if eaten else 0
        left = (self.amount - eaten)
        if self.category != 'D':
            left /= self.packet_size
        return math.ceil(left)
    
    @property
    def top_quantities(self):
        # most 3 chosen quantity for this food in meals
        top3 = self.meals.all().values('quantity').annotate(count=models.Count('quantity')).order_by('-count')[:3].values_list('quantity', flat=True)
        return top3
    
    class Meta:
        db_table = "Food"

    # trigger on modifaication of food
    def save(self, *args, **kwargs):
        if self.unit == "g":
            self.pl = str(round(self.price / (self.amount/1000), 2)) + "€/kg"
        elif self.unit == "ml":
            self.pl = str(round(self.price / (self.amount/1000), 2)) + "€/l"
        elif self.unit == "stk":
            self.pl = str(round(self.price / self.amount, 2)) + "€/stk"
        # on successfull save do the following
        super(Food, self).save(*args, **kwargs)
        # send a notification to the frontend
        async_to_sync(get_channel_layer().group_send)('notify', {
            'type': 'notify.message',
            'message': 'newFood'
        })
    
    # trigger on deletion of food
    def delete(self, *args, **kwargs):
        # on successfull deletion do the following
        super(Food, self).delete(*args, **kwargs)
        # send a notification to the frontend
        async_to_sync(get_channel_layer().group_send)('notify', {
            'type': 'notify.message',
            'message': 'newFood'
        })


class Meal(models.Model):
    # user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    food = models.ForeignKey(Food, on_delete=models.CASCADE, related_name="meals")
    pets = models.ManyToManyField(Pet)
    quantity = models.IntegerField()
    fed_at = models.DateTimeField(default=time_zone_now, blank=True)
    created_at = models.DateTimeField(default=time_zone_now, blank=True)

    class Meta:
        db_table = "Meal"

    # trigger on modifaication of meal
    def save(self, *args, **kwargs):
        if self.food.left <= 0:
            if self.food.active: # if active although no food left
                self.food.active = False
                self.food.save()
        # on successfull save do the following
        super(Meal, self).save(*args, **kwargs)
        # send a notification to the frontend
        async_to_sync(get_channel_layer().group_send)('notify', {
            'type': 'notify.message',
            'message': 'newMeal'
        })
    
    # trigger on deletion of meal
    def delete(self, *args, **kwargs):
        # on successfull deletion do the following
        super(Meal, self).delete(*args, **kwargs)
        # send a notification to the frontend
        async_to_sync(get_channel_layer().group_send)('notify', {
            'type': 'notify.message',
            'message': 'newMeal'
        })

