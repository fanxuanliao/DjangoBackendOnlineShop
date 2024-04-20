from django.shortcuts import render

from .models import Order
from .serializers import OrderSerializer

from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response

from django.core.mail import send_mail
from django.core.mail import EmailMessage
from backend.settings import EMAIL_HOST_USER

# Create your views here.

class OrderView(APIView):
    def get(self, request):
        try:
            orders = Order.objects.all()
            serializer = OrderSerializer(orders, many=True)
            return Response({
                'data': serializer.data,
                'message': "Order fetched successfully."
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                'data': {},
                'message': "Oops! Something went wrong when fetching orders."
            }, status=status.HTTP_400_BAD_REQUEST)
        
    def post(self, request):
        try:
            data = request.data
            serializer = OrderSerializer(data=request.data)
            if serializer.is_valid():

                # implement mail notifications
                subject = "New Order is Placed!"
                message = "Dear Customer,\n\nYour order has been placed successfully.\n\nThank you for shopping with us.\n\nRegards,\nOnline Shop Team"
                recipient_list = [data['customer_email']]
                send_mail(subject,message,EMAIL_HOST_USER,recipient_list,fail_silently=False)

                serializer.save()
                return Response({
                    'data': serializer.data,
                    'message': "Order created successfully."
                }, status=status.HTTP_201_CREATED)
            else:
                return Response({
                    'data': serializer.errors,
                    'message': "Oops! Something went wrong when creating order."
                }, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({
                'data': {},
                'message': "Oops! Something went wrong when creating order."
            }, status=status.HTTP_400_BAD_REQUEST)
            
        
    def patch(self, request):
        try:
            data = request.data
            orderToUpdate = Order.objects.filter(id=data['id']) # make sure to id is in data
            if orderToUpdate.exists():
                serializer = OrderSerializer(orderToUpdate[0], data=data, partial=True)

                if not serializer.is_valid():
                    return Response({
                        'data': serializer.errors,
                        'message': "Oops! Something went when parsing request."
                    }, status=status.HTTP_500_BAD_REQUEST)
                
                serializer.save()
                return Response({
                    'data': serializer.data,
                    'message': "Order is updated successfully."
                }, status=status.HTTP_200_OK)
            else:
                return Response({
                    'data': {},
                    'message': "Oops! Order is not found with id: {}".format(data['id'])
                }, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({
                'data': {},
                'message': "Oops! Something went wrong when updating order."
            }, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request):
        try:
            data = request.data
            orderToDelete = Order.objects.filter(id=data['id']) # make sure to id is in data
            if orderToDelete.exists():
                orderToDelete[0].delete()
                return Response({
                    'data': {},
                    'message': "Order is deleted successfully."
                }, status=status.HTTP_200_OK)
            else:
                return Response({
                    'data': {},
                    'message': "Oops! Order is not found with id: {}".format(data['id'])
                }, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({
                'data': {},
                'message': "Oops! Something went wrong when deleting order."
            }, status=status.HTTP_400_BAD_REQUEST)