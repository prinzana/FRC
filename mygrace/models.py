from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils import timezone
from django.contrib.auth import get_user_model

# Manager for admin user
class MyGraceAdminManager(BaseUserManager):
    def create_admin(self, username, email, fullname, password=None, **extra_fields):
        if not username:
            raise ValueError('The Username field must be set')
        if not email:
            raise ValueError('The Email field must be set')
        if not fullname:
            raise ValueError('The Full Name field must be set')

        email = self.normalize_email(email)
        admin = self.model(username=username, email=email, fullname=fullname, **extra_fields)
        admin.set_password(password)
        admin.is_staff = True
        admin.is_superuser = True
        admin.is_active = True  # Ensure the admin is active
        admin.save(using=self._db)
        return admin

# Manager for regular user
class MyGraceUserManager(BaseUserManager):
    def create_user(self, username, email, fullname, password=None, **extra_fields):
        if not username:
            raise ValueError('The Username field must be set')
        if not email:
            raise ValueError('The Email field must be set')
        if not fullname:
            raise ValueError('The Full Name field must be set')

        email = self.normalize_email(email)
        user = self.model(username=username, email=email, fullname=fullname, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

# MyGraceAdmin model (admins)
class MyGraceAdmin(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=255, unique=True)
    email = models.EmailField(unique=True)
    fullname = models.CharField(max_length=255)
    
    # Define the role field for MyGraceAdmin model
    ADMIN = 'ADMIN'
    USER = 'USER'
    ROLE_CHOICES = [
        (ADMIN, 'Admin'),
        (USER, 'User'),
    ]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default=ADMIN)
    
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=True)  # Admins must be staff
    is_superuser = models.BooleanField(default=True)  # Admins must be superusers
    created_at = models.DateTimeField(default=timezone.now)
  
    objects = MyGraceAdminManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'fullname']

    def __str__(self):
        return self.username

# MyGraceUser model (for regular users)
class MyGraceUser(AbstractBaseUser):
    username = models.CharField(max_length=255, unique=True)
    email = models.EmailField(unique=True)
    fullname = models.CharField(max_length=255)
    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)  # Regular users are not staff
    is_superuser = models.BooleanField(default=False)  # Regular users are not superusers
    created_at = models.DateTimeField(default=timezone.now)
    community = models.CharField(max_length=255, blank=True, null=True)
    clan = models.CharField(max_length=255, blank=True, null=True)
    family_name = models.CharField(max_length=255, blank=True, null=True)
    state_of_residence = models.CharField(max_length=255, blank=True, null=True)
    lga_of_residence = models.CharField(max_length=255, blank=True, null=True)
    occupation = models.CharField(max_length=255, blank=True, null=True)
    sex = models.CharField(max_length=255, blank=True, null=True)
    state_of_origin = models.CharField(max_length=255, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profiles/', blank=True, null=True)  # Optional, only define once
    public_visibility = models.BooleanField(default=True)  # Default to True for public visibility
    lga_of_origin = models.CharField(max_length=255, blank=True, null=True)

    objects = MyGraceUserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'fullname']

    def __str__(self):
        return self.username

# ActivityLog model (to track user activities)
class ActivityLog(models.Model):
    ACTION_TYPES = [
        ('LOGIN', 'Login'),
        ('UPDATE', 'Profile Update'),
        ('PASSWORD_CHANGE', 'Password Change'),
        ('PROFILE_UPDATE', 'Profile Update'),
        ('VIEW_PROFILE', 'Profile View'),
        # Add any other action types you need
    ]

    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)  # Linking to the User model dynamically
    action = models.CharField(max_length=100)
    details = models.TextField(null=True, blank=True)  # Store extra information (if necessary)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} - {self.action} - {self.date}"
    
class Verification(models.Model):
    user = models.OneToOneField(MyGraceUser, on_delete=models.CASCADE)
    id_type = models.CharField(max_length=255, null=False, default='Unknown')
    id_number = models.CharField(max_length=255, null=False, default='default_id_number')
    id_document = models.FileField(upload_to='verification_docs/', null=False, default='default/path/to/file')
    is_verified = models.BooleanField(default=False)
    submitted_at = models.DateTimeField(default=timezone.now)
    verified_at = models.DateTimeField(blank=True, null=True)
    rejection_reason = models.TextField(blank=True, null=True)
    has_requested_verification = models.BooleanField(default=False)  # This field

