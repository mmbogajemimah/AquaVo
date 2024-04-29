from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import(HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_201_CREATED)
from .models import CustomUser
from .serializers import UserSerializer, RegistrationSerializer, CustomerSerializer
from django.contrib.auth.hashers import make_password
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from aquavo_backend.settings import EMAIL_HOST_USER, TOKEN_EXPIRED_AFTER_SECONDS
from django.core.mail import send_mail
from django.contrib.auth import logout
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from aquavo_backend.views import AuthenticatedAPIView

from django.utils import timezone
import datetime
from datetime import timedelta


# Create your views here.
# Gets All the Users in the System
class AllUsers(APIView):
    serializer_class = UserSerializer
    def get(self, request, format=None):
        users = CustomUser.objects.all()
        all_users = UserSerializer(users, many=True)
        return Response(all_users.data, status=HTTP_200_OK)

# Gets a Single User in the System by their ID
class GetUserById(AuthenticatedAPIView):
    serializer_class = UserSerializer
    def get(self, request, user_id, format=None):
        user = CustomUser.objects.filter(id=user_id)
        one_user = UserSerializer(user, many=True)
        return Response(one_user.data, status=HTTP_200_OK)

#Updates Users Information
class UpdateUser(AuthenticatedAPIView):
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
            
class DeleteUserById(AuthenticatedAPIView):
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
            data_saved.username = request.data['firstname'] + ' ' + request.data['lastname']
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
            
@method_decorator(csrf_exempt, name='dispatch')
class Login(APIView):
    serializer_class = UserSerializer
    def post(self, request, format=None):
        # user_data = CustomUser.objects.get(email=request.data['username'])
        username = request.data['username']
        password = request.data['password']
        
        if username is None or password is None:
            return Response({'error': "Provide your username and password kindly"}, status=HTTP_400_BAD_REQUEST)
        user = authenticate(username=username, password=password)
        if not user:
            return Response({'error': "The Credentials provided are Invalid"}, status=HTTP_400_BAD_REQUEST)
        else:
            token, _ = Token.objects.get_or_create(user=user)
            print(token)
            # token, _ = Token.objects.create(user=user)
            is_expired, token = token_expire_handler(token)
            single_user = CustomUser.objects.filter(id=token.user_id)
            print(single_user)
            filtered_user = UserSerializer(single_user, many=True)
            
            return Response({
                'user': filtered_user.data,
                'Expiry_date': expires_in(token),
                'token': token.key
            }, status=HTTP_200_OK)
            
class CreateCustomer(APIView):
    def post(self, request, format=None):
        serializer = CustomerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=HTTP_201_CREATED)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
            

from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import logout

class Logout(AuthenticatedAPIView):
    def post(self,request,format=None):
        request.user.auth_token.delete()
        logout(request)
        return Response({"message":"Logged Out"})
    
class TotalUsers(APIView):
    def get(self, request, format=None):
        total_users = CustomUser.objects.count()
        return Response({ total_users}, status=HTTP_200_OK)
    
def expires_in(token):
    time_elapsed = timezone.now() - token.created
    time_left = timedelta(seconds = TOKEN_EXPIRED_AFTER_SECONDS) - time_elapsed
    return time_left

def is_token_expired(token):
    return expires_in(token) < timedelta(seconds = 0)
    
def token_expire_handler(token):
    is_expired = is_token_expired(token)
    if is_expired:
        token.delete()
        token = Token.objects.create(user = token.user)
    return is_expired, token