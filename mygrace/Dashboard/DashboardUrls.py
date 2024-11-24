# mygrace/Dashboard/DashboardUrls.py
from django.urls import path
from .DashboardViews import DashboardStatsView, RecentActivitiesView, PendingVerificationView

urlpatterns = [
    path('stats/', DashboardStatsView.as_view(), name='dashboard_stats'),
    path('recent-activities/', RecentActivitiesView.as_view(), name='recent_activities'),
    path('pending-verifications/', PendingVerificationView.as_view(), name='pending_verifications'),
]
