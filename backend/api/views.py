from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

    
from django.contrib.auth.models import User
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt
from rest_framework.permissions import AllowAny
from django.contrib.auth import authenticate
class SampleAPI(APIView):
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


class Login(APIView):
    def post(self, request):
        # Get the username and password from the request body
        username = request.data.get('username')
        password = request.data.get('password')

        # Authenticate the user
        user = authenticate(request, username=username, password=password)

        if user is not None:
            # User is authenticated, respond with success
            return Response({'message': 'Login successful'}, status=status.HTTP_200_OK)
        else:
            # Authentication failed, respond with an error
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)
from django.conf import settings
from django.http import JsonResponse
from rest_framework.views import APIView
import uuid
from django.http import HttpResponseRedirect

class loginwith42(APIView):
    """
    Generates the Intra42 OAuth URL and sends it to the frontend.
    """
    def get(self, request):
        # Step 1: Retrieve Client ID from settings
        client_id = settings.OAUTH_42_CLIENT_ID

        # Step 2: Define the Redirect URI
        redirect_uri = settings.OAUTH_42_REDIRECT_URI

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

# import logging

# # Set up logging (optional but recommended for production)
# logger = logging.getLogger(__name__)

# class Intra42Callback(APIView):
#     def get(self, request):
#         code = request.GET.get('code')
#         state = request.GET.get('state')

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
# #id,email,login,last_name,usual_full_name,url,phone,displayname:reda bouissali
# #kind:student,image:{'link': 'https://cdn.intra.42.fr/users/a3eeff3cb3803a74a575bce46cb21021/rbouissa.JPG', 'versions': {'large': 'https://cdn.intra.42.fr/users/36321d78d5c54ac008580c633a958b92/large_rbouissa.JPG', 'medium': 'https://cdn.intra.42.fr/users/2d908253b509b03c0e33b1c3050e226e/medium_rbouissa.JPG', 'small': 'https://cdn.intra.42.fr/users/54c3150e5b52ef6bf9212d37fdc87313/small_rbouissa.JPG',
# #pool_month,pool_year,Wallet: 145,created_at,updated_at,correction_point
#             # Print user data to console
#             print("Fetched User Data:", user_data)

#             # Alternatively, log the data
#             logger.info("Fetched User Data: %s", user_data)

#             # Save or update user data in the database
#             user, created = Intra42User.objects.update_or_create(
#                 intra_id=user_data['id'],
#                 defaults={
#                     "login": user_data['login'],
#                     "email": user_data['email'],
#                 },
#             )

#             return JsonResponse({"message": "Data fetched and printed successfully"})

#         except requests.RequestException as err:
#             logger.error("Error fetching data: %s", err)
#             return JsonResponse({"error": str(err)}, status=500)



class Intra42Callback(APIView):
    def get(self, request):
        code = request.GET.get('code')

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
            user, created = Intra42User.objects.update_or_create(
                intra_id=user_data['id'],  # Unique Intra42 ID
                defaults={
                    "login": user_data['login'],
                    "email": user_data['email'],
                    "first_name": user_data['first_name'],
                    "last_name": user_data['last_name'],
                    
                    # #"first_name": user_data.get('first_name', ''),
                    # "last_name": user_data.get('last_name', ''),
                    "image":  user_data['image'],
                    #"kind": user_data['kind'],
                    
                    #"access_token": access_token,
                    #"refresh_token": tokens.get('refresh_token', ''),
                    
                },
            )

            # Debug: Print success
            print("User saved:", user)

            return JsonResponse({"message": "User data saved successfully"})

        except requests.RequestException as err:
            return JsonResponse({"error": str(err)}, status=500)
