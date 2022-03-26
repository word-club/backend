# from django.db.models.signals import post_save
# from django.dispatch import receiver
#
# from helpers.update_reactions import add_popularity, add_supports
# from .models import Publication
#
#
# @receiver(post_save, sender=Publication)
# def post_save_signal(sender, instance, created, **kwargs):
#     """
#     Signal for post save signal.
#     """
#     if created:
#         add_popularity(instance)
#         add_supports(instance)
