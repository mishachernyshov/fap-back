from django.contrib import admin
from . import models


api_models = [
    models.AutomaticMachineDish,
    models.AutomaticMachineType,
    models.CateringEstablishment,
    models.CateringEstablishmentAutomaticMachine,
    models.CateringEstablishmentDish,
    models.Dish,
    models.DishIngredient,
    models.DishReport,
    models.Ingredient,
    models.OrderedDishIngredient,
    models.User,
]

admin.site.register(api_models)
