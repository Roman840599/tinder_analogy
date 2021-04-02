from rest_framework import viewsets
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from rest_framework import permissions
from rest_framework.response import Response
from communication.models import Dialog, Message
from communication.serializers import DialogListSerializer, DialogDetailSerializer
from profiles.custompermission import IfPermissionForDialog


class DialogViewSet(viewsets.ViewSet):

    def get_queryset(self):
        result_queryset = []
        user = int(self.request.user.id)
        queryset = Dialog.objects.all()
        for instance in queryset:
            if int(instance.participant_one) == user or int(instance.participant_two) == user:
                result_queryset.append(instance)
        return result_queryset

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = DialogListSerializer(queryset, many=True, context={'request': request})
        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        instance = get_object_or_404(Dialog, pk=kwargs['pk'])
        self.check_object_permissions(self.request, instance)
        serializer = self.serializer_class(instance,  context={'request': request})
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        instance = get_object_or_404(Dialog, pk=kwargs['pk'])
        serializer = self.serializer_class(instance, request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)

        user = int(self.request.user.id)
        pk = int(kwargs['pk'])
        instance = Dialog.objects.get(pk=pk)
        if int(instance.participant_two) == user:
            receiver_id = int(instance.participant_one)
        else:
            receiver_id = int(instance.participant_two)

        sender_instance = get_user_model().objects.get(pk=user)
        receiver_instance = get_user_model().objects.get(pk=receiver_id)
        message_content= request.data['message_content']
        Message.objects.create(message_sender=sender_instance, message_receiver=receiver_instance,
                               message_content=message_content)
        return Response(serializer.data)

    serializer_class = DialogDetailSerializer
    permission_classes = (
        permissions.IsAuthenticated,
        IfPermissionForDialog
    )
