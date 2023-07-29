from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from .views import *

urlpatterns = [
    path("Pet/", PetList.as_view()),
    path('FoodList/', FoodList.as_view()),
    path('Meal/', MealList.as_view()),
    path("Pet/<int:pk>", PetDetail.as_view()),
    path('FoodList/<int:pk>', FoodDetail.as_view()),
    path('Meal/<int:pk>', MealDetail.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)






