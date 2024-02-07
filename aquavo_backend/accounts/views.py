from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import(HTTP_200_OK, HTTP_400_BAD_REQUEST)
from .models import CustomUser
from .serializers import UserSerializer, RegistrationSerializer
from django.contrib.auth.hashers import make_password
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from aquavo_backend.settings import EMAIL_HOST_USER
from django.core.mail import send_mail


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
        
@method_decorator(csrf_exempt, name='dispatch')
class Register(APIView):
    serializer_class = RegistrationSerializer
    def post(self, request,format=None):
        user_data = RegistrationSerializer(data=request.data)
        if user_data.is_valid():
            data_saved = user_data.save(password = make_password(request.data['password']))
            data_saved.username = request.data['first_name'] + ' ' + request.data['last_name']
            data_saved.save()
            email = request.data['email']
            html_content = f'''
                <html>
                <head>
                    <style>
                        body {{
                            font-family: Arial, sans-serif;
                            background-color: #f4f4f4;
                            color: #333;
                        }}
                        .container {{
                            max-width: 600px;
                            margin: 0 auto;
                            padding: 20px;
                            background-color: #fff;
                            border-radius: 5px;
                            box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
                        }}
                        h1 {{
                            font-size: 24px;
                            color: #333;
                            text-align: center;
                            margin-bottom: 20px;
                        }}
                        p {{
                            font-size: 16px;
                            line-height: 1.5;
                            margin-bottom: 10px;
                        }}
                        strong {{
                            font-weight: bold;
                        }}
                    </style>
                </head>
                <body>
                    <div class="container">
                        <h1>Welcome to Aquavo</h1>
                        <p>Please log in to Aquavo using the following details:</p>
                        <p><strong>Username:</strong> {email}</p>
                        <p><strong>Password:</strong> {request.data["password"]}</p>
                    </div>
                </body>
                </html>
                '''

            subject = 'You have been successfully Added to Aquavo Vendors System',
            
            send_user_email = send_mail(
                subject, '', EMAIL_HOST_USER, [email], html_message=html_content
            )
            
            return Response(RegistrationSerializer(data_saved).data, status=200)
        else:
            print(user_data.errors)
            return Response({
                "status": "Registration has Failed",
                "message": "Failed to Register User",
                "data": "Failed Registration"
            }, status=HTTP_400_BAD_REQUEST)