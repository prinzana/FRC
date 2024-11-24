# mygrace/AdminPanel/AdminUrls.py
from django.urls import path
from .AdminViews import NewRegistrationsView, RegisterAdminView, VerifiedUsersView  # Import your view
from django.urls import path
from .AdminViews import (
    RegisterAdminView,
    ListUsersView,
    ToggleUserStatusView,
    DeleteUserView,
    BulkActionsView
)

urlpatterns = [
    path('register-admin/', RegisterAdminView.as_view(), name='register-admin'),
    path('users/', ListUsersView.as_view(), name='list-users'),
    path('users/toggle-status/<int:pk>/', ToggleUserStatusView.as_view(), name='toggle-user-status'),
    path('users/<int:pk>/', DeleteUserView.as_view(), name='delete-user'),
    path('users/bulk-actions/', BulkActionsView.as_view(), name='bulk-actions'),
    path('users/new/', NewRegistrationsView.as_view(), name='new_users'),
    path('users/verified/', VerifiedUsersView.as_view(), name='verified_users'),
]
