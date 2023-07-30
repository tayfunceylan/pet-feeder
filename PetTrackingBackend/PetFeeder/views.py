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
from datetime import timedelta
from django.core.paginator import Paginator
from django.utils.dateparse import parse_date

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

    @action(detail=False)
    def get_day(self, request):

        # Get the `date` from query parameters, or you can define a default date
        request_date = request.query_params.get('date')             # format is ?date=YYYY-MM-DD
        date_meals = Meal.objects.filter(time__date=request_date)

        # Serialize the queryset
        serializer = MealSerializer(date_meals, many=True)
        serialized_meals = serializer.data  # This is now a list of dictionaries

        # Prepare daily_data
        daily_data = {'date': request_date, 'meals': serialized_meals}
        return Response(daily_data)


class FoodViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Food.objects.all()
    serializer_class = FoodSerializer


class PetViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Pet.objects.all()
    serializer_class = PetSerializer



