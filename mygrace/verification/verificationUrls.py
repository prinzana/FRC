from django.urls import path
from .verificationViews import (
    SubmitVerificationRequest,
    VerificationRequestList,
    VerifyUser,
    RejectUser,
    get_verified_users,
    get_rejected_users,
    UnverifyUser,
    RequestReverification  # Import the new view for re-verification
)
# mygrace/verification/urls.py

from django.urls import path
from . import verificationViews

urlpatterns = [
    path('submit-request/', verificationViews.SubmitVerificationRequest.as_view(), name='submit_verification_request'),
    path('pending-requests/', verificationViews.VerificationRequestList.as_view(), name='pending_requests'),
    path('verify/<int:pk>/', verificationViews.VerifyUser.as_view(), name='verify_user'),
    path('unverify/<int:user_id>/', verificationViews.UnverifyUser.as_view(), name='unverify_user'),
    path('reject/<int:pk>/', verificationViews.RejectUser.as_view(), name='reject_user'),
    path('verified/', verificationViews.get_verified_users, name='verified_users'),      # Endpoint for verified users
    path('rejected/', verificationViews.get_rejected_users, name='rejected_users'),      # Endpoint for rejected users
    path('verification/<int:user_id>/request-reverify/', verificationViews.RequestReverification.as_view(), name='request_reverify'),
]
