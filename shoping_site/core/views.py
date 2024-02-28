from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.contrib.auth import get_user_model, logout
from rest_framework import status
from .models import CustomUser, Address
from .serializers import UserProfileSerializer, AddressSerializer

class AddressListView(APIView):
    def get(self, request):
        if request.COOKIES.get('login_token') != '' and CustomUser.objects.filter(token=request.COOKIES.get('login_token')).exists():
            user_token = request.COOKIES.get('login_token')
            user = get_user_model().objects.get(token=user_token)
            addresses = Address.objects.filter(customer=user)
            serializer = AddressSerializer(addresses, many=True)
            return Response(serializer.data)


class UserProfileView(APIView):
    def get(self, request):
        if request.COOKIES.get('login_token') != '' and CustomUser.objects.filter(token=request.COOKIES.get('login_token')).exists():
            user_token = request.COOKIES.get('login_token')
            user = get_user_model().objects.get(token=user_token)
            serializer = UserProfileSerializer(user)
            return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout(request):
    user_token = request.COOKIES.get('login_token')
    user = get_user_model().objects.get(token=user_token)
    response = Response({"message": "Logged out successfully."})
    response.delete_cookie('login_token')
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
                data = {
                    'id': user.id,
                    'email': user.email,
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                    'photo': str(user.user_image),
                }
                return Response(data)
            
            except get_user_model().DoesNotExist:
                pass
        return Response({'error': 'User not found'}, status=404)
