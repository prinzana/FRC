# mygrace/activity/ActivitySerializer.py
from rest_framework import serializers
from mygrace.models import ActivityLog

class ActivityLogSerializer(serializers.ModelSerializer):
    # Including the 'fullname' field from the related User model
    fullname = serializers.CharField(source='user.fullname', read_only=True)

    class Meta:
        model = ActivityLog
        fields = ['id', 'action', 'date', 'user_id', 'fullname']  # Include 'fullname'
