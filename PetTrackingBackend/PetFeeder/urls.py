from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from .views import *

meal_list = MealViewSet.as_view({
    'get': 'list',
    'post': 'create',
})
meal_detail = MealViewSet.as_view({
    'get': 'retrieve',
    'post': 'create',
    'put': 'update',
    'delete': 'destroy',
})
food_list = FoodViewSet.as_view({
    'get': 'list',
    'post': 'create',
})
food_detail = FoodViewSet.as_view({
    'get': 'retrieve',
    'post': 'create',
    'put': 'update',
    'delete': 'destroy',
})

urlpatterns = [
]

urlpatterns = format_suffix_patterns(urlpatterns)






