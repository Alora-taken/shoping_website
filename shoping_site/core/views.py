from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import render
from django.contrib.auth import get_user_model, logout
from django.contrib.sessions.models import Session
from rest_framework import status
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from rest_framework.parsers import JSONParser
from .models import CustomUser, Address, Product, ProductCategory
from .serializers import UserProfileSerializer, AddressSerializer, ProductSerializer, ProductCategorySerializer
class IsAuthenticated(IsAuthenticated):
    """
    Allows access only to authenticated users.
    """

    def has_permission(self,request, view):
        if request.COOKIES.get('login_token') != '' and CustomUser.objects.filter(token=request.COOKIES.get('login_token')).exists():
            return True

@api_view(['GET'])
def filter_products(request, category_id):
    category_name = ProductCategory.objects.get(id=category_id)
    products = Product.objects.filter(categories__name=category_name).exclude(is_deleted=True)
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def get_categories(request):
    categories = ProductCategory.objects.filter(is_sub_cat = False).exclude(is_deleted=True)
    serializer = ProductCategorySerializer(categories, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def get_sub_categories(request):
    categories = ProductCategory.objects.filter(is_sub_cat = Tr).exclude(is_deleted=True)
    serializer = ProductCategorySerializer(categories, many=True)
    return Response(serializer.data)

@csrf_exempt
@require_http_methods(["GET"])
def get_products(request):
    products = Product.objects.all()
    serializer = ProductSerializer(products, many=True)
    return JsonResponse(serializer.data, safe=False)

class AddressListView(APIView):
    def get(self, request):
        if request.COOKIES.get('login_token') != '' and CustomUser.objects.filter(token=request.COOKIES.get('login_token')).exists():
            user_token = request.COOKIES.get('login_token')
            user = get_user_model().objects.get(token=user_token)
            addresses = Address.objects.filter(customer=user)
            serializer = AddressSerializer(addresses, many=True)
            return Response(serializer.data)

class AddressListApiViewSet(ModelViewSet):
    queryset = Address.objects.all()
    serializer_class = AddressSerializer
    def get_queryset(self):
        if self.request.COOKIES.get('login_token') != None and CustomUser.objects.filter(token=self.request.COOKIES.get('login_token')).exists():
            user_token = self.request.COOKIES.get('login_token')
            user = get_user_model().objects.get(token=user_token)
            print(user)
            addresses = Address.objects.filter(customer=user)
            return addresses
        
class UserProfileApiViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = CustomUser.objects.all()
    serializer_class = UserProfileSerializer
    def get_queryset(self):
        if self.request.COOKIES.get('login_token') != '' and CustomUser.objects.filter(token=self.request.COOKIES.get('login_token')).exists():
            user_token = self.request.COOKIES.get('login_token')
            user = CustomUser.objects.filter(token=user_token)
        
            return user
    

class UserProfileView(APIView):
    allowed_methods = ['GET', 'PUT']
    def get(self, request):
        if request.COOKIES.get('login_token') != '' and CustomUser.objects.filter(token=request.COOKIES.get('login_token')).exists():
            user_token = request.COOKIES.get('login_token')
            user = get_user_model().objects.get(token=user_token)
            serializer = UserProfileSerializer(user)
            return Response(serializer.data)
    def put(self, request,format=None):
        if request.COOKIES.get('login_token') != '' and CustomUser.objects.filter(token=request.COOKIES.get('login_token')).exists():
            user_token = request.COOKIES.get('login_token')
            user = get_user_model().objects.get(token=user_token)
            serializer = UserProfileSerializer(user, data = request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout(request):
    sessions = Session.objects.all()
    print("sessions: ",sessions)
    for session in sessions:
        print(session)
        session.delete()
    user_token = request.COOKIES.get('login_token')
    user = get_user_model().objects.get(token=user_token)
    response = Response({"message": "Logged out successfully."})
    response.delete_cookie('login_token')
    response.delete_cookie('user_id')
    user.token = None
    user.is_active = False
    user.save()
    return response

class UserInfoAPIView(APIView):
    def get(self, request, *args, **kwargs):
        user_token = request.COOKIES.get('login_token')
        if user_token:
            try:
                user = get_user_model().objects.get(token=user_token)
                serializer = UserProfileSerializer(user)
                return Response(serializer.data)
            
            except get_user_model().DoesNotExist:
                pass
        return Response({'error': 'User not found'}, status=404)
