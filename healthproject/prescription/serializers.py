from django.db.models.signals import post_save
from django.dispatch import receiver

from django.contrib.auth import get_user_model, authenticate
from rest_framework import serializers

from core.models import (
    User,   
    OrganizationUser,
    Patient,
    Doctor,
    Medicine,
    Prescription,
)


class PrescriptionSerializer(serializers.Serializer):
    patient_email = serializers.SlugRelatedField(
        queryset=User.objects.filter(),
        write_only=True,
        slug_field="email",       
    )  
    treatment = serializers.CharField(max_length=250, required=False)
    medicine_uid = serializers.SlugRelatedField(
        queryset=Medicine.objects.filter(),
        write_only=True,
        slug_field="uid",       
    )

    def create(self, validated_data):
        prescription = Prescription()
        prescription.doctor = self.context['request'].user
        prescription.patient = validated_data.get('patient_email')
        prescription.treatment = validated_data.get('treatment')
        prescription.medicine = validated_data.get('medicine_uid')      
        prescription.save()
        return prescription
       


class PrescriptionDetailSerializer(serializers.ModelSerializer):

    class Meta: 
        model = Prescription
        fields = '__all__'
