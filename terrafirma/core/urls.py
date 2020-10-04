from django.urls import include, path

from . import views

urlpatterns = [
    # home
    path('', views.HomeView.as_view(), name='home'),

    # environments
    path('environments/new/', views.NewEnvironmentView.as_view(), name='new-env'),
    path(
        'environment/<str:env_name>/',
        include([
            path('', views.EnvView.as_view(), name='env'),

            # beds
            path('beds/', views.BedListView.as_view(), name='beds'),
            path('beds/new', views.NewBedView.as_view(), name='new-bed'),
            path('bed/<str:bed_name>/', include([
                path('', views.BedView.as_view(), name='bed'),
                path('edit/', views.EditBedView.as_view(), name='edit-bed'),
            ])),
        ])),

    # plants
    path('plants/', views.PlantListView.as_view(), name='plants'),
    path('plants/new/', views.NewPlantView.as_view(), name='new-plant'),
    path(
        'plant/<int:plant_id>/',
        include([
            path('', views.PlantView.as_view(), name='plant'),
            path('transplant/', views.NewTransplantView.as_view(), name='new-transplant'),
        ])),

    # plant types
    path('plant-types/', views.PlantTypeListView.as_view(), name='plant-types'),
    path('plant-types/new/', views.NewPlantTypeView.as_view(), name='new-plant-type'),
    path('plant-type/<int:plant_type_id>/', views.PlantTypeView.as_view(), name='plant-type'),
]
