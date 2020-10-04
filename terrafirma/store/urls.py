from django.urls import path

from . import views

urlpatterns = [
    path('store/', views.StoreView.as_view(), name='store'),
]
