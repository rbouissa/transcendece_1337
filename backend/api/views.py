from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt
from rest_framework.permissions import AllowAny
from django.contrib.auth import authenticate
from rest_framework.exceptions import AuthenticationFailed
import jwt
import datetime
from django.conf import settings
from rest_framework_simplejwt.tokens import RefreshToken


from rest_framework.permissions import IsAuthenticated
class SampleAPI(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        data = {'message': 'Hello from Django backend'}
        return Response(data, status=status.HTTP_200_OK)
    def post(self,request):
        data = {'message': 'Hello from Django backend'}
        return Response(data, status=status.HTTP_200_OK)

class Signup(APIView):
    permission_classes = [AllowAny]  # To allow any user to access this view
    
    @csrf_exempt  # Disables CSRF validation for this method
    def post(self, request):
        data = request.data  # Using DRF's `request.data` instead of parsing manually
        
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')

        if User.objects.filter(username=username).exists():
            return Response({'error': 'Username already taken'}, status=status.HTTP_400_BAD_REQUEST)

        # Create user with hashed password using create_user
        user = User.objects.create_user(username=username, email=email, password=password)
        return Response({'message': 'User created successfully'}, status=status.HTTP_201_CREATED)

    # If you want to handle GET requests, you can define it here as well
    def get(self, request):
        return Response({'message': 'This is the signup page'}, status=status.HTTP_200_OK)


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from django.conf import settings
import jwt
import datetime

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
import time
class Login(APIView):
    permission_classes = [AllowAny]
    time.sleep(5)
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        # Authenticate the user
        user = authenticate(request, username=username, password=password)

        if user is not None:
            # Generate token payload
            payload = {
                'username': user.username,
                'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
                'iat': datetime.datetime.utcnow(),
            }
            # Encode the JWT token
            token = jwt.encode(
                payload, 
                'django-insecure-1a2b3c4d5e6f7g8h9i0j1k2l3m4n5o6p7q8r9s0t1u2v3w4x5y6z7a8b9c0d1e2f3', 
                algorithm='HS256'
            )

            # Respond with the token and other data
            return Response({
                'jwt': token,
                'message': 'Login successful',
                'redirect_url': 'http://localhost:8080/index'  # Replace with your actual URL
            }, status=status.HTTP_200_OK)

        # If authentication fails
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)

            
from django.conf import settings
from django.http import JsonResponse
from rest_framework.views import APIView
import uuid
from django.http import HttpResponseRedirect

class loginwith42(APIView):
    permission_classes = [AllowAny]
    """
    Generates the Intra42 OAuth URL and sends it to the frontend.
    """
    def get(self, request):
        # Step 1: Retrieve Client ID from settings
        client_id = settings.OAUTH_42_CLIENT_ID

        # Step 2: Define the Redirect URI
        redirect_uri = "http://localhost:8000/api/intra42callback/"

        # Step 3: Generate a random state string
        state = str(uuid.uuid4())  # Unique identifier for CSRF protection
        request.session['oauth_state'] = state  # Save state in the session for later validation

        # Step 4: Construct the Intra42 Authorization URL
        auth_url = (
            f"https://api.intra.42.fr/oauth/authorize?"
            f"client_id={client_id}"
            f"&redirect_uri={redirect_uri}"
            f"&response_type=code"
            f"&scope=public"
            f"&state={state}"
        )
        print("Debug: Callback handler reached.\n")
        # Step 5: Return the URL as a JSON response
        return JsonResponse({"url": auth_url})
    
import requests
from django.http import JsonResponse, HttpResponseRedirect
from django.conf import settings
from rest_framework.views import APIView



