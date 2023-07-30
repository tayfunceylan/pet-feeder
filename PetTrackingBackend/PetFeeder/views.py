from django.db.models.functions import TruncDate
from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from .models import *
from .serializers import *
from rest_framework.pagination import PageNumberPagination
from rest_framework import generics, status, viewsets, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view, action
# Create your views here.


class DayPage(PageNumberPagination):
    page_size = 1


# ====================[ Get: list of ..., Post: create a new instance ]=========================
class MealViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Meal.objects.all().order_by('-time')
    serializer_class = MealSerializer

    # Get Daily Meals in paginate
    @action(detail=False)
    def daily_meals(self, request):
        paginator = DayPage()
        # Get all the distinct dates (all the days with meals)
        dates = Meal.objects.order_by().annotate(date=TruncDate('time')).values('date').distinct()
        page = paginator.paginate_queryset(dates, request, self)

        if page is not None:
            results = []
            for item in page:
                date_meals = Meal.objects.filter(time__date=item['date'])
                daily_data = {'date': item['date'], 'meals': date_meals}
                results.append(daily_data)

            serializer = DailyMealSerializer(results, many=True)
            return paginator.get_paginated_response(serializer.data)

        return Response({"detail": "No pagination applied."})


class FoodViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Food.objects.all()
    serializer_class = FoodSerializer


class PetViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Pet.objects.all()
    serializer_class = PetSerializer



