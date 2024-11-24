from django.urls import path
from .profileViews import ProfileListView, ProfileDetailView, ProfileUpdateView,  CurrentUserProfileView # Import your views
from .profileViews import ResidentsByLGAView 

urlpatterns = [
    path('', ProfileListView.as_view(), name='profile-list'),  # Get all profiles, now at /api/profiles/
    path('<int:pk>/', ProfileDetailView.as_view(), name='profile-detail'),  # Get a specific profile, now at /api/profiles/<pk>/
    path('update/<int:pk>/', ProfileUpdateView.as_view(), name='profile-update'),  # Update a profile, now at /api/profiles/update/<pk>/
    path('me/', CurrentUserProfileView.as_view(), name='current-user-profile'),  # Current user profile, now at /api/profiles/me/
    path('residents-by-lga/', ResidentsByLGAView.as_view(), name='residents-by-lga'),
]
