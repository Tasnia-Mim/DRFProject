from django.shortcuts import render

from drf_spectacular.utils import extend_schema

from django.contrib.auth.models import User

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication


from core.permissions import DoctorPermission, OrganizationUserPermission, PatientPermission


from .serializers import (
    AppointmentRequest_PatientSerializer,  
    AppointmentApproval_OrganizationSerializer,
    AppointmentSerializer,       
)

from core.models import (
    User,
    Patient,
    Appointment, 
    Doctor,    
)


class AppointmentRequestView_Patient(APIView):  #send appointment request for a doctor from patient view

    permission_classes = [PatientPermission]
    authentication_classes = [JWTAuthentication]
    
    @extend_schema(
    request=AppointmentRequest_PatientSerializer,
    responses={201: AppointmentRequest_PatientSerializer},
    )   
    def post(self, request, format=None):            
        serializer = AppointmentRequest_PatientSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AppointmentListView_Patient(APIView):   #get a list of appointments from a patient view

    permission_classes = [PatientPermission]
    authentication_classes = [JWTAuthentication] 

    @extend_schema(
    request=AppointmentSerializer,
    responses={200: AppointmentSerializer},
    )
    def get(self, request, format=None):
        appointments = Appointment.objects.filter(patient = request.user)         
        serializer = AppointmentSerializer(appointments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)




class AppointmentCancelView_Patient(APIView): #cancel a appointment request from a patient view
    
    permission_classes = [PatientPermission]
    authentication_classes = [JWTAuthentication]

    @extend_schema(
    request=AppointmentSerializer,
    responses={204: AppointmentSerializer},
    )
    def delete(self, request, uid, format=None):
        appointment = Appointment.objects.get(uid = uid)
        appointment.delete()
        return Response({
            'msg': 'deleted successfully'
        }, status=status.HTTP_204_NO_CONTENT)


class AppointmentRequestListView_OrganizationView(APIView):  #see appointment list sent from patient from organization_user view

    permission_classes = [OrganizationUserPermission]
    authentication_classes = [JWTAuthentication]
    
    @extend_schema(
    request=AppointmentSerializer,
    responses={200: AppointmentSerializer},
    )
    def get(self, request, format=None):
        appointments = Appointment.objects.all()         
        serializer = AppointmentSerializer(appointments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)



class AppointmentApproval_OrganizationView(APIView):  # approve appointment request, and add appointment time and fee from organization_user view

    permission_classes = [OrganizationUserPermission]
    authentication_classes = [JWTAuthentication]
   

    @extend_schema(
    request=AppointmentApproval_OrganizationSerializer,
    responses={200: AppointmentApproval_OrganizationSerializer},
    )   
    def put(self, request, uid, format=None):
        appointment = Appointment.objects.get(uid=uid)
        serializer = AppointmentApproval_OrganizationSerializer(appointment, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class AppointmentListView_Doctor(APIView):  #see appointment list from a doctor view

    permission_classes = [DoctorPermission]
    authentication_classes = [JWTAuthentication]
    
    @extend_schema(
    request=AppointmentSerializer,
    responses={200: AppointmentSerializer},
    )
    def get(self, request, format=None):
        appointments = Appointment.objects.filter(doctor = request.user)         
        serializer = AppointmentSerializer(appointments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


