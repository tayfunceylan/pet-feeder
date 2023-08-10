## API Endpoints

### Meals

- **List all meals**: `GET /meals/`
- **Create a meal**: `POST /meals/`
- **Retrieve a meal**: `GET /meals/:id/`
- **Update a meal**: `PUT /meals/:id/`
- **Partial update a meal**: `PATCH /meals/:id/`
- **Delete a meal**: `DELETE /meals/:id/`
- **Get daily meals in pagination**: `GET /meals/daily_meals/`
- **Get meals by specific date**: `GET /meals/get_day/` with parameter `?date=YYYY-MM-DD`

### Foods

- **List all foods**: `GET /foods/`
- **Create a food**: `POST /foods/`
- **Retrieve a food**: `GET /foods/:id/`
- **Update a food**: `PUT /foods/:id/`
- **Partial update a food**: `PATCH /foods/:id/`
- **Delete a food**: `DELETE /foods/:id/`

### Pets

- **List all pets**: `GET /pets/`
- **Create a pet**: `POST /pets/`
    - Note: A `400 Bad Request` will be returned if a pet with the same name already exists.
- **Retrieve a pet**: `GET /pets/:id/`
- **Update a pet**: `PUT /pets/:id/`
- **Partial update a pet**: `PATCH /pets/:id/`
- **Delete a pet**: `DELETE /pets/:id/`
- **Get meals by pet ID**: `GET /pets/get_meals/` with parameter `?PID=pet_id`

## Models

### Pet

- **name**: CharField (max_length=30)
- **age**: IntegerField
- **race**: CharField (max_length=40)

### Food

- **name**: CharField (max_length=100)
- **brand**: CharField (max_length=30)
- **category**: CharField (choices: Dry, Wet, Snack)
- **price**: IntegerField
- **unit**: CharField (choices: g, ml)

### Meal

- **time**: DateTimeField (default is current time)
- **food**: ForeignKey to Food
- **pet**: ManyToManyField to Pet
- **quantity**: IntegerField

