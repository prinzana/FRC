from django.utils import timezone
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from mygrace.models import Verification, MyGraceUser, ActivityLog
from .verificationSerializer import VerificationRequestSerializer, MyGraceUserSerializer
from rest_framework.permissions import IsAuthenticated, IsAdminUser  # Add permission for authentication

#----------------------------------------------------------------------------------------------------------------------------


# mygrace/views/verification.py
class SubmitVerificationRequest(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        # Check if the user is already verified
        if request.user.is_verified:
            return Response(
                {"message": "You are a verified user, request declined."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Handle previously rejected requests
        rejected_request = Verification.objects.filter(
            user=request.user,
            rejection_reason__isnull=False,  # Request was rejected
            is_verified=False                # Not verified
        ).exists()

        if rejected_request:
            # Delete the rejected request
            Verification.objects.filter(user=request.user).delete()

        # Check if the user has already submitted a verification request
        existing_request = Verification.objects.filter(user=request.user, is_verified=False).exists()
        if existing_request:
            return Response(
                {"message": "Verification request already submitted."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Create new verification request
        serializer = VerificationRequestSerializer(data=request.data)
        if serializer.is_valid():
            verification_instance = serializer.save(user=request.user)

            # Update the `has_requested_verification` field
            verification_instance.has_requested_verification = True
            verification_instance.submitted_at = timezone.now()
            verification_instance.save()

            # Log the verification request submission
            ActivityLog.objects.create(
                user=request.user,
                action='verification_request_submitted',
                details=f"Verification request submitted for user: {request.user.username}"
            )

            return Response(
                {
                    'message': 'Verification request submitted successfully.',
                    'request_id': verification_instance.id
                },
                status=status.HTTP_201_CREATED
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



















# mygrace/verification/verificationViews.py

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from mygrace.models import Verification


class VerificationRequestList(APIView):
    """
    View to list all verification requests that are pending.
    """
    def get(self, request):
        try:
            # Fetch pending verification requests (not verified and not rejected)
            pending_verifications = Verification.objects.filter(
                is_verified=False,                # Not yet verified
                rejection_reason__isnull=True,    # No rejection provided
                has_requested_verification=True   # User has requested verification
            ).select_related('user')  # Optimize query by including related user data

            # Serialize the data
            serializer = VerificationRequestSerializer(pending_verifications, many=True)

            # Check if there are any pending verifications
            if serializer.data:
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response({"message": "No pending verification requests found."}, status=status.HTTP_200_OK)

        except Exception as e:
            # Handle unexpected errors
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)













class VerifyUser(APIView):
    def put(self, request, pk):
        try:
            verification = Verification.objects.get(pk=pk)

            # Ensure only one verification record exists for this user
            if Verification.objects.filter(user=verification.user).count() > 1:
                return Response({"error": "Multiple verification records found for this user."}, status=status.HTTP_400_BAD_REQUEST)

            verification.is_verified = True
            verification.verified_at = timezone.now()
            verification.has_requested_verification = False  # Reset this field after verification
            verification.save()

            verification.user.is_verified = True
            verification.user.save()

            if request.user.is_authenticated:
                ActivityLog.objects.create(
                    user=request.user,
                    action='user_verified',
                    details=f"User {verification.user.username} verified."
                )

            return Response({"message": "User verified successfully."}, status=status.HTTP_200_OK)
        except Verification.DoesNotExist:
            return Response({"error": "Verification request not found."}, status=status.HTTP_404_NOT_FOUND)










       

class RejectUser(APIView):
    def put(self, request, pk):
        try:
            verification = Verification.objects.get(pk=pk)
            rejection_reason = request.data.get('reason')

            if not rejection_reason:
                return Response({"error": "Rejection reason is required."}, status=status.HTTP_400_BAD_REQUEST)

            # Ensure only one verification record exists for this user
            if Verification.objects.filter(user=verification.user).count() > 1:
                return Response({"error": "Multiple verification records found for this user."}, status=status.HTTP_400_BAD_REQUEST)

            verification.is_verified = False
            verification.rejection_reason = rejection_reason
            verification.save()

            if request.user.is_authenticated:
                ActivityLog.objects.create(
                    user=request.user,
                    action='user_rejected',
                    details=f"User {verification.user.username} verification rejected. Reason: {rejection_reason}"
                )

            return Response(
                {
                    "message": "User verification rejected.",
                    "reason": rejection_reason
                },
                status=status.HTTP_200_OK
            )
        except Verification.DoesNotExist:
            return Response({"error": "Verification request not found."}, status=status.HTTP_404_NOT_FOUND)


#-----------------------------------------UNVERIFY---------------------------------------------------------------------------
class UnverifyUser(APIView):
    def put(self, request, user_id):
        try:
            # Fetch the unique verification record for the user
            verification = Verification.objects.get(user__id=user_id)

            # Check if there is more than one verification
            if Verification.objects.filter(user__id=user_id).count() > 1:
                return Response({"error": "Multiple verification records found for this user."}, status=status.HTTP_400_BAD_REQUEST)

            # Update verification status
            verification.is_verified = False
            verification.verified_at = None
            verification.save()

            # Update the user's is_verified field
            verification.user.is_verified = False
            verification.user.save()

            # Log the activity
            if request.user.is_authenticated:
                ActivityLog.objects.create(
                    user=request.user,
                    action='user_unverified',
                    details=f"User {verification.user.username} unverification performed."
                )

            return Response({"message": "User unverified successfully."}, status=status.HTTP_200_OK)

        except Verification.DoesNotExist:
            return Response({"error": "Verification record not found."}, status=status.HTTP_404_NOT_FOUND)
        

#----------------------------------------ReVERIFICATION-------------------------------------------------------       
class RequestReverification(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, user_id):
        try:
            user = MyGraceUser.objects.get(id=user_id)
            verification = Verification.objects.filter(user=user).last()

            # Ensure the user is already verified
            if not verification or not verification.is_verified:
                return Response({"error": "User is not verified."}, status=status.HTTP_400_BAD_REQUEST)

            # 1. Only check for changes after verification
            original_full_name = verification.full_name
            original_address = verification.address
            original_profile_picture = verification.profile_picture

            updated_fields = request.data.get('updated_fields', [])
            
            # Ensure the user is trying to update one of the required fields: fullname, address, or profile_picture
            changes_detected = False

            if 'fullname' in updated_fields and user.full_name != original_full_name:
                changes_detected = True
            if 'address' in updated_fields and user.address != original_address:
                changes_detected = True
            if 'profile_picture' in updated_fields and user.profile_picture != original_profile_picture:
                changes_detected = True

            # Trigger re-verification if there are changes in any of the critical fields
            if changes_detected:
                # Mark user as unverified
                verification.is_verified = False
                verification.verified_at = None  # Clear the verification timestamp
                verification.save()

                user.is_verified = False
                user.save()

                # Log the reverification activity
                ActivityLog.objects.create(
                    user=request.user,
                    action='user_reverification_requested',
                    details=f"Re-verification triggered for user: {user.username} due to profile update."
                )

                return Response({"message": "Re-verification triggered due to profile updates."}, status=status.HTTP_200_OK)

            return Response({"message": "No significant changes detected."}, status=status.HTTP_200_OK)

        except MyGraceUser.DoesNotExist:
            return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)

#--------------------------------GET---------------------------------------------------------------
@api_view(['GET'])
def get_verified_users(request):
    # Get verified users
    verified_users = MyGraceUser.objects.filter(verification__is_verified=True)
    serializer = MyGraceUserSerializer(verified_users, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def get_rejected_users(request):
    # Get rejected users based on rejection reasons
    rejected_verifications = Verification.objects.filter(is_verified=False, rejection_reason__isnull=False)
    rejected_users = MyGraceUser.objects.filter(verification__in=rejected_verifications)
    serializer = MyGraceUserSerializer(rejected_users, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)
