from django.shortcuts import render

from drf_spectacular.utils import extend_schema

from django.contrib.auth.models import User

from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from rest_framework.views import APIView
from rest_framework.response import Response

from core.permissions import PatientPermission, DoctorPermission
from core.models import (
    User,
    Patient, 
    DoctorFollow,
    PatientFollow,       
)

from .serializers import (       
    FollowRequestSerializer_Patient,
    FollowListSerializer_Patient,
    FollowListSerializer_Doctor,     
    FollowSerializer_Doctor,
    FollowBackSerializer_Doctor,
)


class FollowingView_Patient(APIView):  #post request to follow a doctor by patient view
    permission_classes = [PatientPermission]
    authentication_classes = [JWTAuthentication]

    @extend_schema(
    request=FollowRequestSerializer_Patient,
    responses={201: FollowRequestSerializer_Patient},
    )   
    def post(self, request, format=None):
        serializer = FollowRequestSerializer_Patient(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
 
class FollowingListView_Patient(APIView): # get request to view the followed doctor from patient

    permission_classes = [PatientPermission]
    authentication_classes = [JWTAuthentication]

    @extend_schema(
    request=FollowListSerializer_Patient,
    responses={200: FollowListSerializer_Patient},
    ) 
    def get(self, request):
        following_list = PatientFollow.objects.filter(sender = request.user)
        serializer = FollowListSerializer_Patient(following_list, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




class FollowingCancelView_Patient(APIView): #cancel "follow" from patient view
    permission_classes = [PatientPermission]
    authentication_classes = [JWTAuthentication]

    @extend_schema(
    request=FollowListSerializer_Patient,
    responses={204: FollowListSerializer_Patient},
    ) 
    def delete(self, request, uid, format=None):        
        follow = PatientFollow.objects.get(uid=uid)
        follow.delete()
        return Response({
            'msg': 'deleted successfully'
        }, status=status.HTTP_204_NO_CONTENT)



class FollowingRequestView_Doctor(APIView):  #post follow request from doctor to doctor from doctor view
    permission_classes = [DoctorPermission]
    authentication_classes = [JWTAuthentication]    

    @extend_schema(
    request=FollowSerializer_Doctor,
    responses={201: FollowSerializer_Doctor},
    ) 
    def post(self, request, format=None):        
        serializer = FollowSerializer_Doctor(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class FollowingListView_Doctor(APIView):   #get a list of followed doctors from doctor view

    permission_classes = [DoctorPermission]
    authentication_classes = [JWTAuthentication]    


    @extend_schema(
    request=FollowListSerializer_Doctor,
    responses={200: FollowListSerializer_Doctor},
    ) 
    def get(self, request, format=None): 
        follow_list = DoctorFollow.objects.filter(sender=request.user)         
        serializer = FollowListSerializer_Doctor(follow_list, many=True)        
        return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) 



class FollowingCancelView_Doctor(APIView):  # cancel a "follow" from doctor view

    permission_classes = [DoctorPermission]
    authentication_classes = [JWTAuthentication]

    @extend_schema(
    request=FollowListSerializer_Doctor,
    responses={204: FollowListSerializer_Doctor},
    ) 
    def delete(self, request, uid, format=None):        
        follow = DoctorFollow.objects.get(uid=uid)
        follow.delete()
        return Response({
            'msg': 'deleted successfully'
        }, status=status.HTTP_204_NO_CONTENT)



class FollowReceiveListView_Doctor(APIView):    #get a list of "follow" invitaions from other doctors from doctor view

    permission_classes = [DoctorPermission]
    authentication_classes = [JWTAuthentication]
    

    @extend_schema(
    request=FollowListSerializer_Doctor,
    responses={200: FollowListSerializer_Doctor},
    ) 
    def get(self, request, format=None): 
        follow_list = DoctorFollow.objects.filter(receiver=request.user)         
        serializer = FollowListSerializer_Doctor(follow_list, many=True)        
        return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) 



class FollowBackView_Doctor(APIView): # "follow back" a particular doctor from doctor view

    permission_classes = [DoctorPermission]
    authentication_classes = [JWTAuthentication]    

    @extend_schema(
    request=FollowBackSerializer_Doctor,
    responses={206: FollowBackSerializer_Doctor},
    ) 
    def put(self, request, uid, format=None):  
        follow = DoctorFollow.objects.get(uid=uid)     
        serializer = FollowBackSerializer_Doctor(follow, data=request.data, context={'request': request}, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)













    
    

        




    