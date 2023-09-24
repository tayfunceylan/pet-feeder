from rest_framework.routers import DefaultRouter
from django.urls import path
from .views import *

router = DefaultRouter()
router.register(r"meal", MealViewSet, basename="meal")
router.register(r"food", FoodViewSet, basename="food")
router.register(r"pet", PetViewSet, basename="pet")
router.register(r"schedules", ScheduleViewSet, basename="schedule")

urlpatterns = router.urls

urlpatterns += [
    path("token/", TokenView.as_view()),
    path("helper/", MapsView.as_view()),
    path("login/", LoginView.as_view()),
]
