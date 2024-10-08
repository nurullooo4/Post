from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver


from django.contrib.auth.models import User

from app_main.models import Post


@receiver(signal=post_save, sender=User)
def print_user_creation(sender, instance, created, **kwargs):
    if created:
        email = instance.username + '@gmail.com'
        instance.email = email
        instance.save()

@receiver(pre_delete, sender=User)
def print_user_deletion(sender, instance, **kwargs):
    for post in Post.objects.filter(owner=instance):
        post.delete()
