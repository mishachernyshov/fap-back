from django.db import models
from django.contrib.auth import get_user_model


class CateringEstablishment(models.Model):
    establishment_code = models.UUIDField()


class Dish(models.Model):
    name = models.CharField(max_length=20)
    image = models.ImageField(blank=True, upload_to='dishImages/')
    description = models.TextField()
    type = models.TextField(max_length=20)
    popularity = models.CharField(max_length=20)
    rate = models.IntegerField()


class CateringEstablishmentDish(models.Model):
    dish = models.ForeignKey(Dish, on_delete=models.CASCADE)
    catering_establishment = models.ForeignKey(CateringEstablishment,
                                               on_delete=models.CASCADE)


class Ingredient(models.Model):
    name = models.CharField(max_length=20)
    price = models.FloatField()


class DishIngredient(models.Model):
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    dish = models.ForeignKey(Dish, on_delete=models.CASCADE)
    status = models.BooleanField()


class AutomaticMachineType(models.Model):
    pass


class CateringEstablishmentAutomaticMachine(models.Model):
    catering_establishment = models.ForeignKey(CateringEstablishment,
                                               on_delete=models.CASCADE)
    automatic_machine_type = models.ForeignKey(AutomaticMachineType,
                                               on_delete=models.CASCADE)


class AutomaticMachineDish(models.Model):
    automatic_machine_type = models.ForeignKey(AutomaticMachineType,
                                               on_delete=models.CASCADE)
    dish = models.ForeignKey(Dish, on_delete=models.CASCADE)


class User(get_user_model()):
    status = models.CharField(max_length=20)


class DishReport(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    dish = models.ForeignKey(Dish, on_delete=models.CASCADE)
    text = models.TextField()
    publication_date = models.DateField()


class OrderedDishIngredient(models.Model):
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    weight_or_volume = models.FloatField()
    order_date = models.DateField()
    order_time = models.TimeField()
