from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
from profiles.models import UserProfile


class Dialog(models.Model):
    participant_one = models.CharField(max_length=100, null=True)
    participant_two = models.CharField(max_length=100, null=True)

    def __str__(self):
        return f'{self.participant_one} and {self.participant_two}'


class Message(models.Model):
    current_time = models.DateTimeField(auto_now_add=True)
    dialog = models.ForeignKey(
        Dialog,
        related_name='messages',
        on_delete=models.CASCADE,
        null=True
    )
    message_sender = models.ForeignKey(
        UserProfile,
        related_name='messages_I_have_send',
        on_delete=models.CASCADE
    )
    message_receiver = models.ForeignKey(
        UserProfile,
        related_name='messages_I_have_received',
        on_delete=models.CASCADE
    )
    message_content = models.TextField()

    class Meta:
        ordering = ('current_time',)


# Due to this signal after creating each new message will be created new dialog to which this message will be
# belong to.
@receiver(pre_save, sender=Message)
def save_profile(sender, instance, **kwargs):

    consisting_dialogs_1 = Dialog.objects.filter(participant_one=instance.message_sender.id,
                                                 participant_two=instance.message_receiver.id)
    consisting_dialogs_2 = Dialog.objects.filter(participant_one=instance.message_receiver.id,
                                                 participant_two=instance.message_sender.id)

    # There we check if dialog with such participants already exists.
    if len(consisting_dialogs_1) == 0 and len(consisting_dialogs_2) == 0:
        Dialog.objects.create(participant_one=instance.message_sender.id,
                              participant_two=instance.message_receiver.id)
        instance.dialog = Dialog.objects.get(participant_one=instance.message_sender.id,
                                             participant_two=instance.message_receiver.id)
    elif len(consisting_dialogs_1) != 0:
        instance.dialog = Dialog.objects.get(pk=consisting_dialogs_1[0].id)
    else:
        instance.dialog = Dialog.objects.get(pk=consisting_dialogs_2[0].id)
