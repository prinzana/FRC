import json
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from django.contrib.auth import get_user_model
from .profileSerializers import UserProfileSerializer
from rest_framework.response import Response
from django.db.models import Q
from mygrace.models import ActivityLog
import logging
from mygrace.models import MyGraceUser, FaceDescriptor

logger = logging.getLogger(__name__)


User = get_user_model()



class ProfileUpdateView(generics.UpdateAPIView):
    queryset = MyGraceUser.objects.all()
    serializer_class = UserProfileSerializer

    def perform_update(self, serializer):
        update_data = {}

        # Optional profile picture update
        profile_picture = self.request.FILES.get('profile_picture', None)
        if profile_picture:
            update_data['profile_picture'] = profile_picture
            logger.info(f"Profile picture updated for user {self.request.data.get('userId')}.")

        # Optional public_visibility update
        public_visibility = self.request.data.get('public_visibility', None)
        if public_visibility is not None:
            update_data['public_visibility'] = public_visibility
            logger.info(f"Public visibility set to {public_visibility} for user {self.request.data.get('userId')}.")

        # Save the user profile updates
        updated_user = serializer.save(**update_data)

        # Handle face_descriptor (optional)
        face_descriptor_data = self.request.data.get('face_descriptor', None)
        face_descriptor_status = "not updated"

        if face_descriptor_data:
            # Process face descriptor if provided
            if isinstance(face_descriptor_data, str):
                try:
                    face_descriptor_data = json.loads(face_descriptor_data)
                except json.JSONDecodeError as e:
                    logger.error(f"Failed to decode face descriptor: {e}")
                    face_descriptor_data = None

            if isinstance(face_descriptor_data, list) and all(isinstance(i, float) for i in face_descriptor_data):
                face_descriptor, created = FaceDescriptor.objects.get_or_create(user=updated_user)
                face_descriptor.face_descriptor = face_descriptor_data
                face_descriptor.save()
                face_descriptor_status = "created" if created else "updated"

        # Log the activity
        activity_details = f"Profile updated with fields: {', '.join(update_data.keys())}, Face Descriptor: {face_descriptor_status}"
        logger.info(activity_details)

        # Create Activity Log
        ActivityLog.objects.create(
            user=updated_user,
            action='profile_update',
            details=activity_details
        )












