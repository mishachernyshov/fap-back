from django.shortcuts import render
from rest_framework import generics, viewsets
import api.models as models
import api.serializers as serializers
import api.database_tools as database_tools
from collections import defaultdict


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


class DishSetCateringEstablishments(generics.ListAPIView):
    serializer_class = serializers.CateringEstablishmentSerializer

    def get_queryset(self):
        query_parameters = self.request.query_params

        dish_key = 'dish'
        wish_list = set(map(int, list(query_parameters.getlist(dish_key))))

        automated_machines_with_given_dishes = \
            models.AutomaticMachineDish.objects.filter(dish__in=wish_list)
        automated_machines_types_with_given_dishes = \
            automated_machines_with_given_dishes.values_list('automatic_machine_type')
        dishes_cooked_by_machines = \
            automated_machines_with_given_dishes.values_list('dish')

        machine_type_appropriate_dishes = get_list_mapped_to_integer(
            automated_machines_types_with_given_dishes, dishes_cooked_by_machines)

        catering_establishment_machines = get_catering_establishment_machines(
            automated_machines_types_with_given_dishes)

        catering_establishments_that_cook_given_dishes = \
            get_catering_establishments_that_cook_given_dishes(
                machine_type_appropriate_dishes,
                catering_establishment_machines, wish_list)

        searched_catering_establishments = models.CateringEstablishment.objects.filter(
            id__in=catering_establishments_that_cook_given_dishes)
        searched_catering_establishments = \
            choose_catering_establishment_by_location(
                query_parameters, searched_catering_establishments)

        return searched_catering_establishments


def get_list_mapped_to_integer(keys, values):
    result_dict = defaultdict(set)

    for k in range(len(keys)):
        result_dict[keys[k][0]].add(values[k][0])

    return result_dict


def get_catering_establishment_machines(
        automated_machines_types_with_given_dishes):
    machines_that_cook_given_dishes = \
        models.CateringEstablishmentAutomaticMachine.objects.filter(
            automatic_machine_type__in=automated_machines_types_with_given_dishes)
    appropriate_catering_establishments = \
        machines_that_cook_given_dishes.values_list('catering_establishment')
    appropriate_machines = \
        machines_that_cook_given_dishes.values_list('automatic_machine_type')
    return get_list_mapped_to_integer(
        appropriate_catering_establishments, appropriate_machines)


def get_catering_establishments_that_cook_given_dishes(
        catering_establishment_machines, machine_type_dishes, wish_list):
    appropriate_catering_establishments = list()

    for catering_establishment, machines in \
            catering_establishment_machines.items():
        catering_establishment_dishes = set()
        for machine in machines:
            catering_establishment_dishes = \
                catering_establishment_dishes.union(machine_type_dishes[machine])
        if catering_establishment_dishes == wish_list:
            appropriate_catering_establishments.append(catering_establishment)

    return appropriate_catering_establishments


def choose_catering_establishment_by_location(params, catering_establishments):
    street_list = params.getlist('street')
    city_list = params.getlist('city')
    country_list = params.getlist('country')

    if street_list:
        if appropriate_catering_establishments := \
                catering_establishments.filter(street__exact=street_list[0]):
            return appropriate_catering_establishments

    if city_list:
        if appropriate_catering_establishments := \
                catering_establishments.filter(city__exact=city_list[0]):
            return appropriate_catering_establishments

    if country_list:
        if appropriate_catering_establishments := \
                catering_establishments.filter(country__exact=country_list[0]):
            return appropriate_catering_establishments

    return catering_establishments
