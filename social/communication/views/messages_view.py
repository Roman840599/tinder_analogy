from rest_framework import generics
from django.contrib.auth import get_user_model
from rest_framework import permissions
from django.http import HttpResponseRedirect
from communication.models import Message
from communication.serializers import MessageSerializer
from profiles.custompermission import IfPermissionForCommunicate


class MessageList(generics.ListCreateAPIView):

    # Will return only messages which concern two users participated in conversation.
    def get_queryset(self):
        queryset = list(Message.objects.all())
        user = self.request.user
        second_users_pk = self.kwargs['pk']
        second_users_nickname = get_user_model().objects.get(pk=second_users_pk)
        result_queryset = []
        for i in queryset:
            if (i.message_sender == user and i.message_receiver == second_users_nickname) \
                    or (i.message_sender == second_users_nickname and i.message_receiver == user):
                result_queryset.append(i)
        return result_queryset

    # Method is overridden for redirecting user to massage list after creating new massage. And there will be
    # auto fill of the fields 'message sender' and 'message receiver'.
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        sender_id = request.user.id
        receiver_id = self.kwargs['pk']
        serializer.validated_data['message_sender'] = get_user_model().objects.get(pk=sender_id)
        serializer.validated_data['message_receiver'] = get_user_model().objects.get(pk=receiver_id)
        self.perform_create(serializer)
        second_users_pk = self.kwargs['pk']
        second_users_conversation_url = get_user_model().objects.get(pk=second_users_pk).conversation
        return HttpResponseRedirect(redirect_to=second_users_conversation_url)

    serializer_class = MessageSerializer
    name = 'massage-list'
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
        IfPermissionForCommunicate,
    )
