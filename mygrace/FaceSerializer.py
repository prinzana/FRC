

from rest_framework import serializers
from .models import FaceDescriptor


class FaceDescriptorSerializer(serializers.ModelSerializer):
    class Meta:
        model = FaceDescriptor
        fields = ['user', 'face_descriptor']




# mygrace/FaceSerializer.py
#from rest_framework import serializers
#from .models import FaceData

#class FaceDataSerializer(serializers.ModelSerializer):
 #   class Meta:
  #      model = FaceData
   #     fields = ['id', 'user', 'profile_picture', 'face_descriptor']
