from django.urls import path

from . import views

urlpatterns = [
    path('planner/', views.PlannerView.as_view(), name='planner'),
]
