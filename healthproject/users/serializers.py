from django.db.models.signals import post_save
from django.dispatch import receiver

from django.contrib.auth import get_user_model, authenticate
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken



from core.models import (
    User,    
    OrganizationUser,
    Doctor,
    Patient,
)


class PatientRegistrationSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    name = serializers.CharField(max_length=100, required=True)
    password = serializers.CharField(write_only=True, required=True)       
   
    
    def create(self, validated_data):      
        user = User()
        user.email = validated_data.get('email')
        user.name = validated_data.get('name')
        user.password = validated_data.get('password')          
        user.is_patient = True
        user.set_password(user.password)
        user.save()
        return user
        return get_user_model().objects.create_user(**validated_data) 





class OrganizationUserRegistrationSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    name = serializers.CharField(max_length=100, required=True)
    password = serializers.CharField(write_only=True, required=True)       
   
    
    def create(self, validated_data):      
        user = User()
        user.email = validated_data.get('email')
        user.name = validated_data.get('name')
        user.password = validated_data.get('password')          
        user.is_organization_user = True
        user.set_password(user.password)
        user.save()
        return user
        return get_user_model().objects.create_user(**validated_data) 



class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True, required=True)  

    def validate(self, validated_data):

        print ('###### validate')
        email = validated_data.get('email')
        password = validated_data.get('password')
        user = authenticate(
            request=self.context.get('request'),
            username=email,
            password=password,
        )

        if not user:
            msg = ('Unable to authenticate with provided credentials.')
            raise serializers.ValidationError(msg, code='authorization')
        
        validated_data['user'] = user
        return validated_data


    def get_jwt_token(self, validated_data):

        print ('###### get_jwt')
        email = validated_data.get('email')
        password = validated_data.get('password')
        user = authenticate(
            request=self.context.get('request'),
            username=email,
            password=password,
        )

        if not user:
            msg = _('invalid credentials.')
            return {'message': 'invalid credentials', 'data': {}}


        refresh = RefreshToken.for_user(user)
        

        return {'message': 'login succesful', 'data': {'token': {'refresh': str(refresh),
        'access': str(refresh.access_token),}}}












@receiver(post_save, sender=User)
def create_user_profile(instance, sender, created, **kwargs):
    print('****', created)
    if instance.is_doctor:
        Doctor.objects.get_or_create(user=instance)    
    if instance.is_organization_user:
        OrganizationUser.objects.get_or_create(user=instance)
    if instance.is_patient:
        Patient.objects.get_or_create(user=instance)  
        