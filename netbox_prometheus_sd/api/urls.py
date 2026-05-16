from django.urls import path
from . import views

urlpatterns = [
    path('targets/', views.PrometheusTargetsView.as_view(), name='prometheus-target-list'),
]
