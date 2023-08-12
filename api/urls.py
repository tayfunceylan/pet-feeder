from rest_framework.routers import DefaultRouter
from rest_framework.authtoken import views
from django.urls import re_path, path
from .views import *

router = DefaultRouter()
router.register(r"Meal", MealViewSet, basename="meal")
router.register(r"Food", FoodViewSet, basename="food")
router.register(r"Pet", PetViewSet, basename="pet")
urlpatterns = router.urls

urlpatterns += [path("api-token-auth", views.obtain_auth_token)]
