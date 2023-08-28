from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register(r"meal", MealViewSet, basename="meal")
router.register(r"food", FoodViewSet, basename="food")
router.register(r"pet", PetViewSet, basename="pet")
router.register(r"hello", TokenView, basename="hello")
# router.register(r"hello2", hello_world, basename="hello2")

urlpatterns = router.urls

urlpatterns += [
]
