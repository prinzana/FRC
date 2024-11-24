from rest_framework import serializers
from django.contrib.auth import get_user_model
from mygrace.FaceSerializer import FaceDescriptorSerializer  # Import your serializer

User = get_user_model()
class UserProfileSerializer(serializers.ModelSerializer):
    #userId = serializers.IntegerField(source='id', read_only=True)
    #face_descriptor = FaceDescriptorSerializer(required=False, read_only=True)
    profile_picture = serializers.ImageField(required=False, allow_null=True)

    class Meta:
        model = User
        fields = [
             'fullname', 'email', 'community', 'clan',
            'family_name', 'state_of_residence', 'lga_of_residence',
            'state_of_origin', 'lga_of_origin', 'sex', 'occupation',
            'address', 'profile_picture', 'is_verified',
        ]
        read_only_fields = ['email']

    def update(self, instance, validated_data):
        # Check if profile_picture is in the data
        profile_picture = validated_data.pop('profile_picture', None)
        if profile_picture:
            instance.profile_picture = profile_picture

        # Update other fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance


        

from rest_framework import serializers











class ResidentByLGADataSerializer(serializers.Serializer):
    lga_of_residence = serializers.CharField(max_length=100)
    occupation = serializers.CharField(max_length=100)
    community = serializers.CharField(max_length=100)
    is_student = serializers.BooleanField()
    is_unemployed = serializers.BooleanField()
    count = serializers.IntegerField()

# You may already have a profile serializer like this
class ProfileSerializer(serializers.ModelSerializer):
    # Add relevant fields for the profile serialization
    # This is just an example assuming you have a User model with specific fields
    class Meta:
        model = User  # assuming your model is User or something else
       
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'occupation', 'community', 'lga_of_residence']



from rest_framework import serializers
from mygrace.models import MyGraceUser  # Correct import from mygrace/models.py

class MyGraceUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyGraceUser  # Correct model reference
        fields = '__all__'  # Or list the fields you want to expose
