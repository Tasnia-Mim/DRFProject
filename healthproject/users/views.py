import json
from django.shortcuts import render
from drf_spectacular.utils import extend_schema
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.core.serializers import serialize
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import serializers

from core.permissions import DoctorPermission, OrganizationUserPermission

from .serializers import (   
    PatientRegistrationSerializer,   
    OrganizationUserRegistrationSerializer,
    LoginSerializer,        
)

from core.models import (
    User,
    OrganizationUser,
    Doctor,
    Patient,    
)


# to create a doctor account, one must have super user credentials. So this can be done from admin page. 

class PatientRegistrationView(APIView):   #registration for patient type user

    @extend_schema(
    request=PatientRegistrationSerializer,
    responses={201: PatientRegistrationSerializer},
    )
    def post(self, request, format=None):
        serializer = PatientRegistrationSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




class OrganizationUserRegistrationView(APIView):  #registration for organization user

    @extend_schema(
    request=OrganizationUserRegistrationSerializer,
    responses={201: OrganizationUserRegistrationSerializer},
    )
    def post(self, request, format=None):
        serializer = OrganizationUserRegistrationSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


 
class LoginView(APIView):   # login for all kind of user

    @extend_schema(
    request=LoginSerializer,
    responses={201: LoginSerializer},
    )
    def post(self, request, format=None):
     
        print ('###### try')        
        serializer = LoginSerializer(data = request.data)
        if serializer.is_valid():
            response = serializer.get_jwt_token(validated_data = request.data)
            return Response(response, status = status.HTTP_200_OK)
                
        return Response({'message':'something went wrong'}, status=status.HTTP_400_BAD_REQUEST)

