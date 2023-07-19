from django.db.models.signals import post_save
from django.dispatch import receiver

from django.contrib.auth import get_user_model, authenticate
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken

from phonenumber_field.serializerfields import PhoneNumberField

from core.models import (
    User,    
    OrganizationUser,
    Doctor,
    
)
   
class DoctorProfileSerializer(serializers.Serializer):     
    speciality = serializers.CharField(max_length=100, allow_blank=False)
    chamber_email = serializers.CharField(max_length=100, allow_blank=False)
    chamber_phone = serializers.CharField(max_length=100, allow_blank=False)
    personal_address = serializers.CharField(max_length=100, allow_blank=False)
    personal_phone = PhoneNumberField(allow_blank=False)       
    intro = serializers.CharField(style={'base_template': 'textarea.html'}, allow_blank=False)
    gender = serializers.ChoiceField(choices = ['Male', 'Female', 'Others'], allow_blank=False)

    def update(self, instance, validated_data):        
        instance.speciality = validated_data.get('speciality', instance.speciality)
        instance.chamber_email = validated_data.get('chamber_email', instance.chamber_email)
        instance.chamber_phone = validated_data.get('chamber_phone', instance.chamber_phone)
        instance.personal_address = validated_data.get('personal_address', instance.personal_address)
        instance.personal_phone = validated_data.get('personal_phone', instance.personal_phone) 
        instance.intro = validated_data.get('intro', instance.intro)
        instance.gender = validated_data.get('gender', instance.gender)
        instance.save()
        return instance