from django.urls import path
import api.views as views

urlpatterns = [
    path('catering_establishment/',
         views.CateringEstablishmentList.as_view()),
    path('catering_establishment/<int:pk>/',
         views.CateringEstablishmentEntity.as_view()),
    path('dish/', views.DishList.as_view()),
    path('dish/<int:pk>/', views.DishEntity.as_view()),
    path('catering_establishment_dish/',
         views.CateringEstablishmentDishList.as_view()),
    path('catering_establishment_dish/<int:pk>/',
         views.CateringEstablishmentDishEntity.as_view()),
    path('ingredient/', views.IngredientList.as_view()),
    path('ingredient/<int:pk>/', views.IngredientEntity.as_view()),
    path('dish_ingredient/', views.DishIngredientList.as_view()),
    path('dish_ingredient/<int:pk>/', views.DishIngredientEntity.as_view()),
    path('automatic_machine_type/',
         views.AutomaticMachineTypeList.as_view()),
    path('automatic_machine_type/<int:pk>/',
         views.AutomaticMachineTypeEntity.as_view()),
    path('catering_establishment_automatic_machine/',
         views.CateringEstablishmentAutomaticMachineList.as_view()),
    path('catering_establishment_automatic_machine/<int:pk>/',
         views.CateringEstablishmentAutomaticMachineEntity.as_view()),
    path('automatic_machine_dish/', views.AutomaticMachineDishList.as_view()),
    path('automatic_machine_dish/<int:pk>/',
         views.AutomaticMachineDishEntity.as_view()),
    path('user/', views.UserList.as_view()),
    path('user/<int:pk>/', views.UserEntity.as_view()),
    path('dish_report/', views.DishReportList.as_view()),
    path('dish_report/<int:pk>/', views.DishReportEntity.as_view()),
    path('ordered_dish_ingredient/', views.OrderedDishIngredientList.as_view()),
    path('ordered_dish_ingredient/<int:pk>/', views.OrderedDishIngredientEntity.as_view()),
]


