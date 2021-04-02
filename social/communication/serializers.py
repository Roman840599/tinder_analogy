from rest_framework import serializers
from .models import Message, Dialog


class MessageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Message
        fields = ('id', 'current_time', 'message_sender', 'message_receiver', 'message_content')
        extra_kwargs = {
            'message_sender': {'read_only': True},
            'message_receiver': {'read_only': True}
        }


class DialogListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Dialog
        fields = ('id', 'url', 'participant_one', 'participant_two')


class DialogDetailSerializer(serializers.ModelSerializer):
    messages = MessageSerializer(read_only=True, many=True)
    message_content = serializers.CharField(write_only=True)

    class Meta:
        model = Dialog
        fields = ('id', 'participant_one', 'participant_two', 'messages', 'message_content')
        extra_kwargs = {
            'participant_one': {'read_only': True},
            'participant_two': {'read_only': True}
        }
