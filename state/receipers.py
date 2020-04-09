# from django.dispatch import receiver
# from django.db.models.signals import post_save

# from search_in_video.models import Video

# from channels.layers import get_channel_layer
# from asgiref.sync import async_to_sync


# @receiver(post_save, sender=Video)
# def announce_state(sender, instance, **kwargs):
#     if instance.__original_state != instance.state:
#         channel_layer = get_channel_layer()
#         async_to_sync(channel_layer.group_send)(
#             'state_%s' % instance.id, {
#                 'type': 'state_message',
#                 'message': instance.state
#             }
#         )