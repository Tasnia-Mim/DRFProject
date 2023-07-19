from django.urls import path, include
from . import views

app_name = 'organization_user'

urlpatterns = [
    path('organization-user/profile', views.OrganizationUserProfileView.as_view(), name='organization_user_profile'),        
    
]