# mygrace/AdminPanel/AdminViews.py
from django.views import View
from rest_framework import generics
from .AdminSerializer import MyGraceUserSerializer  # Ensure you create this serializer
from rest_framework.permissions import IsAdminUser
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from mygrace.models import MyGraceUser
from rest_framework.permissions import AllowAny
from django.utils import timezone
from datetime import timedelta
from django.http import JsonResponse



# Fetch the count of newly registered users within a specified timeframe (e.g., last 7 days)
class NewRegistrationsView(View):
    def get(self, request, *args, **kwargs):
        last_week = timezone.now() - timedelta(days=7)  # Adjust the days if necessary
        new_users_count = MyGraceUser.objects.filter(created_at__gte=last_week).count()
        return JsonResponse({'count': new_users_count})

# Fetch the count of verified users
class VerifiedUsersView(View):
    def get(self, request, *args, **kwargs):
        verified_users_count = MyGraceUser.objects.filter(is_verified=True).count()
        return JsonResponse({'count': verified_users_count})




class RegisterAdminView(generics.CreateAPIView):
    serializer_class = MyGraceUserSerializer
  #  permission_classes = [IsAdminUser]   Only allow super admin to access this

    def perform_create(self, serializer):
        serializer.save(is_staff=True, is_superuser=True)  # Automatically set staff and superuser roles

class ListUsersView(generics.ListAPIView):
    queryset = MyGraceUser.objects.all()
    serializer_class = MyGraceUserSerializer
   # permission_classes = [IsAdminUser] Toggle status

class ToggleUserStatusView(generics.UpdateAPIView):
    queryset = MyGraceUser.objects.all()
    serializer_class = MyGraceUserSerializer
    permission_classes = [IsAdminUser]

    def update(self, request, *args, **kwargs):
        user = self.get_object()
        user.is_active = not user.is_active  # Toggle status
        user.save()
        return Response({'status': 'user status toggled'})

class DeleteUserView(generics.DestroyAPIView):
    queryset = MyGraceUser.objects.all()
    serializer_class = MyGraceUserSerializer
    permission_classes = [AllowAny] # Toggle status

class BulkActionsView(generics.GenericAPIView):
    permission_classes = [AllowAny]

    def post(self, request):
        action = request.data.get('action')
        user_ids = request.data.get('user_ids')
        users = MyGraceUser.objects.filter(id__in=user_ids)

        if action == 'delete':
            users.delete()
            return Response({'status': 'users deleted'}, status=status.HTTP_204_NO_CONTENT)
        elif action == 'activate':
            users.update(is_active=True)
            return Response({'status': 'users activated'})
        elif action == 'deactivate':
            users.update(is_active=False)
            return Response({'status': 'users deactivated'})
        else:
            return Response({'error': 'Invalid action'}, status=status.HTTP_400_BAD_REQUEST)
