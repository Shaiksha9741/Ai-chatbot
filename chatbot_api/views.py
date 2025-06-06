from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from .models import ChatHistory
import openai
import os

class RegisterView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        email = request.data.get('email')

        if not username or not password or not email:
            return Response({'error': 'All fields are required'}, status=status.HTTP_400_BAD_REQUEST)

        if User.objects.filter(username=username).exists():
            return Response({'error': 'Username already exists'}, status=status.HTTP_400_BAD_REQUEST)

        User.objects.create_user(username=username, password=password, email=email)
        return Response({'message': 'User registered successfully'}, status=status.HTTP_201_CREATED)


class LoginView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        if not username or not password:
            return Response({'error': 'Both username and password are required'}, status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(username=username, password=password)
        if user is None:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

        # Generate a token (you can use Django Rest Framework's TokenAuthentication or JWT)
        # For simplicity, we'll return a dummy token here
        token = "dummy-token-for-testing"
        return Response({'token': token}, status=status.HTTP_200_OK)


class ChatView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user_message = request.data.get('message')
        if not user_message:
            return Response({'error': 'Message is required'}, status=status.HTTP_400_BAD_REQUEST)

        # Use OpenAI API to generate bot response
        openai.api_key = os.getenv('OPENAI_API_KEY')
        try:
            completion = openai.Completion.create(
                engine="text-davinci-003",
                prompt=user_message,
                max_tokens=150
            )
            bot_response = completion.choices[0].text.strip()
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # Save chat history
        ChatHistory.objects.create(
            user=request.user,
            user_message=user_message,
            bot_response=bot_response
        )

        return Response({'bot_response': bot_response}, status=status.HTTP_200_OK)


class ChatHistoryView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        chat_history = ChatHistory.objects.filter(user=request.user).order_by('-timestamp')
        history_data = [
            {
                'user_message': chat.user_message,
                'bot_response': chat.bot_response,
                'timestamp': chat.timestamp
            }
            for chat in chat_history
        ]
        return Response(history_data, status=status.HTTP_200_OK)






# import openai
# from django.conf import settings
# from django.contrib.auth import authenticate
# from rest_framework import status, generics
# from rest_framework.response import Response
# from rest_framework.permissions import IsAuthenticated, AllowAny
# from rest_framework_simplejwt.tokens import RefreshToken
# from .models import ChatHistory
# from .serializers import (
#     UserSerializer, 
#     LoginSerializer, 
#     ChatMessageSerializer, 
#     ChatHistorySerializer
# )

# # Configure OpenAI API key
# openai.api_key = settings.OPENAI_API_KEY

# class RegisterView(generics.CreateAPIView):
#     serializer_class = UserSerializer
#     permission_classes = [AllowAny]

# class LoginView(generics.GenericAPIView):
#     serializer_class = LoginSerializer
#     permission_classes = [AllowAny]

#     def post(self, request):
#         serializer = self.serializer_class(data=request.data)
#         serializer.is_valid(raise_exception=True)
        
#         user = authenticate(
#             username=serializer.validated_data['username'],
#             password=serializer.validated_data['password']
#         )
        
#         if user is not None:
#             refresh = RefreshToken.for_user(user)
#             return Response({
#                 'token': str(refresh.access_token),
#                 'refresh': str(refresh),
#             })
#         return Response(
#             {"error": "Invalid credentials"}, 
#             status=status.HTTP_401_UNAUTHORIZED
#         )

# class ChatView(generics.GenericAPIView):
#     serializer_class = ChatMessageSerializer
#     permission_classes = [IsAuthenticated]

#     def post(self, request):
#         serializer = self.serializer_class(data=request.data)
#         serializer.is_valid(raise_exception=True)
        
#         user_message = serializer.validated_data['message']
        
#         try:
#             # Call OpenAI API
#             response = openai.ChatCompletion.create(
#                 model="gpt-3.5-turbo",
#                 messages=[
#                     {"role": "system", "content": "You are a helpful assistant."},
#                     {"role": "user", "content": user_message}
#                 ]
#             )
            
#             bot_response = response.choices[0].message.content
            
#             # Save to chat history
#             chat_history = ChatHistory.objects.create(
#                 user=request.user,
#                 user_message=user_message,
#                 bot_response=bot_response
#             )
            
#             return Response(ChatHistorySerializer(chat_history).data)
        
#         except Exception as e:
#             return Response(
#                 {"error": str(e)}, 
#                 status=status.HTTP_500_INTERNAL_SERVER_ERROR
#             )

# class ChatHistoryView(generics.ListAPIView):
#     serializer_class = ChatHistorySerializer
#     permission_classes = [IsAuthenticated]
    
#     def get_queryset(self):
#         return ChatHistory.objects.filter(user=self.request.user)