def fetch_intra42_user_info(access_token):
    url = "https://api.intra.42.fr/v2/me"
    headers = {
        "Authorization": f"Bearer {access_token}",
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()  # User profile data
    else:
        print(f"Error: {response.status_code}, {response.text}")
        return None

import requests
from django.conf import settings
from django.http import JsonResponse
from rest_framework.views import APIView
from .models import Intra42User
from django.shortcuts import render


class Intra42Callback(APIView):
    permission_classes = [AllowAny] 
    print('vvvvvvvvvvvvvvvvvvvvvv\n\n\n\n\n')
    def get(self, request):
        print("Debug: Callback handler reached.")
        code = request.GET.get('code')
        #print("code = |", code, "|")
        try:
            # Exchange the code for tokens
            token_url = "https://api.intra.42.fr/oauth/token"
            token_data = {
                "grant_type": "authorization_code",
                "client_id": settings.OAUTH_42_CLIENT_ID,
                "client_secret": settings.OAUTH_42_CLIENT_SECRET,
                "code": code,
                "redirect_uri": settings.OAUTH_42_REDIRECT_URI,
            }
            token_response = requests.post(token_url, data=token_data)
            token_response.raise_for_status()
            tokens = token_response.json()

            # Fetch user info using access token
            access_token = tokens['access_token']
            user_info_url = "https://api.intra.42.fr/v2/me"
            user_info_headers = {
                "Authorization": f"Bearer {access_token}",
            } 
            user_info_response = requests.get(user_info_url, headers=user_info_headers)
            user_info_response.raise_for_status()
            user_data = user_info_response.json()

            # Save or update user data in the database
            # user, created = Intra42User.objects.update_or_create(
            #     intra_id=user_data['id'],  # Unique Intra42 ID
            #     defaults={
            #         "login": user_data['login'],
            #         "email": user_data['email'],
            #         "first_name": user_data['first_name'],
            #         "last_name": user_data['last_name'],
            #         # #"first_name": user_data.get('first_name', ''),
            #         # "last_name": user_data.get('last_name', ''),
            #         "image":  user_data['image'],
            #         #"kind": user_data['kind'],
            #         #"access_token": access_token,
            #         #"refresh_token": tokens.get('refresh_token', ''),
            #     },
            # )
            user = Intra42User(intra_id=user_data['id'], login=user_data['login'],first_name=user_data['first_name'],last_name=user_data['last_name'],email=user_data['email'],image=user_data['image'])#picture=picture
            user.save()
            refresh = RefreshToken.for_user(user)

            print("User saved:", refresh.access_token)
            print("User saved:", str(refresh))
            responsee = JsonResponse({
            'message': 'Data received successfully',
            'access_token': str(refresh.access_token),
            'refresh_token': str(refresh),
            'url' : "http://localhost:8080/dashboard"
            })

            set_secure_cookie(responsee, {'access': str(refresh.access_token), 'refresh': refresh})
            print('\n\n\n', responsee, '\n\n\n')
            return responsee

        except requests.RequestException as err:
            return JsonResponse({"error": str(err)}, status=500)

def set_secure_cookie(response, param):
    response.set_cookie(
        'access_token',
        str(param['access']),
        secure=True,
        samesite='None'
    )
    response.set_cookie(
        'refresh_token',
        str(param['refresh']),
        httponly=True,
        secure=True,
        samesite='None'
    )
    return response


from rest_framework.exceptions import NotFound

from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

class data_user(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user  # This will be the authenticated Intra42User
        user_data = {
            "login": user.login,
            "email": user.email,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "image": user.image,
        }
        return Response(user_data)

# class Intra42Callback(APIView):
#     permission_classes = [AllowAny] 
    
#     def get(self, request):
#         print("Debug: Callback handler reached.")
#         code = request.GET.get('code')

#         try:
#             # Exchange the code for tokens
#             token_url = "https://api.intra.42.fr/oauth/token"
#             token_data = {
#                 "grant_type": "authorization_code",
#                 "client_id": settings.OAUTH_42_CLIENT_ID,
#                 "client_secret": settings.OAUTH_42_CLIENT_SECRET,
#                 "code": code,
#                 "redirect_uri": settings.OAUTH_42_REDIRECT_URI,
#             }
#             token_response = requests.post(token_url, data=token_data)
#             token_response.raise_for_status()
#             tokens = token_response.json()

#             # Fetch user info using access token
#             access_token = tokens['access_token']
#             user_info_url = "https://api.intra.42.fr/v2/me"
#             user_info_headers = {
#                 "Authorization": f"Bearer {access_token}",
#             }
#             user_info_response = requests.get(user_info_url, headers=user_info_headers)
#             user_info_response.raise_for_status()
#             user_data = user_info_response.json()

#             # Save or update user data in the database
#             user, created = Intra42User.objects.update_or_create(
#                 intra_id=user_data['id'],  # Unique Intra42 ID
#                 defaults={
#                     "login": user_data['login'],
#                     "email": user_data['email'],
#                     "first_name": user_data['first_name'],
#                     "last_name": user_data['last_name'],
#                     "image": user_data['image']['link'],  # Adjusted to match the expected key
#                 },
#             )
#             print("User saved:", user)

#             # Respond with user data
#             response_data = {
#                 "id": user.intra_id,
#                 "login": user.login,
#                 "email": user.email,
#                 "first_name": user.first_name,
#                 "last_name": user.last_name,
#                 "image": user.image,  # Assuming this field is a URL
#             }
#             return Response(response_data, status=status.HTTP_200_OK)

#         except requests.RequestException as err:
#             return Response({"error": str(err)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


