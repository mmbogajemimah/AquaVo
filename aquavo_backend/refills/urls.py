from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

app_name = 'refills'

urlpatterns = [
    path('create_refill/', views.CreateRefillView.as_view(), name='create_refill'),
    path('all_refills/', views.GetAllRefillsView.as_view(), name="all_refills"),
    path('user_refills/<int:customer_id>/', views.GetRefillsForUserView.as_view(), name='user_refills'),
    path('update_refills/<int:refill_id>/', views.UpdateRefillView.as_view(), name='update_refill'),
    path('delete_refills/<int:refill_id>/', views.DeleteRefillView.as_view(), name='delete_refill'),
]


urlpatterns = format_suffix_patterns(urlpatterns)
