from django.contrib import admin
from .models import MyGraceAdmin, MyGraceUser, Verification, ActivityLog

from .forms import MyGraceAdminCreationForm, MyGraceAdminChangeForm, MyGraceUserCreationForm, MyGraceUserChangeForm

# Admin configuration for MyGraceAdmin model
class MyGraceAdminAdmin(admin.ModelAdmin):
    form = MyGraceAdminChangeForm
    add_form = MyGraceAdminCreationForm
    list_display = ('username', 'email', 'fullname', 'is_staff', 'is_superuser', 'created_at')
    search_fields = ('username', 'email', 'fullname')

# Admin configuration for MyGraceUser model
class MyGraceUserAdmin(admin.ModelAdmin):
    form = MyGraceUserChangeForm
    add_form = MyGraceUserCreationForm
    list_display = ('username', 'email', 'fullname', 'is_verified', 'is_active', 'created_at')
    search_fields = ('username', 'email', 'fullname')

# Admin configuration for Verification model
class VerificationAdmin(admin.ModelAdmin):
    list_display = ('user', 'id_type', 'id_number', 'is_verified', 'submitted_at', 'verified_at', 'rejection_reason')
    list_filter = ('is_verified',)
    search_fields = ('user__username', 'id_number', 'id_type')

# Admin configuration for ActivityLog model
class ActivityLogAdmin(admin.ModelAdmin):
    list_display = ('user', 'action', 'date')
    search_fields = ('user__username', 'action')

# Register models to admin
admin.site.register(MyGraceAdmin, MyGraceAdminAdmin)
admin.site.register(MyGraceUser, MyGraceUserAdmin)
admin.site.register(Verification, VerificationAdmin)
admin.site.register(ActivityLog, ActivityLogAdmin)
from django.contrib import admin
from .models import FaceDescriptor, FaceRecognitionData

admin.site.register(FaceDescriptor)
admin.site.register(FaceRecognitionData)
# mygrace/admin.py
from django.contrib import admin
from .models import FaceData

admin.site.register(FaceData)


from django.contrib import admin
from .models import DebugFaceMatch

@admin.register(DebugFaceMatch)
class DebugFaceMatchAdmin(admin.ModelAdmin):
    list_display = ('id', 'similarity_score', 'user', 'timestamp')
    list_filter = ('timestamp',)
    search_fields = ('user__username',)
