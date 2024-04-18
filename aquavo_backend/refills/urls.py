from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

app_name = 'refills'

urlpatterns = [
    path('create_refill/', views.CreateRefillView.as_view(), name='create_refill'),
]


urlpatterns = format_suffix_patterns(urlpatterns)
