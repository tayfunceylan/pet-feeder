import tinytuya
from os import getenv
from django.core.exceptions import ObjectDoesNotExist
from django.db.models.functions import TruncDate
from django.contrib.auth import authenticate, login
from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.forms.models import model_to_dict
from .serializers import *
from django.middleware.csrf import get_token
from rest_framework.views import APIView


class TokenView(APIView):
    permission_classes = []

    def get(self, request):
        return Response(get_token(request))


class LoginView(APIView):
    permission_classes = []
    def post(self, request):
        # get username and password from request
        username = request.data.get("username")
        password = request.data.get("password")
        # authenticate user
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return Response({"detail": "Login successful"}, 200)
        else:
            return Response({"detail": "Login failed"}, 401)
    
    def get(self, request):
        if request.user.is_authenticated:
            return Response({"detail": "User is logged in"}, 200)
        else:
            return Response({"detail": "User is not logged in"}, 401)


class MapsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        units_map = dict(Food.UNIT)
        categories_map = dict(Food.FOOD_CATEGORIES)
        pets_map = {pet.id: pet.name for pet in Pet.objects.all()}
        
        categories_list = [ {"k": k, "v": v} for k, v in Food.FOOD_CATEGORIES ]
        units_list = [ {"k": k, "v": v} for k, v in Food.UNIT ]

        maps = {"units": units_map, "categories": categories_map, "pets": pets_map}
        lists = {"units": units_list, "categories": categories_list}
        return Response({"maps": maps, "lists": lists})


class DayPage(PageNumberPagination):
    page_size = 1


# ====================[ Get: list of ..., Post: create a new instance ]=========================
class MealViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Meal.objects.all().order_by("-fed_at")
    serializer_class = MealSerializer

    # Get Daily Meals in paginate
    @action(detail=False)
    def daily_meals(self, request):
        paginator = DayPage()
        # Get all the distinct dates (all the days with meals)
        dates = (
            Meal.objects.order_by()
            .annotate(date=TruncDate("time"))
            .values("date")
            .distinct()
        )
        page = paginator.paginate_queryset(dates, request, self)

        # only display the pagination if needed
        if page is not None:
            results = []
            for item in page:
                date_meals = Meal.objects.filter(fed_at__date=item["date"])
                daily_data = {"date": item["date"], "meals": date_meals}
                results.append(daily_data)

            serializer = DailyMealSerializer(results, many=True)
            return paginator.get_paginated_response(serializer.data)

        return Response({"detail": "No pagination applied."})

    @action(detail=False)
    def get_day(self, request):
        # Get the `date` from query parameters, or you can define a default date
        request_date = request.query_params.get("date")  # format is ?date=YYYY-MM-DD
        date_meals = Meal.objects.filter(fed_at__date=request_date).order_by("fed_at")

        # Serialize the queryset
        serialized_meals = MealSerializer(date_meals, many=True)

        # Prepare daily_data
        daily_data = {"date": request_date, "meals": serialized_meals.data}
        return Response(daily_data)

    @action(detail=False)
    def sort_category_an(self, request):
        # Get the `date` from query parameters, or you can define a default date
        request_date = request.query_params.get("date")  # format is ?date=YYYY-MM-DD
        categories_query = Food.objects.values("category").distinct()
        categories = [cat["category"] for cat in categories_query]
        food_categories = dict(Food.FOOD_CATEGORIES)
        meals = {}
        for category in categories:
            date_meals = (Meal.objects
                          .filter(fed_at__date=request_date, food__category=category)
                          .order_by("-fed_at"))

        # Serialize the queryset
            serializer = MealSerializer(date_meals, many=True)
            serialized_meals = serializer.data  # This is now a list of dictionaries
            meals[food_categories[category]] = serialized_meals

        # Prepare daily_data
        daily_data = {"date": request_date, "meals": meals}
        return Response(daily_data)

    @action(detail=False)
    def sort_category(self, request):
        request_date = request.query_params.get("date")  # format is ?date=YYYY-MM-DD
        meals = Meal.objects.filter(fed_at__date=request_date).order_by("-fed_at")
        result = {category[1]: [] for category in Food.FOOD_CATEGORIES}
        for meal in meals:
            result[meal.food.get_category_display()].append(MealSerializer(meal).data)

        daily_data = {"date": request_date, "meals": result}
        return Response(daily_data)
    
    # dispenses food for cats and logs it
    @action(detail=False)
    def dispenser(self, request):
        id, ip, key = getenv("TUYA_ID"), getenv("TUYA_IP"), getenv("TUYA_KEY")
        print(id, ip, key)
        if not id or not ip or not key:
            return Response({"detail": "Tuya environment variables not set"}, 500)
        
        d = tinytuya.OutletDevice(id, ip, key)
        d.set_version(3.3)
        d.set_socketTimeout(2.0)
        d.set_socketRetryLimit(1)
        payload=d.generate_payload(tinytuya.CONTROL, {'3': 1})
        binary = d._encode_message(payload)
        # print binary in hex format
        print(binary.hex())
        d.send(payload)
        answer = d.receive()

        meal = {}
        if "Error" not in answer:
            # create a new meal with latest dry food
            meal = Meal.objects.create(
                food=Food.objects.last(),
                quantity=20,
            )
            meal.pets.set(Pet.objects.all())
            meal = MealSerializer(meal).data
        return Response({"feeder": answer, "meal": meal})


class FoodViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Food.objects.all()
    serializer_class = FoodSerializer

    @action(detail=False)
    def get_options(self, request):
        # as list with dict name: long name value: short name
        categories = [
            {"value": value, "name": name} 
            for value, name in Food.FOOD_CATEGORIES
        ]  
        units = [
            {"value": value, "name": name} 
            for value, name in Food.UNIT
        ]
        category_dict = dict(Food.FOOD_CATEGORIES)
        return Response({"categories": categories, "units": units, "maps": {'categories': category_dict}})


class PetViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Pet.objects.all()
    serializer_class = PetSerializer

    # Handle multiple occurrence of names
    def create(self, request, *args, **kwargs):
        new_pet = request.data
        existing_pets = Pet.objects.filter(name=new_pet["name"])

        # check if the pet.name is already existing. return the existing cat-names
        if existing_pets.exists():
            return Response(
                {
                    "detail": "Pet with the same name already exists",
                    "your_pet:": new_pet,
                    "existing_pets": [
                        model_to_dict(pet) for pet in existing_pets.iterator()
                    ],
                },
                status=400,
            )

        # Perform the creation after validating that the name is not already existent
        serialized_pet = self.get_serializer(data=new_pet)
        serialized_pet.is_valid(raise_exception=True)
        self.perform_create(serialized_pet)
        return Response(serialized_pet.data, status=201)

    @action(
        detail=False,
        description="Search All the Meals a pet has eaten.",
        methods=["GET"],
    )
    def get_meals(self, reqeust):
        request_data = reqeust.query_params.get("PID")  # get the data

        # Try to get the Pet with ID. If the ID is a wrong return with Error 404
        try:
            pet = Pet.objects.get(id=request_data)
        except ObjectDoesNotExist:
            return Response({"detail": "Pet with the given id does not exist"}, 404)

        # get the meal too
        pet_meals = Meal.objects.filter(pet__id=request_data).distinct()
        # serialize Both objects
        pet_serializer = PetSerializer(pet).data
        meal_serializer = MealSerializer(pet_meals, many=True)
        serialized_meals = meal_serializer.data

        # return both objects
        pet_data = {"pet": pet_serializer, "meals": serialized_meals}
        return Response(pet_data)