from django.urls import path

from . import views

app_name = 'appointment'

urlpatterns = [
    path('patient/appoitnments/request', views.AppointmentRequestView_Patient.as_view(), name='appointment_request_patient'),
    path('patient/appoitnments', views.AppointmentListView_Patient.as_view(), name='appointment_request_patient'),    
    path('patient/appointments/<uuid:uid>', views.AppointmentCancelView_Patient.as_view(), name='appointment_cancel_patient'), 
    path('organization/appointments', views.AppointmentRequestListView_OrganizationView.as_view(), name='organization_appointment_list'), 
    path('organization/appointments/<uuid:uid>', views.AppointmentApproval_OrganizationView.as_view(), name='appointment_approval'), 
    path('doctor/appointments', views.AppointmentListView_Doctor.as_view(), name='appointment_list_doctor'), 
]