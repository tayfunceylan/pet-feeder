from rest_framework.routers import DefaultRouter

from .views import *

router = DefaultRouter()
router.register(r"Meal", MealViewSet, basename="meal")
router.register(r"Food", FoodViewSet, basename="food")
router.register(r"Pet", PetViewSet, basename="pet")
urlpatterns = router.urls

urlpatterns += [
]
