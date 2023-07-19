from django.db.models.signals import post_save
from django.dispatch import receiver

from django.contrib.auth import get_user_model, authenticate
from rest_framework import serializers

from phonenumber_field.serializerfields import PhoneNumberField

from core.models import (
    User,      
    Patient,
)


class PatientProfileSerializer(serializers.Serializer):
    blood_group = serializers.CharField(max_length=100, allow_blank=False)
    weight = serializers.CharField(max_length=100, allow_blank=False)   
    height = serializers.CharField(max_length=100, allow_blank=False)     
    address = serializers.CharField(max_length=100, allow_blank=False)
    phone = PhoneNumberField(allow_blank=False)
    gender = serializers.ChoiceField(choices = ['Male', 'Female', 'Others'], allow_blank=False)

    def update(self, instance, validated_data):       
        instance.blood_group = validated_data.get('blood_group', instance.blood_group)
        instance.weight = validated_data.get('weight', instance.weight)        
        instance.height = validated_data.get('height', instance.height)        
        instance.address = validated_data.get('address', instance.address)
        instance.phone = validated_data.get('phone', instance.phone)        
        instance.gender = validated_data.get('gender', instance.gender)
        instance.save()
        return instance
