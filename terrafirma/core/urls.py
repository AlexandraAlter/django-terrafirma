from django.urls import include, path

from . import views

urlpatterns = [
    # home
    path('', views.HomeView.as_view(), name='home'),

    # environments
    path('environments/new/', views.NewEnvView.as_view(), name='new-env'),
    path(
        'environment/<str:env_abbrev>/',
        include([
            path('', views.EnvView.as_view(), name='env'),
            path('edit/', views.EditEnvView.as_view(), name='edit-env'),

            # beds
            path('beds/', views.BedListView.as_view(), name='beds'),
            path('beds/new', views.NewBedView.as_view(), name='new-bed'),
            path(
                'bed/<str:bed_abbrev>/',
                include([
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
            path('edit/', views.EditPlantView.as_view(), name='edit-plant'),
            path('new-obs/', views.NewPlantObsView.as_view(), name='new-obs'),
            path('new-trt/', views.NewPlantTrtView.as_view(), name='new-trt'),
            path('new-mal/', views.NewPlantMalView.as_view(), name='new-mal'),
            path('transplant/', views.NewTransplantView.as_view(), name='new-trans'),
        ])),

    # plant types
    path('plant-types/', views.PlantTypeListView.as_view(), name='plant-types'),
    path('plant-types/new/', views.NewPlantTypeView.as_view(), name='new-plant-type'),
    path('plant-type/<int:plant_type_id>/', views.PlantTypeView.as_view(), name='plant-type'),

    # treatment types
    path('treatment-types/', views.TreatmentTypeListView.as_view(), name='trt-types'),
    path('treatment-types/new/', views.NewTreatmentTypeView.as_view(), name='new-trt-type'),
    path('treatment-type/<int:trt_type_id>/', views.TreatmentTypeView.as_view(), name='trt-type'),
    path('treatment-type/<int:trt>/edit/', views.EditTreatmentTypeView.as_view(), name='edit-trt-type'),

    # # malady types
    path('malady-types/', views.MaladyTypeListView.as_view(), name='mal-types'),
    path('malady-types/new/', views.NewMaladyTypeView.as_view(), name='new-mal-type'),
    path('malady-type/<int:mal_type_id>/', views.MaladyTypeView.as_view(), name='mal-type'),
    path('malady-type/<int:mal_type_id>/edit/', views.EditMaladyTypeView.as_view(), name='edit-mal-type'),
]
