from django.urls import path
import api.views as views
from rest_framework.routers import SimpleRouter

router = SimpleRouter()

router.register('catering_establishment',
                views.CateringEstablishmentViewSet,
                basename='catering_establishment')
router.register('dish',
                views.DishViewSet,
                basename='dish')
router.register('ingredient',
                views.IngredientViewSet,
                basename='ingredient')
router.register('dish_ingredient',
                views.DishIngredientViewSet,
                basename='dish_ingredient')
router.register('automatic_machine_type',
                views.AutomaticMachineTypeViewSet,
                basename='automatic_machine_type')
router.register('catering_establishment_automatic_machine',
                views.CateringEstablishmentAutomaticMachineViewSet,
                basename='catering_establishment_automatic_machine')
router.register('automatic_machine_dish',
                views.AutomaticMachineDishViewSet,
                basename='automatic_machine_dish')
router.register('user',
                views.UserViewSet,
                basename='user')
router.register('dish_report',
                views.DishReportViewSet,
                basename='dish_report')
router.register('ordered_dish_ingredient',
                views.OrderedDishIngredientViewSet,
                basename='ordered_dish_ingredient')


urlpatterns = [
    path('catering_establishment_dish/<int:pk>/',
         views.CateringEstablishmentDishList.as_view()),
    path('appropriate_dishes/',
         views.AppropriateDishesWithIngredientsList.as_view()),
    path('catering_establishments_with_given_dishes/',
         views.DishSetCateringEstablishments.as_view()),
]

urlpatterns += router.urls
