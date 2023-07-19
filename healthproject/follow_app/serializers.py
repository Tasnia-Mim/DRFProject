from django.db.models.signals import post_save
from django.dispatch import receiver

from django.contrib.auth import get_user_model, authenticate
from rest_framework import serializers

from core.models import (
    User,      
    Patient,
    DoctorFollow,
    PatientFollow,
)

class FollowRequestSerializer_Patient(serializers.Serializer):    
    receiver_uid = serializers.SlugRelatedField(
        queryset=User.objects.filter(),
        write_only=True,
        slug_field="uid",       
    )  

    def create(self, validated_data):
        follow = PatientFollow()
        follow.sender = self.context['request'].user
        follow.receiver = validated_data.get('receiver_uid')
        follow.save()
        return follow  




class FollowListSerializer_Patient(serializers.Serializer):
    sender = serializers.CharField(max_length=250, required=False)   
    receiver = serializers.CharField(max_length=250, required=False)   
       
    

class FollowListSerializer_Doctor(serializers.Serializer):
    sender = serializers.CharField(max_length=250, required=False)   
    receiver = serializers.CharField(max_length=250, required=False)   
    follow_status = serializers.CharField(max_length=250, required=False)   



class FollowSerializer_Doctor(serializers.Serializer): 
    receiver_uid = serializers.SlugRelatedField(
        queryset=User.objects.filter(),
        write_only=True,
        slug_field="uid",       
    )    
    


    def create(self, validated_data):
        follow = DoctorFollow()
        follow.sender = self.context['request'].user
        follow.receiver = validated_data.get('receiver_uid')
        follow.follow_status = 'pending'
        follow.save()
        return follow  




class FollowBackSerializer_Doctor(serializers.Serializer): 
    follow_status = serializers.ChoiceField(choices = ['approved', 'canceled', 'pending'], allow_blank=False)


    def update(self, instance, validated_data):            
        instance.follow_status = validated_data.get('follow_status', instance.follow_status)
        instance.save()
        return instance 
