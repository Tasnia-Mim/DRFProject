from django.db.models.signals import post_save
from django.dispatch import receiver

from django.contrib.auth import get_user_model, authenticate
from rest_framework import serializers

from core.models import (
    User,      
    Patient,
    Doctor,
    Blog,
)


class BlogViewSerializer(serializers.Serializer):
    blogger = serializers.CharField(max_length=100, required=False)
    tittle =  serializers.CharField(max_length=200, required= False) 
    blog = serializers.CharField(max_length=500, required=True)
    read_only_fields = ['blogger'] 
 



class BlogSerializer(serializers.Serializer):
    tittle =  serializers.CharField(max_length=200, required= False) 
    blog = serializers.CharField(max_length=500, required=False)

    def create(self, validated_data):
        blog = Blog()
        blog.blogger = self.context['request'].user
        blog.tittle = validated_data.get('tittle')
        blog.blog = validated_data.get('blog')
        blog.save()
        return blog


class BlogUpdateSerializer(serializers.Serializer):
    tittle =  serializers.CharField(max_length=200, required= False) 
    blog = serializers.CharField(max_length=500, required=False)


    def update(self, instance, validated_data):       
        instance.tittle = validated_data.get('tittle', instance.tittle)        
        instance.blog = validated_data.get('blog', instance.blog) 
        instance.save()
        return instance 
