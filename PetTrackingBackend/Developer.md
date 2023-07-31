# For Developers (aka Tayfun)

## List Of Contents

- ### [Data Base Model](#model)

- ### [Serializers Documentation](#serializers-documentation)

- ### [View](#API-Endpoints)

  - [ModelViewSet](#modelviewset-documentation)
  - [Extra Actions](#extra-actions) 


## Serializers Documentation

Serializers in Django REST Framework serve a similar purpose to Django's forms, providing a mechanism of converting complex data types into JSON or other content types that can be rendered into a HTTP response or can be used to parse the content of an HTTP request.

Serializers offer validation of the incoming data, deserialization (turning received JSON into model instances), and serialization (converting model instances into JSON).

### Pet Serializer

`PetSerializer` is a ModelSerializer for the Pet model. It validates and (de-)serializes data for Pet model instances.

This serializer has one field validator, `validate_name`, which checks if a Pet with the given name already exists and raises a validation error if true.

### Food Serializer

`FoodSerializer`, like `PetSerializer`, is a ModelSerializer for the Food model. It processes and validates data for Food model instances.

It also has a `validate_name` method, which works much like the one in the `PetSerializer`.

### Meal Serializer

`MealSerializer` is a simple ModelSerializer for the Meal model. It handles the serialization and deserialization of the Meal model instances.

### DailyMeal Serializer

`DailyMealSerializer`, unlike the others, does not inherit from `ModelSerializer` but directly from `serializers.Serializer`. This is because the data it handles do not directly correspond to a model.

Instead, it represents data for a specific structure that includes a date and a collection of Meal instances for that date. `DailyMealSerializer` uses `MealSerializer` to serialize the Meal instances.

## ModelViewSet Documentation

A `ModelViewSet` is a type of view that includes the set of generic class-based views (Create, Retrieve, Update, Delete, List) for a given model class. A `ModelViewSet` essentially provides complete CRUD operations for a model without having to write explicit code for each individual view.

...
