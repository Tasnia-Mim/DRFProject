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
    DoctorProfileSerializer,    
)

from core.models import (
    User,
    OrganizationUser,
    Doctor,    
)


class DoctorProfileView(APIView):    
    permission_classes = [DoctorPermission]
    authentication_classes = [JWTAuthentication]


    def get_object(self, slug):
        try:           
            return User.objects.get(slug=slug)
        except User.DoesNotExist:
            raise Http404


    @extend_schema(
    request=DoctorProfileSerializer,
    responses={200: DoctorProfileSerializer},
    )   
    def get(self, request, format=None):
        user = self.get_object(request.user.slug)
        serializer = DoctorProfileSerializer(user.doctor)
        return Response(serializer.data)


    @extend_schema(
    request=DoctorProfileSerializer,
    responses={201: DoctorProfileSerializer},
    )   
    def post(self, request, format=None):
        user = self.get_object(request.user.slug)
        serializer = DoctorProfileSerializer(user.doctor, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)