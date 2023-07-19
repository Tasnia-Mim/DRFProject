from django.urls import path
from . import views

app_name = 'users'


urlpatterns = [
    path('user/patient/registration', views.PatientRegistrationView.as_view(), name='patient_registration'),   
    path('user/organization-user/registration', views.OrganizationUserRegistrationView.as_view(), name='organization_user_registration'),   
    path('user/login', views.LoginView.as_view(), name='login'), 
    
]