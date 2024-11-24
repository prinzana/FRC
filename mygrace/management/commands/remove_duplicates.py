from django.core.management.base import BaseCommand
from mygrace.models import Verification
from django.db.models import Count

class Command(BaseCommand):
    help = 'Removes duplicate verification records and keeps the most recent one.'

    def handle(self, *args, **kwargs):
        # Identify users with more than one verification record
        duplicate_users = Verification.objects.values('user').annotate(user_count=Count('user')).filter(user_count__gt=1)

        for user in duplicate_users:
            user_verifications = Verification.objects.filter(user_id=user['user']).order_by('-submitted_at')
            verification_to_keep = user_verifications.first()  # Keep the most recent

            # Delete the rest of the duplicates except for the most recent record
            user_verifications.exclude(id=verification_to_keep.id).delete()

            self.stdout.write(self.style.SUCCESS(f"Deleted duplicate verification records for user {user['user']}, keeping the most recent."))
