from django.conf import settings
from django.contrib.auth.models import User, Group
from django.db.models.signals import post_migrate
from django.dispatch import receiver

@receiver(post_migrate)
def create_superuser(sender, **kwargs):
    # Check if superuser already exists
    if not User.objects.filter(is_superuser=True).exists():
        # Define the superuser credentials
        superuser_username = 'thole'
        superuser_password = 'tholethunder'

        superuser = User.objects.create_superuser(
            username=superuser_username,
            password=superuser_password,
        )

        admin_group, created = Group.objects.get_or_create(name='admin')

        superuser.groups.add(admin_group)

        print(f"Superuser created with username: {superuser_username} and password: {superuser_password}")
        print("Superuser added to 'admin' group.")
