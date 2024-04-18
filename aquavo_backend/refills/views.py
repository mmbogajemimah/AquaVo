from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_200_OK
from .models import Refill
from .serializers import RefillSerializer
from rest_framework.permissions import IsAdminUser
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

# Create your views here.
@method_decorator(csrf_exempt, name='dispatch')
class CreateRefillView(APIView):
    serializer_class = RefillSerializer
    permission_classes = [IsAdminUser]
    
    def post(self, request, format=None):
        serializer = RefillSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=HTTP_201_CREATED)
        else:
            return Response({
                "status": "Refill creation failed",
                "message": "Invalid input data",
                "errors": serializer.errors
            }, status=HTTP_400_BAD_REQUEST)
            
class GetAllRefillsView(APIView):
    permission_classes = [IsAdminUser]
    
    def get(self, request, format=None):
        refills = Refill.objects.all()
        serializer = RefillSerializer(refills, many=True)
        
        return Response({
            "status": "Success",
            "data": serializer.data
        }, status=HTTP_200_OK)
        
        
class GetRefillsForUserView(APIView):
    permission_classes = [IsAdminUser]
    
    def get(self, request, customer_id, format=None):
        refills = Refill.objects.filter(customer_id=customer_id)
        
        serializer = RefillSerializer(refills, many=True)
        
        return Response({
            'status': "success",
            'data': serializer.data
        }, status=HTTP_200_OK)