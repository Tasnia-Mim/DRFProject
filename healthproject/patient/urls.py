from django.urls import path, include
from . import views

app_name = 'patient'

urlpatterns = [    
    path('patient/profile', views.PatientProfileView.as_view(), name='profile_profile'),    
    
]