from rest_framework import generics
from rest_framework.response import Response
from rest_framework.reverse import reverse
from . import profile_view


class ApiRoot(generics.GenericAPIView):
    name = 'api-root'

    def get(self, request, *args, **kwargs):
        return Response({
            'find_friend': request.build_absolute_uri('userprofile/'),
            'my_profile': reverse(profile_view.ProfileDetailView.name, request=request),
            'my_dialogs': request.build_absolute_uri('dialog/'),
        })
