from django.shortcuts import render
from rest_framework import generics, viewsets
import api.models as models
import api.serializers as serializers
import api.database_tools as database_tools


class CateringEstablishmentViewSet(viewsets.ModelViewSet):
    queryset = models.CateringEstablishment.objects.all()
    serializer_class = serializers.CateringEstablishmentSerializer


class DishViewSet(viewsets.ModelViewSet):
    queryset = models.Dish.objects.all()
    serializer_class = serializers.DishSerializer


class IngredientViewSet(viewsets.ModelViewSet):
    queryset = models.Ingredient.objects.all()
    serializer_class = serializers.IngredientSerializer


class DishIngredientViewSet(viewsets.ModelViewSet):
    queryset = models.DishIngredient.objects.all()
    serializer_class = serializers.DishIngredientSerializer


class AutomaticMachineTypeViewSet(viewsets.ModelViewSet):
    queryset = models.AutomaticMachineType.objects.all()
    serializer_class = serializers.AutomaticMachineTypeSerializer


class CateringEstablishmentAutomaticMachineViewSet(viewsets.ModelViewSet):
    queryset = models.AutomaticMachineType.objects.all()
    serializer_class = serializers.AutomaticMachineTypeSerializer


class AutomaticMachineDishViewSet(viewsets.ModelViewSet):
    queryset = models.AutomaticMachineDish.objects.all()
    serializer_class = serializers.AutomaticMachineDishSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = models.User.objects.all()
    serializer_class = serializers.UserSerializer


class DishReportViewSet(viewsets.ModelViewSet):
    queryset = models.DishReport.objects.all()
    serializer_class = serializers.DishReportSerializer


class OrderedDishIngredientViewSet(viewsets.ModelViewSet):
    queryset = models.OrderedDishIngredient.objects.all()
    serializer_class = serializers.OrderedDishIngredientSerializer


class AppropriateDishesWithIngredientsList(generics.ListCreateAPIView):
    serializer_class = serializers.AppropriateDishesSerializer

    def get_queryset(self):
        parameter_key = '0'
        query_parameters = self.request.query_params
        missed_count_parameter_list = \
            list(query_parameters.getlist(parameter_key))
        missed_count_parameter = int(missed_count_parameter_list[0]) \
            if len(missed_count_parameter_list) >= 1 else 2
        parameter_set = \
            set(map(int, list(query_parameters.getlist(parameter_key))))

        return get_dishes_with_ingredients(parameter_set, missed_count_parameter)


def get_dishes_with_ingredients(
        ingredients: set[int],
        acceptable_missed_count: int) -> dict[str: list[int]]:
    dishes = [dish.id for dish in models.Dish.objects.all()]
    appropriate_dishes = list()
    almost_appropriate_dishes = list()

    for dish_id in dishes:
        dish_ingredients = {item.ingredient_id for item
                            in models.DishIngredient.objects.filter(dish=dish_id)}
        print(dish_ingredients)
        not_used_ingredients = dish_ingredients.difference(ingredients)
        not_used_ingredients_count = len(not_used_ingredients)
        if not_used_ingredients_count == 0:
            appropriate_dishes.append(dish_id)
        elif not_used_ingredients_count <= acceptable_missed_count:
            almost_appropriate_dishes.append(dish_id)

    return (models.Dish.objects.filter(id__in=appropriate_dishes),
            models.Dish.objects.filter(id__in=almost_appropriate_dishes))


class CateringEstablishmentDishList(generics.ListAPIView):
    queryset = ''
    request = \
        'SELECT		    DISTINCT api_dish.* ' \
        'FROM   		api_cateringestablishment ' \
        'INNER JOIN 	api_cateringestablishmentautomaticmachine ' \
        'ON 			api_cateringestablishment.id = ' \
        '			    api_cateringestablishmentautomaticmachine.catering_establishment_id ' \
        'INNER JOIN 	api_automaticmachinetype ' \
        'ON 			api_cateringestablishmentautomaticmachine.automatic_machine_type_id = ' \
        '			    api_automaticmachinetype.id ' \
        'INNER JOIN 	api_automaticmachinedish ' \
        'ON 			api_automaticmachinetype.id = ' \
        '			    api_automaticmachinedish.automatic_machine_type_id ' \
        'INNER JOIN 	api_dish ' \
        'ON 			api_automaticmachinedish.dish_id = api_dish.id ' \
        'WHERE          api_cateringestablishment.id = {}'

    def get(self, request, *args, **kwargs):
        dishes = []
        return database_tools.executeRequest(
            CateringEstablishmentDishList.request.format(kwargs['pk']),
            database_tools.save_response_data_to_list,
            dishes,
            'GET')
