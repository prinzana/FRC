# mygrace/AdminPanel/AdminSerializer.py
from rest_framework import serializers
from mygrace.models import MyGraceUser  # Import your user model

class MyGraceUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyGraceUser
        fields = ['username', 'email', 'fullname', 'password']
        extra_kwargs = {'password': {'write_only': True}}  # Ensure password is write-only

    def create(self, validated_data):
        user = MyGraceUser(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user
