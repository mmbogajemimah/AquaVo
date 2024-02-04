from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import(HTTP_200_OK, HTTP_400_BAD_REQUEST)
from .models import CustomUser
from .serializers import UserSerializer

# Create your views here.
# Gets All the Users in the System
class AllUsers(APIView):
    serializer_class = UserSerializer
    def get(self, request, format=None):
        users = CustomUser.objects.all()
        all_users = UserSerializer(users, many=True)
        return Response(all_users.data, status=HTTP_200_OK)

# Gets a Single User in the System by their ID
class GetUserById(APIView):
    serializer_class = UserSerializer
    def get(self, request, user_id, format=None):
        user = CustomUser.objects.filter(id=user_id)
        one_user = UserSerializer(user, many=True)
        return Response(one_user.data, status=HTTP_200_OK)

#Updates Users Information
class UpdateUser(APIView):
    serializer_class = UserSerializer
    def patch(self, request, user_id, format=None):
        one_user = CustomUser.objects.get(id=user_id)
        request.data['password'] = one_user.password
        user_update = UserSerializer(one_user, data=request.data)
        if user_update.is_valid():
            user_update.save()
            return Response(user_update.data, status=HTTP_200_OK)
        else:
            print(user_update.errors)
            return Response({
                "status": "Update Has Failed",
                "message": "Current User has not been updated",
                "data": "The User Has not been Updated"
            }, status=HTTP_400_BAD_REQUEST)
            
class DeleteUserById(APIView):
    serializer_class = UserSerializer
    def delete(self, request, user_id, format=None):
        """
        Delete User by Id
        """
        CustomUser.objects.get(id=user_id).delete()
        return Response({
            "status": "OK",
            "message": "User Deleted Successfully",
            "data": "The User has been deleted Successfully"
        }, status=HTTP_200_OK)