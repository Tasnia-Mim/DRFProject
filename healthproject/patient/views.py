from django.shortcuts import render

from drf_spectacular.utils import extend_schema

from django.contrib.auth.models import User

from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from rest_framework.views import APIView
from rest_framework.response import Response


from core.permissions import PatientPermission


from core.models import (
    User,
    Patient,    
    
)


from .serializers import (      
    PatientProfileSerializer,    
)

#view for Patient profile

class PatientProfileView(APIView):

    permission_classes = [PatientPermission]
    authentication_classes = [JWTAuthentication]

    def get_object(self, slug):
        try:           
            return User.objects.get(slug=slug)
        except User.DoesNotExist:
            raise Http404

    @extend_schema(
    request=PatientProfileSerializer,
    responses={200: PatientProfileSerializer},
    )   
    def get(self, request, format=None):
        user = self.get_object(request.user.slug)
        serializer = PatientProfileSerializer(user.patient)
        return Response(serializer.data)


    @extend_schema(
    request=PatientProfileSerializer,
    responses={201: PatientProfileSerializer},
    )   
    def post(self, request, format=None):
        user = self.get_object(request.user.slug)
        serializer = PatientProfileSerializer(user.patient, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



    @extend_schema(
    request=PatientProfileSerializer,
    responses={204: PatientProfileSerializer},
    ) 
    def delete(self, request, id=None):
        user = self.get_object(request.user.slug)
        user.delete()
        return Response({
            'msg': 'deleted successfully'
        }, status=status.HTTP_204_NO_CONTENT)