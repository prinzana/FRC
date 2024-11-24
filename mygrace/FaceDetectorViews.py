import json
import logging
import numpy as np
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .FaceSerializer import FaceDescriptor
from .FaceSerializer import FaceDescriptorSerializer
from .Face_Recognition import extract_face_descriptor
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import IsAdminUser
from .models import FaceData
from mygrace.models import FaceDescriptor
from .profiles.profileSerializers import UserProfileSerializer
from .models import DebugFaceMatch


logger = logging.getLogger(__name__)


from rest_framework.views import APIView



from .Face_Recognition import extract_face_descriptor
import logging

logger = logging.getLogger(__name__)

class CreateFaceDataView(APIView):
    def post(self, request, *args, **kwargs):
        user = request.user
        image_file = request.data.get('image')  # The uploaded image to extract face descriptor from

        if not image_file:
            logger.error("No image file provided.")
            return Response({"error": "No image file provided."}, status=status.HTTP_400_BAD_REQUEST)

        # Extract face descriptor from the image
        face_descriptor = extract_face_descriptor(image_file)

        if not face_descriptor:
            logger.error("No face found in the image.")
            return Response({"error": "No face found in the image."}, status=status.HTTP_400_BAD_REQUEST)

        # Store the face descriptor in the FaceDescriptor model
        face_descriptor_instance, created = FaceDescriptor.objects.get_or_create(user=user)
        face_descriptor_instance.face_descriptor = face_descriptor
        face_descriptor_instance.save()

        # Create a new entry in the FaceRecognitionData model
        face_data = FaceDescriptor.objects.create(
            user=user,
            face_descriptor=face_descriptor,
            uploaded_at=face_descriptor_instance.created_at
        )

        logger.info(f"Face data created for user {user.username}")

        # Serialize the face data and return it
        face_data_serializer = FaceDescriptorSerializer(face_data)
        return Response(face_data_serializer.data, status=status.HTTP_201_CREATED)



class StoreFaceDescriptorView(APIView):
    def post(self, request, *args, **kwargs):
        user = request.user
        image_file = request.data.get('image')  # Assuming the image is passed in the request

        if not image_file:
            logger.error("No image file provided.")
            return Response({"error": "No image file provided."}, status=status.HTTP_400_BAD_REQUEST)

        # Extract face descriptor from the image
        face_descriptor = extract_face_descriptor(image_file)

        if not face_descriptor:
            logger.error("No face found in the image.")
            return Response({"error": "No face found in the image."}, status=status.HTTP_400_BAD_REQUEST)

        # Check if the user already has a face descriptor stored
        face_descriptor_instance, created = FaceDescriptor.objects.get_or_create(user=user)
        face_descriptor_instance.face_descriptor = face_descriptor
        face_descriptor_instance.save()

        logger.info(f"Face descriptor stored for user {user.username}")
        return Response({"message": "Face descriptor stored successfully."}, status=status.HTTP_201_CREATED)

# mygrace/FaceDetectorViews.py
# mygrace/FaceDetectorViews.py


  # Ensure you have the correct serializer
from rest_framework import serializers
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import FaceDescriptor
from rest_framework.permissions import AllowAny
from .FaceSerializer import FaceDescriptorSerializer
import json
class UpdateFaceDescriptorView(APIView):
    permission_classes = [AllowAny]

    def put(self, request, user_id):
        # Retrieve the face descriptor data from the request
        face_descriptor_data = request.data.get('face_descriptor')

        if not face_descriptor_data:
            logger.error(f"No face descriptor provided for user_id: {user_id}")
            return Response({'error': 'Face descriptor is required.'}, status=400)

        # Handle string input for face descriptor (if applicable)
        if isinstance(face_descriptor_data, str):
            try:
                face_descriptor_data = json.loads(face_descriptor_data)
                logger.debug(f"Converted face descriptor string to list: {face_descriptor_data}")
            except json.JSONDecodeError:
                logger.error(f"Failed to decode face descriptor string for user_id: {user_id}")
                return Response({'error': 'Invalid face descriptor format.'}, status=400)

        # Handle dictionary input by converting to a float list
        if isinstance(face_descriptor_data, dict):
            try:
                face_descriptor_data = [float(value) for value in face_descriptor_data.values()]
            except ValueError:
                logger.error(f"Failed to convert dictionary to float list for user_id: {user_id}")
                return Response({'error': 'Face descriptor must be a list of 128 float values.'}, status=400)

        # Validate the face descriptor size
        try:
            numpy_face_descriptor = np.array(face_descriptor_data, dtype=np.float32)
            if numpy_face_descriptor.shape[0] != 128:
                logger.error(f"Invalid face descriptor size for user_id: {user_id}")
                return Response({'error': 'Face descriptor must be a list of 128 float values.'}, status=400)
        except ValueError as e:
            logger.error(f"Error converting face descriptor to NumPy array for user_id: {user_id} - {str(e)}")
            return Response({'error': 'Face descriptor must be valid floats.'}, status=400)

        # Retrieve or create the FaceDescriptor instance
        face_descriptor, created = FaceDescriptor.objects.get_or_create(user_id=user_id)

        # Save the descriptor in both NumPy and list formats
        face_descriptor.numpy_face_descriptor = numpy_face_descriptor.tobytes()  # Save as binary
        face_descriptor.face_descriptor = face_descriptor_data  # Save as list
        face_descriptor.save()

        logger.info(f"{'Created' if created else 'Updated'} face descriptor for user_id: {user_id}")

        # Serialize and return the response
        serialized_data = FaceDescriptorSerializer(face_descriptor)
        return Response(serialized_data.data, status=200)



