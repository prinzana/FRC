from rest_framework.permissions import AllowAny
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import RegisterSerializer
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import AccessToken
from .models import ActivityLog  # Import the ActivityLog model



from django.core.mail import send_mail#password
from django.utils.http import urlsafe_base64_encode#password
from django.utils.encoding import force_bytes#password
from django.contrib.auth.tokens import PasswordResetTokenGenerator#password
from .models import MyGraceUser  # password
from django.urls import reverse #passowrd

from django.views.decorators.csrf import csrf_exempt
from .serializers import PasswordResetRequestSerializer
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth import get_user_model


from django.http import JsonResponse
from django.middleware.csrf import get_token

def get_csrf_token(request):
    return JsonResponse({'csrfToken': get_token(request)})



# views.py
from django.http import HttpResponse

def homepage(request):
    return HttpResponse("<h1>Welcome Home</h1>")







class RegisterUserView(APIView):
    permission_classes = [AllowAny]  # Allow any user to access this view

    def post(self, request, *args, **kwargs):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()

            # Log the registration action in the ActivityLog model
            ActivityLog.objects.create(user=user, action='REGISTER')

            return Response({'message': 'User created successfully!'}, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Login View------------------------------------------------------------------------------------------------------------
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import AccessToken
from .models import ActivityLog  # Import the ActivityLog model

class LoginUserView(APIView):
    permission_classes = [AllowAny]  # Allow any user to access this view

    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')

        # Debugging statements
        print(f"Attempting to authenticate user: {username}")

        # Authenticate the user
        user = authenticate(username=username, password=password)

        if user is not None:
            print(f"User {username} authenticated successfully.")
            # Generate a token
            token = AccessToken.for_user(user)

            # Log the login action in the ActivityLog model
            ActivityLog.objects.create(user=user, action='LOGIN')

            return Response({
                'message': 'Login successful!',
                'username': user.username,
                'user_id': user.id,  # Include the user ID in the response
                'access_token': str(token)  # Include the access token in the response
            }, status=status.HTTP_200_OK)

        print(f"Authentication failed for user: {username}")
        return Response({'error': 'Invalid Credentials'}, status=status.HTTP_401_UNAUTHORIZED)






#Password reset----------------------------------------------------------------------------------------------

from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
# Import necessary modules
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_str
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.urls import reverse
from django.utils.encoding import force_bytes
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_str, force_bytes
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.urls import reverse

# Import your serializers
from .serializers import PasswordResetRequestSerializer, PasswordResetConfirmSerializer

MyGraceUser = get_user_model()

@method_decorator(csrf_exempt, name='dispatch')
class PasswordResetRequestView(APIView):
    permission_classes = [AllowAny]  # Allows non-authenticated users
    def post(self, request, *args, **kwargs):
        serializer = PasswordResetRequestSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            try:
                user = MyGraceUser.objects.get(email=email)
                token_generator = PasswordResetTokenGenerator()
                token = token_generator.make_token(user)
                uid = urlsafe_base64_encode(force_bytes(user.pk))
                reset_link = request.build_absolute_uri(
                    reverse('password-reset-confirm', kwargs={'uidb64': uid, 'token': token})
                )
                send_mail(
                    subject="Password Reset Request",
                    message=f"Click the link below to reset your password:\n{reset_link}",
                    from_email="noreply@pzana.fred@gmail.com",  # Verify this email
                    recipient_list=[email],
                )
                return Response({"message": "Password reset email has been sent."}, status=status.HTTP_200_OK)
            except MyGraceUser.DoesNotExist:
                return Response({"error": "User with this email does not exist."}, status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@method_decorator(csrf_exempt, name='dispatch')
class PasswordResetConfirmView(APIView):
    permission_classes = [AllowAny]
    def post(self, request, uidb64, token, *args, **kwargs):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = MyGraceUser.objects.get(pk=uid)
            token_generator = PasswordResetTokenGenerator()
            if not token_generator.check_token(user, token):
                return Response({"error": "Invalid or expired token."}, status=status.HTTP_400_BAD_REQUEST)
            serializer = PasswordResetConfirmSerializer(data=request.data)
            if serializer.is_valid():
                user.set_password(serializer.validated_data['new_password'])
                user.save()
                return Response({"message": "Password has been reset successfully."}, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except MyGraceUser.DoesNotExist:
            return Response({"error": "User does not exist."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status.HTTP_500_INTERNAL_SERVER_ERROR)
        

