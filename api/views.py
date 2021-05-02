from rest_framework import generics, viewsets
from django.http import HttpResponse
from django.views import View
from rest_framework.parsers import MultiPartParser

import api.models as models
import api.serializers as serializers
import api.database_tools as database_tools
from collections import defaultdict
import os
from json import dumps, load
from datetime import date


class CateringEstablishmentViewSet(viewsets.ModelViewSet):
    queryset = models.CateringEstablishment.objects.all()
    serializer_class = serializers.CateringEstablishmentSerializer


class DishViewSet(viewsets.ModelViewSet):
    parser_classes = [MultiPartParser]
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


class AppropriateDishesWithIngredientsList(
    generics.ListCreateAPIView):
    serializer_class = serializers.AppropriateDishesSerializer

    def get_queryset(self):
        ingredient_key = '0'
        missed_parameter_key = '1'
        query_parameters = self.request.query_params
        missed_count_parameter_list = \
            list(query_parameters.getlist(missed_parameter_key))
        missed_count_parameter = \
            int(missed_count_parameter_list[0]) \
                if len(missed_count_parameter_list) >= 1 else 0
        parameter_set = \
            set(map(int, list(
                query_parameters.getlist(ingredient_key))))

        return get_dishes_with_ingredients(
            parameter_set, missed_count_parameter)


def get_dishes_with_ingredients(
        ingredients: set[int],
        acceptable_missed_count: int) -> dict[str: list[int]]:
    dishes = [dish.id for dish in models.Dish.objects.all()]
    appropriate_dishes = list()
    almost_appropriate_dishes = list()

    for dish_id in dishes:
        dish_ingredients = {
            item.ingredient_id for item in
            models.DishIngredient.objects.filter(dish=dish_id)}
        print(dish_ingredients)
        not_used_ingredients = \
            dish_ingredients.difference(ingredients)
        not_used_ingredients_count = len(not_used_ingredients)
        if not_used_ingredients_count == 0:
            appropriate_dishes.append(dish_id)
        elif not_used_ingredients_count <= acceptable_missed_count:
            almost_appropriate_dishes.append(dish_id)

    return (
        models.Dish.objects.filter(
            id__in=appropriate_dishes),
        models.Dish.objects.filter(
            id__in=almost_appropriate_dishes))


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


class DishSetCateringEstablishments(
        generics.ListAPIView):
    serializer_class = \
        serializers.CateringEstablishmentSerializer

    def get_queryset(self):
        query_parameters = self.request.query_params

        dish_key = 'dish'
        wish_list = set(map(int, list(
            query_parameters.getlist(dish_key))))

        automated_machines_with_given_dishes = \
            models.AutomaticMachineDish.objects.filter(
                dish__in=wish_list)
        automated_machines_types_with_given_dishes = \
            automated_machines_with_given_dishes. \
            values_list('automatic_machine_type')
        dishes_cooked_by_machines = \
            automated_machines_with_given_dishes.\
            values_list('dish')

        machine_type_appropriate_dishes = \
            get_list_mapped_to_integer(
                automated_machines_types_with_given_dishes,
                dishes_cooked_by_machines)

        catering_establishment_machines = \
            get_catering_establishment_machines(
                automated_machines_types_with_given_dishes)

        catering_establishments_that_cook_given_dishes = \
            get_catering_establishments_that_cook_given_dishes(
                machine_type_appropriate_dishes,
                catering_establishment_machines, wish_list)

        searched_catering_establishments = \
            models.CateringEstablishment.objects.filter(
                id__in=
                catering_establishments_that_cook_given_dishes)
        searched_catering_establishments = \
            choose_catering_establishment_by_location(
                query_parameters,
                searched_catering_establishments)

        return searched_catering_establishments


