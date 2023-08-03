from django.core.exceptions import ObjectDoesNotExist
from django.db.models.functions import TruncDate
from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .serializers import *

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

        # only display the pagination if needed
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

    @action(detail=False, description="Search All the Meals a pet has eaten.", methods=['GET'])
    def get_meals(self, reqeust):
        request_data = reqeust.query_params.get('PID')      # get the data

        # Try to get the Pet with ID. If the ID is wrong return with Error 404
        try:
            pet = Pet.objects.get(id=request_data)
        except ObjectDoesNotExist:
            return Response({"detail": "Pet with the given id does not exist"}, 404)

        # get the meal too
        pet_meals = Meal.objects.filter(pet__id=request_data)
        # serialize Both objects
        pet_serializer = PetSerializer(pet).data
        meal_serializer = MealSerializer(pet_meals, many=True)
        serialized_meals = meal_serializer.data

        # return both objects
        pet_data = {"pet": pet_serializer, "meals": serialized_meals}
        return Response(pet_data)