from django.urls import include, path

from . import views

urlpatterns = [
    path('home/', views.HomeView.as_view(), name='home'),
    path('environments/new/', views.NewEnvironmentView.as_view(), name='new-env'),
    path(
        'environment/<str:env_name>',
        include([
            path('', views.EnvView.as_view(), name='env')
            # path('beds', views.BedListView.as_view()),
            # path('bed/<str:bed_name>', include([
            #     path('', views.BedView.as_view()),
            # ])),
        ])),
    # path('plants/', views.PlantListView.as_view()),
    # path('plant/<int:plant_id>', views.PlantView.as_view()),
]
