from rest_framework import viewsets
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from rest_framework import permissions
from django.http import HttpResponseRedirect
from profiles.serializers import MyUserListSerializer, MyUserDetailSerializer
from profiles.custompermission import IfPermissionForLike
from profiles.search_users import find_users


class UsersViewSet(viewsets.GenericViewSet):

    def get_queryset(self):
        user_instance = get_user_model().objects.get(pk=self.request.user.id)
        queryset = find_users(user_instance)
        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = MyUserListSerializer(queryset, many=True, context={'request': request})
        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        user = get_object_or_404(get_user_model(), pk=kwargs['pk'])
        self.check_object_permissions(self.request, user)
        serializer = self.serializer_class(user,  context={'request': request})
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        instance = get_object_or_404(get_user_model(), pk=kwargs['pk'])
        serializer = self.serializer_class(instance, request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        like_value = serializer.validated_data['like']
        if like_value:
            if request.user.id not in instance.my_likes:
                instance.my_likes.append(request.user.id)
            another_instance = get_user_model().objects.get(pk=request.user.id)
            if int(kwargs['pk']) not in another_instance.whom_I_liked:
                another_instance.whom_I_liked.append(kwargs['pk'])
                another_instance.save()
            if request.user.id in instance.whom_I_liked and request.user.id not in instance.match:
                instance.match.append(request.user.id)
                another_instance.match.append(kwargs['pk'])
                another_instance.save()
        serializer.save()

        # There is better to return Response, but in my situation I use HTTPResponseRedirect for refreshing
        # page (after refreshing will appear field conversations if there is match between users). It is
        # better to implement redirection in frontend then here.
        # return Response(serializer.data)
        return HttpResponseRedirect(redirect_to=f"http://127.0.0.1:8000/api/v1/userprofile/{kwargs['pk']}/")

    serializer_class = MyUserDetailSerializer
    permission_classes = (
        permissions.IsAuthenticated,
        IfPermissionForLike
    )