# View to list all profiles with search functionality
class ProfileListView(generics.ListAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        # Only return profiles where public_visibility is True
        queryset = User.objects.filter(public_visibility=True)
        query = self.request.query_params.get('query', None)

        if query:
            # Log the search activity if there's a query
            if self.request.user.is_authenticated:
                ActivityLog.objects.create(
                    user=self.request.user,
                    action='profile_search',
                    details=f"Search query: '{query}'"
                )

            queryset = queryset.filter(
                Q(fullname__icontains=query) |
                Q(email__icontains=query) |
                Q(occupation__icontains=query)
            )
        return queryset







# View to get the current user's profile
class CurrentUserProfileView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

    def get(self, request, *args, **kwargs):
        user = self.get_object()
        serializer = UserProfileSerializer(user)
        return Response(serializer.data, status=200)


# View to get a specific user's profile
class ProfileDetailView(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request, *args, **kwargs):
        # Fetch the profile being accessed
        profile = self.get_object()

        # Log the activity (profile view)
        if request.user.is_authenticated:
            ActivityLog.objects.create(
                user=request.user,
                action='profile_view',
                details=f"Profile viewed by user: {request.user.username}"
            )

        # Serialize and return the profile data
        serializer = self.get_serializer(profile)
        return Response(serializer.data, status=200)
    




from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django.db.models import Count

class ResidentsByLGAView(APIView):
    """
    API to filter residents by LGA and occupation details.
    """




from rest_framework import status
from mygrace.models import MyGraceUser  # Correct model import from mygrace/models.py
from .profileSerializers import MyGraceUserSerializer  # Correct serializer import


class ResidentsByLGAView(APIView):
    """
    API to filter residents by LGA and occupation details.
    """

    def get(self, request, *args, **kwargs):
        # Fetch query parameters
        lga = request.query_params.get('lga', None)
        occupation = request.query_params.get('occupation', None)
        is_student = request.query_params.get('is_student', None)
        is_unemployed = request.query_params.get('is_unemployed', None)

        # Build the query filters
        filters = {}
        if lga:
            filters['lga_of_residence'] = lga
        if occupation:
            filters['occupation'] = occupation
        if is_student:
            filters['is_student'] = True if is_student.lower() == 'true' else False
        if is_unemployed:
            filters['is_unemployed'] = True if is_unemployed.lower() == 'true' else False

        # Query the database for users (Residents)
        residents_query = MyGraceUser.objects.filter(**filters)

        # Serialize the result
        serializer = MyGraceUserSerializer(residents_query, many=True)

        # Return the data as JSON
        return Response({'data': serializer.data}, status=status.HTTP_200_OK)
    
class ResidentsByLGAView(APIView):
    """
    API to filter and aggregate residents by LGA, community, occupation, and sex details.
    """

    def get(self, request, *args, **kwargs):
        # Fetch query parameters
        lga = request.query_params.get('lga', None)
        occupation = request.query_params.get('occupation', None)
        community = request.query_params.get('community', None)
        sex = request.query_params.get('sex', None)
        is_student = request.query_params.get('is_student', None)
        is_unemployed = request.query_params.get('is_unemployed', None)

        # Build the query filters using Q objects for flexibility
        query = Q()
        if lga:
            query &= Q(lga_of_residence__iexact=lga)  # Case-insensitive exact match
        if occupation:
            query &= Q(occupation__iexact=occupation)  # Case-insensitive exact match
        if community:
            query &= Q(community__icontains=community)  # Case-insensitive partial match
        if sex:
            query &= Q(sex__iexact=sex)  # Case-insensitive exact match for sex
        if is_student:
            query &= Q(is_student=is_student.lower() == 'true')
        if is_unemployed:
            query &= Q(is_unemployed=is_unemployed.lower() == 'true')

        # Query and aggregate data grouped by LGA
        residents_query = (
            MyGraceUser.objects.filter(query)
            .values('lga_of_residence')  # Group by LGA
            .annotate(count=Count('id'))
            .order_by('lga_of_residence')
        )

        # Check if data exists
        if not residents_query:
            return Response(
                {'data': [], 'message': 'No residents found for the specified filters.'},
                status=status.HTTP_200_OK,
            )

        # Prepare data for the response
        response_data = [{'lga_of_residence': item['lga_of_residence'], 'count': item['count']} for item in residents_query]

        return Response({'data': response_data}, status=status.HTTP_200_OK)
    





from rest_framework.decorators import api_view
from mygrace .models import FaceDescriptor  # Correct import path for FaceDescriptor
from mygrace.profiles.profileSerializers import UserProfileSerializer 
from mygrace import FaceSerializer
from rest_framework.response import Response
from rest_framework import status
from mygrace.models import MyGraceUser  # Ensure MyGraceUser is imported

@api_view(['PUT'])
def update_user_profile(request, user_id):
    try:
        user = MyGraceUser.objects.get(id=user_id)
    except MyGraceUser.DoesNotExist:
        return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'PUT':
        # Handle user profile update
        user_serializer = UserProfileSerializer(user, data=request.data, partial=True)
        if user_serializer.is_valid():
            user_serializer.save()
        else:
            return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # Handle face descriptor update (if it exists in the request)
        if 'face_descriptor' in request.data:
            face_data = request.data.get('face_descriptor')
            face_descriptor_instance, created = FaceDescriptor.objects.get_or_create(user=user)
            face_descriptor_serializer = FaceSerializer(face_descriptor_instance, data={'face_descriptor': face_data}, partial=True)

            if face_descriptor_serializer.is_valid():
                face_descriptor_serializer.save()
            else:
                return Response(face_descriptor_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response(user_serializer.data)

