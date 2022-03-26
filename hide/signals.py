# from django.db.models.signals import post_delete, post_save
# from django.dispatch import receiver
#
# from helpers.update_reactions import add_dislikes, decrease_dislikes
# from hide.models import Hide
#
#
# @receiver(post_save, sender=Hide)
# def post_save_hide(sender, instance, created, **kwargs):
#     add_dislikes(instance)
#
#
# @receiver(post_delete, sender=Hide)
# def post_delete_hide(sender, instance, **kwargs):
#     decrease_dislikes(instance)
