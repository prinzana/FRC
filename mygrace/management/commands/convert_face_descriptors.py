# myapp/management/commands/convert_face_descriptors.py

from django.core.management.base import BaseCommand
from mygrace.models import FaceDescriptor

class Command(BaseCommand):
    help = 'Convert old face descriptors from dict to list format'

    def handle(self, *args, **kwargs):
        face_descriptors = FaceDescriptor.objects.filter(converted_face_descriptor__isnull=True)

        for face_descriptor in face_descriptors:
            # If the face_descriptor is a dictionary, convert it to a list
            if isinstance(face_descriptor.face_descriptor, dict):
                face_descriptor.converted_face_descriptor = face_descriptor.convert_face_descriptor_to_list()
                face_descriptor.save()
                self.stdout.write(self.style.SUCCESS(f'Converted face descriptor for {face_descriptor.user.username}'))
