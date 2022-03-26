from django.contrib.auth.models import User
from django.core.validators import MinLengthValidator
from django.db import models
from django.conf import settings
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.contrib.auth.models import AbstractUser


class Profile(models.Model):
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
    )

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    city = models.CharField(max_length=120, blank=False)
    country = models.CharField(max_length=120, blank=False)
    state = models.CharField(max_length=120, blank=False)
    zip_code = models.CharField(max_length=5, validators=[MinLengthValidator(5)], blank=False)

    def __str__(self):
        return self.user


class EmergencyContacts(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    state = models.CharField(max_length=120, blank=False)
    phone_number = models.CharField(max_length=120, blank=False)

    def __str__(self):
        return self.user


# @receiver(post_save, sender=User)
# def create_profile(sender, instance, created, **kwargs):
#     if created:
#         Profile.objects.create(user=instance,)


# @receiver(post_save, sender=User)
# def save_user_profile(sender, instance, **kwargs):
#     instance.profile.save()


@receiver(post_delete, sender=User)
def delete_user(sender, instance=None, **kwargs):
    try:
        instance.user
    except User.DoesNotExist:
        print("User does not exists")
    else:
        instance.user.delete()

