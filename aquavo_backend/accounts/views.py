from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import(HTTP_200_OK)
from .models import CustomUser
from .serializers import UserSerializer

# Create your views here.
class AllUsers(APIView):
    serializer_class = UserSerializer
    def get(self, request, format=None):
        users = CustomUser.objects.all()
        all_users = UserSerializer(users, many=True)
        return Response(all_users.data, status=HTTP_200_OK)
    
class GetUserById(APIView):
    serializer_class = UserSerializer
    def get(self, request, user_id, format=None):
        user = CustomUser.objects.filter(id=user_id)
        one_user = UserSerializer(user, many=True)
        return Response(one_user.data, status=HTTP_200_OK)
    
