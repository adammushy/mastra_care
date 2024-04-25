from django.shortcuts import render
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializer import *
from django.contrib.auth import authenticate, login, update_session_auth_hash
from .models import *
from rest_framework.generics import UpdateAPIView
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes

# Create your views here.



class RegisterUser(APIView):
    permission_classes= [AllowAny]
    
    @staticmethod
    def post(request):
        data = request.data
        serializer = UserSerializer(data=data)
        
        if serializer.is_valid():
            email = data['email']
            username =data['username']
            user = User.objects.filter(email=email)
            if user:
                message = {'status':false,'message':'username or email alread exist'}
                return Response(message,status=status.HTTP_400_BAD_REQUEST)
            user2 = serializer.save()
            message ={'save':True}
            return Response(message)
        
        message = {'save':False,'errors':serializer.errors}
        return Response(message)

    @staticmethod
    def get(request):
        users  = User.objects.all()
        return Response(UserSerializer(instance=users, many=True).data)

# {
# "email":"mike@gmail.com",
# "password":"123",
# "username":"mike",
# "phone":"078676726",
# "blood_group":"B+",
# "gender":"MALE",
# "dob":"2000-03-27",
# "profile":null,
# "profile_binary":null,

# }
    
class LoginUser(APIView):
    permission_classes= [AllowAny]
    
    @staticmethod
    def post(request):
        data = request.data
        email = data.get('email')
        password = data.get('password')
        user = authenticate(email=email, password=password)        
        
        if user is not None:
            login(request,user)
            user_id = User.objects.get(email=email)
            user_info = UserSerializer(instance=user_id,many=False).data
            token, create = Token.objects.get_or_create(user=user)
            response = {
                'login': True,
                'token': token.key,
                'user': user_info
            }
            return Response(response)
        else:
            response ={
                'login':False,
                'message':'Invalid username or password'
            }
            return Response(response)
        
        
class UserInformation(APIView):
    @staticmethod
    def get(request,query_type):
        if query_type == 'single':
            try:
                user_id = request.GET.get('user_id')
                user = User.objects.get(id =user_id)
            except User.DoesNotExist:
                return Response({'message':'User doesnot exist'})
            
            response= UserSerializer(instance=user,many=False).data
            return Response(response)
        
        elif query_type=='all':
            queryset= User.objects.all()
            response = UserSerializer(instance=queryset,many=True).data
            
            return Response(response)
        
        else:
            response={'message':'wrong Request!!'}
            
            return Response(response)
        
        
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def change_password(request):
        if request.method =='POST':
            print(request.data)
            serializer = ChangePasswordSerializer(data=request.data)
            if serializer.is_valid():
                user = request.user
                if user.check_password(serializer.data.get('old_password')):
                    user.set_passowrd(serializer.data.get('new_password'))
                    user.save()
                    update_session_auth_hash(request,user)
                    message ={'message': 'Password changed successfully.', 'success': True}
                    return Response(message,status=status.HTTP_200_OK)

                response ={'error': 'Incorrect old password.', 'success': False}
                return Response(response,status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    

class DeleteUser(APIView):
    @staticmethod
    def post(request):
        data = request.data
        try:
            user = User.objects.get(id=data['userId'])
            account.delete()
            return Response({"delete": True})

        except:
            return Response({"delete": False})


# {
#     "userId": "",
# }
            