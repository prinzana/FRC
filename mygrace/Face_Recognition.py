import face_recognition
import numpy as np
from PIL import Image
from io import BytesIO

def extract_face_descriptor(image_file):
    """
    Extracts the face descriptor from an uploaded image file.
    Returns a 128-dimensional list if a face is detected, otherwise None.
    """
    try:
        # Open the image file
        image = Image.open(image_file)
        image_np = np.array(image)

        # Detect face locations
        face_locations = face_recognition.face_locations(image_np)
        if not face_locations:
            print("No face detected in the image.")
            return None  # No face found

        # Extract face encodings
        face_encodings = face_recognition.face_encodings(image_np, face_locations)
        if face_encodings:
            # Return the first face descriptor as a list
            face_descriptor = [float(value) for value in face_encodings[0]]
            print("Extracted face descriptor:", face_descriptor)
            return face_descriptor
        else:
            print("No encodings found for detected faces.")
            return None
    except Exception as e:
        print("Error in extract_face_descriptor:", e)
        return None