#---------------------------------------------------FaceView Section-------------------------------------------------

# Set up logging
logger = logging.getLogger(__name__)



logger = logging.getLogger(__name__)

class SearchFaceView(APIView):
    def post(self, request, *args, **kwargs):
        # Retrieve the uploaded face descriptor
        uploaded_face_descriptor = request.data.get('face_descriptor')

        if not uploaded_face_descriptor:
            logger.error("No face descriptor provided.")
            return Response({"error": "No face descriptor provided."}, status=status.HTTP_400_BAD_REQUEST)

        if not isinstance(uploaded_face_descriptor, list) or len(uploaded_face_descriptor) != 128:
            logger.error("Invalid face descriptor format.")
            return Response({"error": "Face descriptor must be a list of 128 float values."}, status=status.HTTP_400_BAD_REQUEST)

        # Convert to NumPy array for computation
        try:
            uploaded_array = np.array(uploaded_face_descriptor, dtype=np.float32)
        except ValueError:
            logger.error("Uploaded face descriptor conversion to NumPy array failed.")
            return Response({"error": "Invalid face descriptor values."}, status=status.HTTP_400_BAD_REQUEST)

        matched_users = []
        face_descriptors = FaceDescriptor.objects.all()

        for face_data in face_descriptors:
            try:
                # Convert stored descriptor back to NumPy array
                stored_descriptor = np.frombuffer(face_data.numpy_face_descriptor, dtype=np.float32)

                if stored_descriptor.shape[0] != 128:
                    logger.warning(f"Skipping descriptor with invalid size for user_id {face_data.user.id}")
                    continue

                # Compute cosine similarity
                similarity = 1 - (
                    np.dot(uploaded_array, stored_descriptor) /
                    (np.linalg.norm(uploaded_array) * np.linalg.norm(stored_descriptor))
                )

                if similarity > 0.1:  # Match threshold
                    logger.debug(f"Match found for user_id {face_data.user.id} with similarity {similarity}")
                    serializer = UserProfileSerializer(face_data.user)
                    matched_users.append(serializer.data)
                    logger.debug(f"Similarity score between uploaded and stored descriptor: {similarity}")


                    # Save debug info
                    DebugFaceMatch.objects.create(
                        user=face_data.user,
                        uploaded_descriptor=uploaded_array.tolist(),
                        stored_descriptor=stored_descriptor.tolist(),
                        similarity_score=similarity,
                    )

            except Exception as e:
                logger.error(f"Error processing descriptor for user_id {face_data.user.id}: {e}")

        logger.info(f"{len(matched_users)} matches found.")
        return Response({"matched_users": matched_users}, status=status.HTTP_200_OK)




#-------------------------------FaceView Section---------------------------------------------------------------------































class GetFaceDataView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        try:
            face_data = FaceDescriptor.objects.get(user=request.user)
            return Response(FaceDescriptor(face_data).data, status=status.HTTP_200_OK)
        except FaceDescriptor.DoesNotExist:
            return Response({"error": "Face data not found for this user."}, status=status.HTTP_404_NOT_FOUND)




class ListFaceDataView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        face_data = FaceDescriptor.objects.all()
        return Response(FaceDescriptorSerializer(face_data, many=True).data, status=status.HTTP_200_OK)

class DeleteFaceDataView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request):
        try:
            face_data = FaceDescriptor.objects.get(user=request.user)
            face_data.delete()
            return Response({"message": "Face data deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
        except FaceDescriptor.DoesNotExist:
            return Response({"error": "Face data not found for this user."}, status=status.HTTP_404_NOT_FOUND)
