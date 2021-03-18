from django.shortcuts import render
from rest_framework import generics
import api.models as models
import api.serializers as serializers


class CateringEstablishmentList(generics.ListCreateAPIView):
    queryset = models.CateringEstablishment.objects.all()
    serializer_class = serializers.CateringEstablishmentSerializer


class CateringEstablishmentEntity(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.CateringEstablishment.objects.all()
    serializer_class = serializers.CateringEstablishmentSerializer


class DishList(generics.ListCreateAPIView):
    queryset = models.Dish.objects.all()
    serializer_class = serializers.DishSerializer


class DishEntity(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.Dish.objects.all()
    serializer_class = serializers.DishSerializer


class CateringEstablishmentDishList(generics.ListCreateAPIView):
    queryset = models.CateringEstablishmentDish.objects.all()
    serializer_class = serializers.CateringEstablishmentDishSerializer


class CateringEstablishmentDishEntity(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.CateringEstablishmentDish.objects.all()
    serializer_class = serializers.DishSerializer


class IngredientList(generics.ListCreateAPIView):
    queryset = models.Ingredient.objects.all()
    serializer_class = serializers.IngredientSerializer


class IngredientEntity(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.Ingredient.objects.all()
    serializer_class = serializers.IngredientSerializer


class DishIngredientList(generics.ListCreateAPIView):
    queryset = models.DishIngredient.objects.all()
    serializer_class = serializers.DishIngredientSerializer


class DishIngredientEntity(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.DishIngredient.objects.all()
    serializer_class = serializers.DishIngredientSerializer


class AutomaticMachineTypeList(generics.ListCreateAPIView):
    queryset = models.AutomaticMachineType.objects.all()
    serializer_class = serializers.AutomaticMachineTypeSerializer


class AutomaticMachineTypeEntity(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.AutomaticMachineType.objects.all()
    serializer_class = serializers.AutomaticMachineTypeSerializer


class CateringEstablishmentAutomaticMachineList(generics.ListCreateAPIView):
    queryset = models.AutomaticMachineType.objects.all()
    serializer_class = serializers.AutomaticMachineTypeSerializer


class CateringEstablishmentAutomaticMachineEntity(
        generics.RetrieveUpdateDestroyAPIView):
    queryset = models.CateringEstablishmentAutomaticMachine.objects.all()
    serializer_class = \
        serializers.CateringEstablishmentAutomaticMachineSerializer


class AutomaticMachineDishList(generics.ListCreateAPIView):
    queryset = models.AutomaticMachineDish.objects.all()
    serializer_class = serializers.AutomaticMachineDishSerializer


class AutomaticMachineDishEntity(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.AutomaticMachineDish.objects.all()
    serializer_class = serializers.AutomaticMachineDishSerializer


class UserList(generics.ListCreateAPIView):
    queryset = models.User.objects.all()
    serializer_class = serializers.UserSerializer


class UserEntity(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.User.objects.all()
    serializer_class = serializers.UserSerializer


class DishReportList(generics.ListCreateAPIView):
    queryset = models.DishReport.objects.all()
    serializer_class = serializers.DishReportSerializer


class DishReportEntity(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.DishReport.objects.all()
    serializer_class = serializers.DishReportSerializer


class OrderedDishIngredientList(generics.ListCreateAPIView):
    queryset = models.OrderedDishIngredient.objects.all()
    serializer_class = serializers.OrderedDishIngredientSerializer


class OrderedDishIngredientEntity(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.OrderedDishIngredient.objects.all()
    serializer_class = serializers.OrderedDishIngredientSerializer
