from django.shortcuts import render

from drf_spectacular.utils import extend_schema

from django.contrib.auth.models import User

from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from rest_framework.views import APIView
from rest_framework.response import Response


from core.permissions import DoctorPermission


from core.models import (
    User,
    Doctor,
    Blog,    
)


from .serializers import (      
    BlogSerializer, 
    BlogUpdateSerializer, 
    BlogViewSerializer,  
)


#is Blog system is only enable for doctor. Only doctors can create, update, delete blogs 


class BlogCreatView(APIView):   

    permission_classes = [DoctorPermission]
    authentication_classes = [JWTAuthentication]  

   
    @extend_schema(
    request=BlogSerializer,
    responses={201: BlogSerializer},
    )   

    def post(self, request, format=None):
        serializer = BlogSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class BlogList(APIView):

    permission_classes = [DoctorPermission]
    authentication_classes = [JWTAuthentication]    

    @extend_schema(
    request=BlogViewSerializer,
    responses={200: BlogViewSerializer},
    )  

    def get(self, request, format=None):
        blogs = Blog.objects.filter(blogger = request.user)
        serializer = BlogViewSerializer(blogs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class BlogDetailView(APIView):

    permission_classes = [DoctorPermission]
    authentication_classes = [JWTAuthentication]

    @extend_schema(
    request=BlogViewSerializer,
    responses={200: BlogViewSerializer},
    )  
    def get(self, request, uid, format=None):
        blog = Blog.objects.get(uid=uid)
        serializer = BlogViewSerializer(blog)
        return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    
    @extend_schema(
    request=BlogUpdateSerializer,
    responses={200: BlogUpdateSerializer},
    ) 
    def put(self, request, uid, format=None):
        blog = Blog.objects.get(uid=uid)
        serializer = BlogUpdateSerializer(blog, data=request.data,  partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    @extend_schema(
    request=BlogSerializer,
    responses={204: BlogSerializer},
    )
    def delete(self, request, uid, format=None):
        blog = Blog.objects.get(uid=uid)
        blog.delete()
        return Response({
            'msg': 'deleted successfully'
        }, status=status.HTTP_204_NO_CONTENT)














    





