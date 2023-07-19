from django.urls import path

from . import views

app_name = 'prescriptionS'

urlpatterns = [
    path('doctor/prescriptions/<uuid:uid>', views.PrescriptionDetailView_Doctor.as_view(), name='prescription_detail_doctor'), 
    path('doctor/prescriptions/prescription', views.PrescriptionCreateView_Doctor.as_view(), name='prescription_create'),
    path('doctor/prescriptions', views.PrescriptionListView_Doctor.as_view(), name='prescription_create'),        
    path('patient/prescriptions/<uuid:uid>', views.PrescriptionDetailView_Patient.as_view(), name='prescription_detail_patient'),
    path('patient/prescriptions', views.PrescriptionListView_Patient.as_view(), name='prescription_list_patient'),
]