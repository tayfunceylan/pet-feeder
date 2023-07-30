from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from .views import *
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r"Meal", MealViewSet, basename="meal")
router.register(r"Food", FoodViewSet, basename="food")
router.register(r"Pet", PetViewSet, basename="pet")
urlpatterns = router.urls

urlpatterns += [
]






