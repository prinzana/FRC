from rest_framework import serializers
from .models import MyGraceUser

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyGraceUser
        fields = [
            'username', 'email', 'password', 'fullname', 'community', 'clan', 'family_name',
            'state_of_residence', 'lga_of_residence', 'state_of_origin', 'lga_of_origin',
            'sex', 'occupation', 'address'
        ]
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        # Extract only required fields and set defaults for optional ones
        optional_fields = [
            'state_of_residence', 'lga_of_residence', 
            'state_of_origin', 'lga_of_origin', 
            'occupation', 'address'
        ]

        for field in optional_fields:
            validated_data.setdefault(field, None)  # Set default value to None if not provided

        user = MyGraceUser.objects.create_user(
            username=validated_data['username'],  # Include username
            email=validated_data['email'],
            password=validated_data['password'],  # Hashing done by create_user
            fullname=validated_data['fullname'],
            community=validated_data['community'],
            clan=validated_data['clan'],
            family_name=validated_data['family_name'],
            **{field: validated_data[field] for field in optional_fields}  # Unpack optional fields
        )
        
        return user

#Password-----------------------------------------------------------------------------------------------------------------
class PasswordResetRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        """
        Check if a user with this email exists.
        """
        if not MyGraceUser.objects.filter(email=value).exists():
            raise serializers.ValidationError("User with this email does not exist.")
        return value
    
class PasswordResetConfirmSerializer(serializers.Serializer):
    new_password = serializers.CharField(write_only=True, min_length=8, required=True)

    def validate_new_password(self, value):
        # You can add custom password validation rules here
        return value

    