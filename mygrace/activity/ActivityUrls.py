# mygrace/activity/ActivityUrls.py
from django.urls import path
from . import ActivityViews

urlpatterns = [
    path('', ActivityViews.ActivityLogListView.as_view(), name='activity_log_list'),  # Get all activity logs
    path('user/<int:user_id>/', ActivityViews.ActivityLogUserView.as_view(), name='user_activity_log'),  # Get activity logs by user
    path('admin/', ActivityViews.ActivityLogAdminView.as_view(), name='admin_activity_log'),  # Get all activity logs for admin
    path('monthly/', ActivityViews.MonthlyActivityLogView.as_view(), name='monthly_activity_log'),  # Get monthly activity log
]
