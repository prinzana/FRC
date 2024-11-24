# verification/verificationSerializer.py
from rest_framework import serializers
from ..models import Verification, MyGraceUser

class MyGraceUserSerializer(serializers.ModelSerializer):
    """
    Serializer for user data to include essential fields from MyGraceUser model.
    """
    class Meta:
        model = MyGraceUser
        fields = ['username', 'email', 'fullname']

class VerificationRequestSerializer(serializers.ModelSerializer):
    user = MyGraceUserSerializer(read_only=True)  # Use nested serializer for user details

    class Meta:
        model = Verification
        fields = ['id', 'user', 'id_type', 'id_number', 'id_document', 'is_verified', 
                  'submitted_at', 'verified_at', 'rejection_reason', 'has_requested_verification']
        
        read_only_fields = ['is_verified', 'submitted_at', 'verified_at', 'rejection_reason', 'has_requested_verification']