class RequestedCatalogData(generics.ListAPIView):
    serializer_class = serializers.DishSerializer

    def get_queryset(self):
        received_parameters = self.request.query_params
        types, popularity, min_rate, max_rate, name_substring = \
            self.parse_params(received_parameters)
        filter_dict = self.get_filter_dict(
            types, popularity, min_rate, max_rate, name_substring
        )
        return models.Dish.objects.filter(**filter_dict)

    def parse_params(self, params):
        types = params.getlist('0')
        popularity = params.getlist('1')
        min_rate = int(params.get('2')) if params.get('2') else 0
        max_rate = int(params.get('3')) if params.get('3') else 0
        name_substring = params.get('4') if params.get('4') else ''
        return types, popularity, min_rate, max_rate, name_substring

    def get_filter_dict(self, types, popularity,
                        min_rate, max_rate, name_substring):
        filter_params = dict()
        if types:
            filter_params['type__in'] = types
        if popularity:
            filter_params['popularity__in'] = popularity
        if min_rate:
            filter_params['rate__gte'] = min_rate
        if max_rate:
            filter_params['rate__lte'] = max_rate
        if name_substring:
            filter_params['name__icontains'] = name_substring
        return filter_params


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
        machine_type_dishes, catering_establishment_machines, wish_list):
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


class FiltrationParamsView(View):

    def get(self, request, *args, **kwargs):
        dish_types = list(models.Dish.objects.\
                          values_list('type', flat=True).distinct())
        dish_popularity = list(models.Dish.objects.
                               values_list('popularity', flat=True).distinct())
        if '' in dish_popularity:
            dish_popularity.pop(dish_popularity.index(''))
        return HttpResponse(dumps({
            'type': dish_types,
            'popularity': dish_popularity
        }, ensure_ascii=False))


class DishIngredientsPreciseData(View):

    def get(self, request, *args, **kwargs):
        requested_dish_id = kwargs['pk']
        related_dish_ingredient_entities = \
            models.DishIngredient.objects.filter(dish=requested_dish_id)
        related_ingredients_values = \
            related_dish_ingredient_entities.values_list(
                'id', 'ingredient',
            )
        ingredients_data = list()
        for related_ingredient_value in related_ingredients_values:
            ingredient_object = models.Ingredient.objects.get(
                id=related_ingredient_value[1]
            )
            standard_portion = models.DishIngredientStandardPortion.objects.get(
                dish_ingredient=related_ingredient_value[0]
            )
            ingredients_data.append({
                'id': ingredient_object.id,
                'name': ingredient_object.name,
                'price': ingredient_object.price,
                'weight_or_volume': standard_portion.weight_or_volume,
                'is_liquid': standard_portion.is_liquid,
                'dish_ingredient': related_ingredient_value[0],
            })
        return HttpResponse(dumps(ingredients_data, ensure_ascii=False))


class AllDishReports(generics.ListAPIView):

    def get(self, request, *args, **kwargs):
        dish_id = kwargs['pk']
        appropriate_dish_reports = \
            list(models.DishReport.objects.filter(dish=dish_id))
        result_report_list = []
        for report in appropriate_dish_reports:
            result_report_list.append({
                'user': report.user.username,
                'text': report.text,
                'publication_date': str(report.publication_date),
            })
        return HttpResponse(dumps(result_report_list, ensure_ascii=False))


class ReportSending(generics.CreateAPIView):

    def post(self, request, *args, **kwargs):
        user_id = request.user.id
        new_report = models.DishReport(
            user=models.User.objects.get(id=user_id),
            dish=models.Dish.objects.get(id=request.data['dish']),
            text=request.data['text'],
            publication_date=date.today(),
        )
        new_report.save()
        return HttpResponse({})


class BackUpMaking(View):

    def post(self, request, *args, **kwargs):
        return perform_os_command('python manage.py dbbackup')


class RestoreDatabase(View):

    def post(self, request, *args, **kwargs):
        return perform_os_command('yes Y | python manage.py dbrestore')


class UpdateCertificate(View):

    def post(self, request, *args, **kwargs):
        return perform_os_command(
            'mkcert cert key 0.0.0.0 localhost 127.0.0.1 ::1 && mv '
            'cert+5.pem cert.pem && mv cert+5-key.pem key.pem')


def perform_os_command(command):
    try:
        os.system(command)
    except:
        return HttpResponse(status=500)
    return HttpResponse(status=200)
