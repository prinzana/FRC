# mygrace/urls.py
from django.urls import path, include
from .views import RegisterUserView, LoginUserView, PasswordResetRequestView, PasswordResetConfirmView
from django.views.decorators.csrf import get_token
from django.views.generic import View
from django.http import JsonResponse
from mygrace.profiles.profileViews import ResidentsByLGAView
from django.conf import settings
from django.conf.urls.static import static
from .FaceDetectorViews import CreateFaceDataView, StoreFaceDescriptorView, UpdateFaceDescriptorView, SearchFaceView, GetFaceDataView, ListFaceDataView, DeleteFaceDataView








# Define CSRF Token View
class CsrfTokenView(View):
    def get(self, request, *args, **kwargs):
        return JsonResponse({'csrfToken': get_token(request)})
    




urlpatterns = [
    # Registration, login, and password reset URLs
    path('register/', RegisterUserView.as_view(), name='register'),
    path('login/', LoginUserView.as_view(), name='login'),
    path('password-reset/', PasswordResetRequestView.as_view(), name='password-reset-request'),
    path('password-reset-confirm/<uidb64>/<token>/', PasswordResetConfirmView.as_view(), name='password-reset-confirm'),
    path('api/get-csrf-token/', CsrfTokenView.as_view(), name='get-csrf-token'),
    
    # Include other application-specific URLs here for consistency
    path('verification/', include('mygrace.verification.verificationUrls')),
    path('activity/', include('mygrace.activity.ActivityUrls')),  # Activity URLs
    path('residents-by-lga/', ResidentsByLGAView.as_view(), name='residents_by_lga'),
  
   # Other URLs
    path('create_face_data/', CreateFaceDataView.as_view(), name='create_face_data'),
    path('store_face_descriptor/', StoreFaceDescriptorView.as_view(), name='store_face_descriptor'),
    
    # Ensure the user ID is included in the URL pattern for updating the face descriptor
    path('update_face_descriptor/<int:user_id>/', UpdateFaceDescriptorView.as_view(), name='update_face_descriptor'),
    
    path('search_face/', SearchFaceView.as_view(), name='search_face'),
    path('get_face_data/', GetFaceDataView.as_view(), name='get_face_data'),
    path('list_face_data/', ListFaceDataView.as_view(), name='list_face_data'),
    path('delete_face_data/<int:user_id>/', DeleteFaceDataView.as_view(), name='delete_face_data'),
]


















    # Path for ResidentsByLGAView




if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
