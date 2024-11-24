from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.conf import settings
from django.conf.urls.static import static
from mygrace.AdminPanel.AdminViews import RegisterAdminView
from mygrace.profiles.profileViews import ResidentsByLGAView
from mygrace.FaceDetectorViews import  UpdateFaceDescriptorView
  # Updated import

urlpatterns = [
    # Admin route
    path('admin/', admin.site.urls),

    # JWT Token Authentication
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # Main application routes
    path('api/mygrace/', include('mygrace.urls')),  # Main app URLs
    path('api/profiles/', include('mygrace.profiles.profileUrls')),  # Profiles-specific routes
    path('api/verification/', include('mygrace.verification.verificationUrls')),  # Verification routes
    path('api/admin/', include('mygrace.AdminPanel.AdminUrls')),  # Admin-related URLs
    path('api/dashboard/', include('mygrace.Dashboard.DashboardUrls')),  # Dashboard routes
    path('api/activity/', include('mygrace.activity.ActivityUrls')),  # Activity log routes
    path('register-admin/', RegisterAdminView.as_view(), name='register_admin'),
    path('residents-by-lga/', ResidentsByLGAView.as_view(), name='residents_by_lga'),
    path('api/', include('mygrace.urls')),
    path('api/update_face_descriptor/<int:user_id>/', UpdateFaceDescriptorView.as_view(), name='update_face_descriptor'),
]

# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
