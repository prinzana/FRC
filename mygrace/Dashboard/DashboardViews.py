from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import status
from django.utils import timezone
from datetime import timedelta
from django.db.models import Q
from mygrace.models import MyGraceUser

class DashboardStatsView(APIView):
    permission_classes = [AllowAny]  # Allow public access for stats

    def get(self, request):
        # Count all users
        total_users = MyGraceUser.objects.count()

        # Count male and female users with case-insensitive filtering
        male_users = MyGraceUser.objects.filter(sex__iexact='male').count()
        female_users = MyGraceUser.objects.filter(sex__iexact='female').count()

        # Count users with unspecified or unknown gender
        unknown_gender_users = MyGraceUser.objects.filter(
            Q(sex__isnull=True) | Q(sex__iexact='') | 
            ~Q(sex__iexact='male') & ~Q(sex__iexact='female')
        ).count()

        # Count verified users
        verified_users = MyGraceUser.objects.filter(is_verified=True).count()

        # New registrations in the last 30 days
        new_registrations = MyGraceUser.objects.filter(
            created_at__gte=timezone.now() - timedelta(days=30)
        ).count()

        # Count pending verification users (those who are not verified)
        pending_verifications = MyGraceUser.objects.filter(is_verified=False).count()

        # Package the stats
        data = {
            'total_users': total_users,
            'male_users': male_users,
            'female_users': female_users,
            'verified_users': verified_users,
            'new_registrations': new_registrations,
            'unknown_gender_users': unknown_gender_users,
            'pending_verifications': pending_verifications,  # Added Pending Verifications
        }

        # Return stats as a response
        return Response(data, status=status.HTTP_200_OK)




from rest_framework.pagination import PageNumberPagination
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from mygrace.models import ActivityLog
from .DashboardSerializer import ActivityLogSerializer

class RecentActivitiesPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

class RecentActivitiesView(APIView):
    def get(self, request):
        recent_activities = ActivityLog.objects.order_by('-date')
        paginator = RecentActivitiesPagination()
        result_page = paginator.paginate_queryset(recent_activities, request)
        serializer = ActivityLogSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from mygrace.models import MyGraceUser, Verification
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from mygrace.models import MyGraceUser, Verification
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from mygrace.models import Verification

class PendingVerificationView(APIView):
    """
    View to list all users with pending verification requests.
    Excludes users who have been rejected.
    """
    def get(self, request):
        try:
            # Fetch verification requests that are pending (not verified and not rejected)
            pending_users = Verification.objects.filter(
                is_verified=False,                # Not verified yet
                rejection_reason__isnull=True,    # No rejection reason
                has_requested_verification=True   # User has actively requested verification
            ).select_related('user')  # Optimize query by including related user data

            # Build a list of pending verifications with relevant user details
            pending_list = [
                {
                    "id": verification.user.id,
                    "name": verification.user.fullname,
                    "email": verification.user.email,
                    "id_type": verification.id_type,
                    "submitted_at": verification.submitted_at,
                }
                for verification in pending_users
            ]

            # Return the pending verifications or a message if no pending requests exist
            if pending_list:
                return Response({"pending_verifications": pending_list}, status=status.HTTP_200_OK)
            else:
                return Response({"message": "No pending verification requests found."}, status=status.HTTP_200_OK)

        except Exception as e:
            # Handle unexpected errors and return an appropriate response
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
