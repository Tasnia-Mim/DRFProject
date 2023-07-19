from django.urls import path, include
from . import views

app_name = 'doctor'

urlpatterns = [
    path('doctor/profile', views.DoctorProfileView.as_view(), name='doctor_profile'),   
    
]