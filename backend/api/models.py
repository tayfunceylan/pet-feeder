import math
from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now as time_zone_now
from django.db.models import Sum
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from django.core.validators import MaxValueValidator, MinValueValidator
import base64
from os import getenv
import tinytuya

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
    last_used = models.DateTimeField(default=time_zone_now, blank=True)

    @property
    def left(self):
        eaten = self.meals.all().aggregate(Sum('quantity'))['quantity__sum']
        eaten = eaten if eaten else 0
        left = (self.amount - eaten)
        if self.category != 'D':
            left /= self.packet_size
        if left <= 0: 
            self.active = False
            self.save()
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
        if not self.pk: # if new meal
            self.food.last_used = self.fed_at
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


class Schedule(models.Model):
    # byte 1 is for weekdays 7th bit is for monday, 1st bit is for sunday
    # byte 2 is for hour
    # byte 3 is for minute
    # byte 4 is for amount of feedings (1-12)
    # byte 5 is for on or off (0 or 1)
    weekdays = models.IntegerField(default=0b01111111, validators=[MaxValueValidator(0b01111111)])
    hour = models.IntegerField(validators=[MaxValueValidator(23), MinValueValidator(0)])
    minute = models.IntegerField(validators=[MaxValueValidator(59), MinValueValidator(0)])
    amount = models.IntegerField(validators=[MaxValueValidator(12), MinValueValidator(1)])
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=time_zone_now, blank=True)

    @property
    def export_schedule(self):
        weekdays = self.weekdays.to_bytes(1, byteorder='big')
        hour = self.hour.to_bytes(1, byteorder='big')
        minute = self.minute.to_bytes(1, byteorder='big')
        amount = self.amount.to_bytes(1, byteorder='big')
        active = self.active.to_bytes(1, byteorder='big')
        export = weekdays + hour + minute + amount + active
        return export.hex()

    # trigger on modifaication of meal
    def save(self, *args, **kwargs):
        if not self.update_schedule(): return
        # on successfull save do the following
        super(Schedule, self).save(*args, **kwargs)
        # send a notification to the frontend
        async_to_sync(get_channel_layer().group_send)('notify', {
            'type': 'notify.message',
            'message': 'newSchedule'
        })
    
    # trigger on deletion of meal
    def delete(self, *args, **kwargs):
        if not self.update_schedule(True): return
        # on successfull deletion do the following
        super(Schedule, self).delete(*args, **kwargs)
        # send a notification to the frontend
        async_to_sync(get_channel_layer().group_send)('notify', {
            'type': 'notify.message',
            'message': 'newSchedule'
        })

    def update_schedule(self, delete=False):
        all_schedules = Schedule.objects.all().exclude(id=self.id)
        all_schedules = ''.join([schedule.export_schedule for schedule in all_schedules])
        if not delete: all_schedules += self.export_schedule
        print("all: ", all_schedules)
        all_schedules = base64.b64encode(bytes.fromhex(all_schedules)).decode('ascii')
        id, ip, key = getenv("TUYA_ID"), getenv("TUYA_IP"), getenv("TUYA_KEY")
        if not id or not ip or not key: return False
        
        d = tinytuya.OutletDevice(id, ip, key)
        d.set_version(3.3)
        d.set_socketTimeout(2.0)
        d.set_socketRetryLimit(1)

        payload = d.generate_payload(tinytuya.CONTROL, {'1': all_schedules})
        d.send(payload)
        resp = d.receive()
        if "Error" in resp:
            print(resp)
            return False
        return True