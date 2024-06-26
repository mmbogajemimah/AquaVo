from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_200_OK, HTTP_404_NOT_FOUND, HTTP_204_NO_CONTENT
from .models import Refill
from .serializers import RefillSerializer
from rest_framework.permissions import IsAdminUser
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from accounts.models import CustomUser

# Create your views here.
# @method_decorator(csrf_exempt, name='dispatch')
class CreateRefillView(APIView):
    serializer_class = RefillSerializer
    permission_classes = [IsAdminUser]
    
    def post(self, request, format=None):
        customer_name = request.data.get('customer_username')
        print("Customer Name =>>",customer_name)
        
        request.data['customer_name'] = customer_name
        serializer = RefillSerializer(data=request.data)
        print("Request Data :: ",request.data)
        if serializer.is_valid():
            serializer.save(customer=request.user)
            return Response(serializer.data, status=HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
            
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
      
# Get Refill by Id
class GetRefillByIdView(APIView):
    permission_classes = [IsAdminUser] 
    
    def get(self, request, refill_id, format=None):
        #Get the refill object by its Id
        try:
            refill = Refill.objects.get(id=refill_id)
            serializer = RefillSerializer(refill)
            return Response({
                "status": "Success",
                "data": serializer.data
            }, status=HTTP_200_OK) 
        except Refill.DoesNotExist:
            return Response({
                "status": "Failed to get Refill by Id",
                "message": "Refill not found"
            }, status=HTTP_404_NOT_FOUND)
# Update Refill
class UpdateRefillView(APIView):
    permission_classes = [IsAdminUser]
    def patch(self, request, refill_id, format=None):
        try:
            refill = Refill.objects.get(id=refill_id)
        except Refill.DoesNotExist:
            return Response(
                {"detail": "Refill not found"},
                status=HTTP_404_NOT_FOUND
            )
        serializer = RefillSerializer(refill, data=request.data)
        #Check if the data is valid
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=HTTP_200_OK)
        else:
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
        
class DeleteRefillView(APIView):
    #Only Admins can access this endpoint
    permission_classes = [IsAdminUser]
    
    def delete(self, request, refill_id, format=None):
        #Get the refill object based on the refill_id
        try:
            refill = Refill.objects.get(id=refill_id)
        except Refill.DoesNotExist:
            #If refill object is not found, return a 404 response
            return Response(
                {"detail": "Refill not found"},
                status=HTTP_400_BAD_REQUEST
            )
        #Delete the refill object
        refill.delete()
        #Return a success messahe in the response
        return Response(
            {"message": "Refill deleted successfully"},
            status=HTTP_204_NO_CONTENT
        )
        