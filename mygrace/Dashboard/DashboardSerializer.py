
# mygrace/Dashboard/DashboardSerializer.py

# mygrace/Dashboard/DashboardSerializer.py
from rest_framework import serializers
from mygrace .models import ActivityLog,  MyGraceUser # type: ignore
from rest_framework import serializers
from django.contrib.auth.models import User

from rest_framework import serializers
from mygrace.models import MyGraceUser


class ActivityLogSerializer(serializers.ModelSerializer):
    fullname = serializers.SerializerMethodField()

    def get_fullname(self, obj):
        # Ensure that fullname is retrieved from MyGraceUser based on user_id in the activity log
        try:
            user = MyGraceUser.objects.get(id=obj.user_id)
            return user.fullname
        except MyGraceUser.DoesNotExist:
            return "Unknown User"

    class Meta:
        model = ActivityLog
        fields = ['fullname', 'action', 'date']

        
# mygrace/Dashboard/dashboardSerializer.py
from rest_framework import serializers
from mygrace.models import MyGraceUser

class MyGraceUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyGraceUser
        fields = ['id', 'username', 'email', 'fullname', 'is_staff', 'is_active', 'is_verified']
