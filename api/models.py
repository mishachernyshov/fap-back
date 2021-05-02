from django.db import models
from django.contrib.auth.models import AbstractUser, Permission
from django.utils.translation import gettext_lazy as _


class CateringEstablishment(models.Model):
    name = models.CharField(max_length=20)
    establishment_code = models.UUIDField()
    image = models.ImageField(
        blank=True,
        upload_to='cateringEstablishmentImages/'
    )
    country = models.CharField(max_length=25)
    city = models.CharField(max_length=25)
    street = models.CharField(max_length=30)

    def __str__(self):
        return self.name


class Dish(models.Model):
    name = models.CharField(max_length=20)
    image = models.ImageField(blank=True, upload_to='dishImages/')
    description = models.TextField()
    type = models.CharField(max_length=20)
    popularity = models.CharField(max_length=20, blank=True)
    rate = models.IntegerField()

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    name = models.CharField(max_length=20)
    price = models.FloatField()

    def __str__(self):
        return self.name


class DishIngredient(models.Model):
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    dish = models.ForeignKey(Dish, on_delete=models.CASCADE)
    # status = models.BooleanField()

    def __str__(self):
        return f'{self.dish.name}: {self.ingredient.name}'


class DishIngredientStandardPortion(models.Model):
    dish_ingredient = models.ForeignKey(
        DishIngredient, on_delete=models.CASCADE
    )
    weight_or_volume = models.FloatField()
    is_liquid = models.BooleanField(default=False)


class AutomaticMachineType(models.Model):

    def __str__(self):
        return str(self.id)


class CateringEstablishmentAutomaticMachine(models.Model):
    catering_establishment = models.ForeignKey(CateringEstablishment,
                                               on_delete=models.CASCADE)
    automatic_machine_type = models.ForeignKey(AutomaticMachineType,
                                               on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.catering_establishment.id}: ' \
               f'{self.automatic_machine_type.id}'


class AutomaticMachineDish(models.Model):
    automatic_machine_type = models.ForeignKey(AutomaticMachineType,
                                               on_delete=models.CASCADE)
    dish = models.ForeignKey(Dish, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.automatic_machine_type.id}: {self.dish.name}'


class User(AbstractUser):
    is_VIP = models.BooleanField(null=True)
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name=_('user permissions'),
        blank=True,
        help_text=_('Specific permissions for this user.'),
        related_name='users',
        related_query_name='user',
    )

    def __str__(self):
        return self.username


class DishReport(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    dish = models.ForeignKey(Dish, on_delete=models.CASCADE)
    text = models.TextField()
    publication_date = models.DateField()


class OrderedDishIngredient(models.Model):
    ingredient = models.ForeignKey(DishIngredient, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    weight_or_volume = models.FloatField()
    order_date = models.DateField()
    order_time = models.TimeField()
