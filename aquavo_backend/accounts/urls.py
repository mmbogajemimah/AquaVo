from django.urls import path  # Use path instead of url
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

app_name = 'accounts'

# Obtain auth Token to Obtain User Token
urlpatterns = [
    path('all_users/', views.AllUsers.as_view(), name='all_users'),  # Use path instead of url
    path('user_by_id/<int:user_id>/', views.GetUserById.as_view(), name='user_by_id'),
    path('update_user_by_id/<int:user_id>/', views.UpdateUser.as_view(), name='update_user_by_id'),
]

urlpatterns = format_suffix_patterns(urlpatterns)
