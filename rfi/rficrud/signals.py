from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import RFI


def translate_by_api(text):
    """Func that recieve text and translating to english"""
    pass


@receiver(post_save, sender=RFI)
def translate_to_english(sender, instance, **rwargs):
    """Func that translating offline, but first need to train model to do it"""

    instance.description_of_work_english = translate_to_english(
                                            instance.description_of_work_russian)
