from django.db.models.signals import post_save, post_delete
from django.contrib.auth.models import User
from .models import Profile
from django.conf import settings
from django.core.mail import send_mail

# Signals in Django is used, whenever a profile or user is created/updated or deleted some actions needs to be done

# creates profile when a user is created otherwise we need to create user and profile separately

# created=first time a user is created
# sender=class that is sending
# instance=name of the sender


def createProfile(sender, instance, created, **kwargs):
    if created:
        user = instance
        profile = Profile.objects.create(
            user=user,
            username=user.username,
            email=user.email,
            name=user.first_name,
        )
        subject="Welcome to DevSearch"
        message="We are glad you are here"
        send_mail(subject,message,settings.EMAIL_HOST_USER,[profile.email],fail_silently=False)

# when profile is updated user also needs to be updated


def updateUser(sender, instance, created, **kwargs):
    profile = instance
    # from one to one relation taking user from the profile
    user = profile.user
    if created == False:
        user.first_name = profile.name
        user.username = profile.username
        user.email = profile.email
        user.save()



# deletes the user when profile is deleted, if user is deleted profile is automatically deleted but not so in other


def deleteUser(sender, instance, **kwargs):
    try:
        user = instance.user
        user.delete()
    except:
        pass


post_save.connect(createProfile, sender=User)
post_save.connect(updateUser, sender=Profile)
post_delete.connect(deleteUser, sender=Profile)


# signals.py needs to be registered in apps.py. If it is inside models.py that it doesn't need to be registered