from django.db.models.signals import post_save
from django.dispatch import receiver
from mygrace.models import MyGraceUser, Verification

@receiver(post_save, sender=MyGraceUser)
def handle_user_verification(sender, instance, **kwargs):
    # Check if the user has been unverified
    if instance.is_verified == False:
        # Delete the verification record if it exists
        Verification.objects.filter(user=instance).delete()


    def __str__(self):
        return f"{self.user} - {self.is_verified}"
    



from django.db import models
from django.contrib.auth import get_user_model

class FaceDescriptor(models.Model):
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE, related_name='face_descriptor')
    face_descriptor = models.JSONField(null=True, blank=True)

    def __str__(self):
        return f"Face descriptor for {self.user.username}"
    




    

class FaceRecognitionData(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)  # Link to the user
    face_descriptor = models.JSONField()  # Store the face descriptor as a JSON field
    uploaded_at = models.DateTimeField(auto_now_add=True)  # Timestamp for when the data was uploaded

class Meta:
    constraints = [
        models.UniqueConstraint(fields=['user', 'face_descriptor'], name='unique_user_face_descriptor')
    ]
from django.core.exceptions import ValidationError

def clean(self):
    if self.face_descriptor:
        if not isinstance(self.face_descriptor, list) or not all(isinstance(i, float) for i in self.face_descriptor):
            raise ValidationError("Face descriptor must be a list of floats.")
    super().clean()


    def __str__(self):
        return f"Face data for {self.user.username}"

# mygrace/models.py
from django.conf import settings
from django.db import models

class FaceData(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="face_data")
    profile_picture = models.ImageField(upload_to="profile_pictures/", null=True, blank=True)
    face_descriptor = models.JSONField(null=True, blank=True)  # Use JSONField for face descriptors

    def __str__(self):
        return f"{self.user.username}'s Face Data"


from django.db import models
from django.contrib.auth import get_user_model
import numpy as np
import numpy as np
from django.db import models
from django.contrib.auth import get_user_model
import logging


logger = logging.getLogger(__name__)

from django.db import models
from django.contrib.auth import get_user_model

class FaceDescriptor(models.Model):
    user = models.OneToOneField(MyGraceUser, on_delete=models.CASCADE, related_name="face_descriptor")
    face_descriptor = models.JSONField(null=True, blank=True)  # Original face descriptor as JSON
    numpy_face_descriptor = models.BinaryField(null=True, blank=True)  # For NumPy serialized descriptor

    def __str__(self):
        return f"Face descriptor for {self.user.username}"

    def to_numpy(self):
        """Convert the stored JSON face descriptor to a NumPy array."""
        if self.face_descriptor:
            return np.array(self.face_descriptor, dtype=np.float32)
        return None

    def save(self, *args, **kwargs):
        """Ensure the descriptor is valid before saving."""
        if self.face_descriptor and len(self.face_descriptor) != 128:
            raise ValueError("Face descriptor must be a list of 128 float values.")
        super().save(*args, **kwargs)



#----------------------------------------DEBUG MODEL---------------------------------------------------------------


class DebugFaceMatch(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,  # Points to MyGraceUser model
        on_delete=models.CASCADE,
        related_name='debug_face_matches'
    )
    uploaded_descriptor = models.JSONField()
    stored_descriptor = models.JSONField()
    similarity_score = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)  # Automatically set the timestamp on creation

    def __str__(self):
        return f"DebugFaceMatch for {self.user} at {self.timestamp}"
from .models import FaceDescriptor  # Make sure you import the correct model

def save_face_descriptor(user, face_descriptor_array):
    # Convert numpy array to list if needed
    face_descriptor_list = face_descriptor_array.tolist()  # Convert numpy array to list
    
    # Check if the user already has a face descriptor entry
    face_descriptor, created = FaceDescriptor.objects.update_or_create(
        user=user,  # Link it to the user
        defaults={'descriptor': face_descriptor_list}  # Store the descriptor data
    )
    return face_descriptor
