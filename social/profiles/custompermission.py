from rest_framework import permissions
from django.contrib.auth import get_user_model


class IsCurrentUserOwnerOrReadOnly(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        else:
            return obj.id == request.user.id


class IfPermissionForCommunicate(permissions.BasePermission):

    def has_permission(self, request, view):
        uri = request.build_absolute_uri()
        l = uri.split('/')
        pk_index = l.index('userprofile') + 1
        pk = l[pk_index]
        instance_wich_user_try_to_communicate = get_user_model().objects.get(pk=pk)
        if request.user.id in instance_wich_user_try_to_communicate.match:
            return True
        else:
            return False


class IfPermissionForLike(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):

        if str(obj.id) in request.user.todays_queryset:
            return True
        else:
            return False


class IfPermissionForDialog(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if int(obj.participant_one) == request.user.id or int(obj.participant_two) == request.user.id:
            return True
        else:
            return False
