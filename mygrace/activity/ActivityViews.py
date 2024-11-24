# mygrace/activity/ActivityViews.py
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from mygrace.models import ActivityLog
from .ActivitySerializer import ActivityLogSerializer
from rest_framework.permissions import IsAuthenticated
from django.db.models import Count
from django.utils import timezone

# mygrace/activity/views.py
from mygrace.activity.ActivitySerializer import ActivityLogSerializer

class ActivityLogListView(generics.ListAPIView):
    queryset = ActivityLog.objects.all()
    serializer_class = ActivityLogSerializer




class ActivityLogUserView(generics.ListAPIView):
    serializer_class = ActivityLogSerializer

    def get_queryset(self):
        user_id = self.kwargs['user_id']
        return ActivityLog.objects.filter(user_id=user_id)

class ActivityLogAdminView(generics.ListAPIView):
    serializer_class = ActivityLogSerializer

    def get_queryset(self):
        return ActivityLog.objects.all()  # Admin can view all logs or filter as needed


class MonthlyActivityLogView(APIView):
    def get(self, request):
        # Get the first and last day of the current month
        today = timezone.now()
        first_day_of_month = today.replace(day=1)
        last_day_of_month = today.replace(day=28) + timezone.timedelta(days=4)  # A little trick to ensure we get the last day
        last_day_of_month = last_day_of_month - timezone.timedelta(days=last_day_of_month.day)

        # Filter activities within the current month
        activities = ActivityLog.objects.filter(date__range=[first_day_of_month, last_day_of_month])

        # Aggregate activity counts for each action type
        activity_counts = activities.values('action').annotate(count=Count('action')).order_by('action')

        # Prepare response data
        result = {}
        for activity in activity_counts:
            result[activity['action']] = activity['count']

        return Response(result)
