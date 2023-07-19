from django.shortcuts import render

from drf_spectacular.utils import extend_schema

from django.contrib.auth.models import User

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from rest_framework.permissions import IsAuthenticated
from core.permissions import PatientPermission, DoctorPermission
from rest_framework_simplejwt.authentication import JWTAuthentication


from .serializers import (
    PrescriptionSerializer,
    PrescriptionDetailSerializer,    
)

from core.models import (
    User,
    Patient,    
    Doctor,  
    Prescription,  
    
)


#only doctor has the prescription create permission. But a doctor cannot update or delete a prescription. patient and doctor can see the prescription list. 

class PrescriptionCreateView_Doctor(APIView):  

    permission_classes = [DoctorPermission]
    authentication_classes = [JWTAuthentication]

    @extend_schema(
    request=PrescriptionSerializer,
    responses={201: PrescriptionSerializer},
    )   
    def post(self, request, format=None):
        serializer = PrescriptionSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class PrescriptionListView_Doctor(APIView):

    permission_classes = [DoctorPermission]
    authentication_classes = [JWTAuthentication]

    
    @extend_schema(
    request=PrescriptionDetailSerializer,
    responses={200 : PrescriptionDetailSerializer},
    )  
    def get(self, request, format = None):
        prescriptions = Prescription.objects.filter(doctor=request.user)
        serializer = PrescriptionDetailSerializer(prescriptions, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class PrescriptionDetailView_Doctor(APIView):

    permission_classes = [DoctorPermission]
    authentication_classes = [JWTAuthentication]

    @extend_schema(
    request=PrescriptionDetailSerializer,
    responses={200: PrescriptionDetailSerializer},
    ) 
    def get(self, request, uid, format = None):
        prescription = Prescription.objects.get(uid=uid, doctor=request.user)
        serializer = PrescriptionDetailSerializer(prescription)
        return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




class PrescriptionListView_Patient(APIView):

    permission_classes = [PatientPermission]
    authentication_classes = [JWTAuthentication]    
 

    @extend_schema(
    request=PrescriptionDetailSerializer,
    responses={200: PrescriptionDetailSerializer},
    )  
    def get(self, request, format = None):
        prescriptions = Prescription.objects.filter(patient=request.user)
        serializer = PrescriptionDetailSerializer(prescriptions, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class PrescriptionDetailView_Patient(APIView):

    permission_classes = [PatientPermission]
    authentication_classes = [JWTAuthentication]

    @extend_schema(
    request=PrescriptionDetailSerializer,
    responses={200: PrescriptionDetailSerializer},
    ) 
    def get(self, request, uid, format = None):
        prescription = Prescription.objects.get(uid=uid, patient=request.user)
        serializer = PrescriptionDetailSerializer(prescription)
        return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



