import json
import logging
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from mygrace.models import FaceDescriptor
from mygrace.serializers import FaceDescriptorSerializer

# Set up logger
logger = logging.getLogger(__name__)

class UpdateFaceDescriptorView(APIView):
    permission_classes = [AllowAny]

    def put(self, request, user_id):
        # Get the face descriptor data from the request body
        face_descriptor_data = request.data.get('face_descriptor')

        # Check if the face descriptor is provided
        if not face_descriptor_data:
            logger.error(f"No face descriptor provided for user_id: {user_id}")
            return Response({'error': 'Face descriptor is required.'}, status=400)

        # Ensure the face descriptor is a list of 128 floats
        try:
            logger.debug(f"Received face descriptor data: {face_descriptor_data}")
            face_descriptor_data = json.loads(face_descriptor_data)  # Convert string to list if necessary
            logger.debug(f"Face descriptor data after conversion: {face_descriptor_data}")
        except ValueError:
            logger.error(f"Invalid face descriptor format received for user_id: {user_id}")
            return Response({'error': 'Invalid face descriptor data format.'}, status=400)

        # Check if the descriptor is the right length
        if len(face_descriptor_data) != 128:
            logger.error(f"Face descriptor for user_id: {user_id} does not have 128 values.")
            return Response({'error': 'Face descriptor must be a list of 128 float values.'}, status=400)

        # Retrieve or create FaceDescriptor for the user
        try:
            face_descriptor, created = FaceDescriptor.objects.get_or_create(user_id=user_id)
            
            # Log whether the descriptor was created or updated
            if created:
                logger.info(f"Created new face descriptor for user_id: {user_id}")
            else:
                logger.info(f"Updating existing face descriptor for user_id: {user_id}")

            face_descriptor.face_descriptor = face_descriptor_data  # Update the descriptor
            face_descriptor.save()

            # Log the saved face descriptor
            logger.debug(f"Updated face descriptor for user_id {user_id}: {face_descriptor.face_descriptor}")

            # Serialize the updated face descriptor and return the response
            serialized_data = FaceDescriptorSerializer(face_descriptor)
            logger.info(f"Successfully updated face descriptor for user_id {user_id}")
            return Response(serialized_data.data, status=200)

        except Exception as e:
            logger.error(f"Error updating face descriptor for user_id {user_id}: {str(e)}")
            return Response({'error': str(e)}, status=500)
