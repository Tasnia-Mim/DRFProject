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
    OrganizationUserProfileSerializer,
)

from core.models import (
    User,
    OrganizationUser,
    Doctor,
    
)

# view for organization user profile

class OrganizationUserProfileView(APIView):

    permission_classes = [OrganizationUserPermission]
    authentication_classes = [JWTAuthentication]
 

    def get_object(self, slug):
        try:            
            return User.objects.get(slug=slug)
        except User.DoesNotExist:
            raise Http404


    @extend_schema(
    request=OrganizationUserProfileSerializer,
    responses={200: OrganizationUserProfileSerializer},
    )   
    def get(self, request,format=None):
        user = self.get_object(request.user.slug)
        serializer = OrganizationUserProfileSerializer(user.organization_user)
        return Response(serializer.data)


    @extend_schema(
    request=OrganizationUserProfileSerializer,
    responses={201: OrganizationUserProfileSerializer},
    )   
    def post(self, request, format=None):
        user = self.get_object(request.user.slug)
        serializer = OrganizationUserProfileSerializer(user.organization_user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) 