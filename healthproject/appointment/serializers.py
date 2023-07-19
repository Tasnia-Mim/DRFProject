from django.db.models.signals import post_save
from django.dispatch import receiver

from django.contrib.auth import get_user_model, authenticate
from rest_framework import serializers

from core.models import (
    User,      
    Patient,
    Doctor,
    Appointment,
)



class AppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = ['doctor','patient','request_time', 'problem', 'appointment_time', 'fee', 'appointment_status']
    

class AppointmentRequest_PatientSerializer(serializers.Serializer):
    doctor = serializers.SlugRelatedField(
        queryset=User.objects.filter(),
        write_only=True,
        slug_field="uid",       
    )    
    problem = serializers.CharField(max_length=250, required=True)

    def create(self, validated_data): 
        appointment = Appointment() 
        appointment.patient = self.context['request'].user       
        appointment.doctor = validated_data.get('doctor')
        appointment.problem = validated_data.get('problem')
        appointment.save()
        return appointment   

    


class AppointmentApproval_OrganizationSerializer(serializers.Serializer): 
    appointment_time  =  serializers.DateTimeField(required=True)   
    fee =  serializers.CharField(max_length=50, required=True)
    appointment_status = serializers.ChoiceField(choices = ['approved', 'canceled', 'pending'], allow_blank=False)

    def update(self, instance, validated_data): 
        instance.appointment_time = validated_data.get('appointment_time', instance.appointment_time)             
        instance.fee = validated_data.get('fee', instance.fee)
        instance.appointment_status = validated_data.get('appointment_status', instance.appointment_status)
        instance.save()
        return instance   

    

    