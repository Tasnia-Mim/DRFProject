from django.urls import path

from . import views

app_name = 'follow_app'


urlpatterns = [
    path('patient/followings/follow', views.FollowingView_Patient.as_view(), name='followcreate_patient'),
    path('patient/followings', views.FollowingListView_Patient.as_view(), name='following_patient'),    
    path('patient/followings/<uuid:uid>', views.FollowingCancelView_Patient.as_view(), name='follow_cancel_patient'),      
    path('doctor/followings/follow', views.FollowingRequestView_Doctor.as_view(), name='following_doctor'),
    path('doctor/followings', views.FollowingListView_Doctor.as_view(), name='following_list_doctor'), 
    path('doctor/following/<uuid:uid>', views.FollowingCancelView_Doctor.as_view(), name='follow_cancel_doctor'),   
    path('doctor/followed_bys', views.FollowReceiveListView_Doctor.as_view(), name='follow_list_received_doctor'),    
    path('doctor/followed_bys/follow-back<uuid:uid>', views.FollowBackView_Doctor.as_view(), name='follow_back_doctor'),       
    
]
