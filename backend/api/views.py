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

class Intra42Callback(APIView):
    """
    Handles the callback from Intra42, exchanges the code for tokens,
    and retrieves user info.
    """
    def get(self, request):
        code = request.GET.get('code')
        state = request.GET.get('state')

        # Verify state
        #if state != request.session.get('oauth_state'):
        #    return JsonResponse({"error": "Invalid state"}, status=400)

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
            token_response.raise_for_status()  # Raise exception for invalid responses
            tokens = token_response.json()

            # Fetch user info using access token
            user_info_url = "https://api.intra.42.fr/v2/me"
            user_info_headers = {
                "Authorization": f"Bearer {tokens['access_token']}"
            }
            user_info_response = requests.get(user_info_url, headers=user_info_headers)
            user_info_response.raise_for_status()
            intra42_user = user_info_response.json()

            # Optionally, set the user's name in a cookie and redirect
            response = HttpResponseRedirect("http://localhost")
            response.set_cookie("username", intra42_user.get("login"))

            return response

        except requests.RequestException as err:
            return JsonResponse({"error": str(err)}, status=500)
