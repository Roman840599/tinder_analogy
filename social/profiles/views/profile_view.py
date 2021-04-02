from rest_framework import generics
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser
from django.utils import timezone
from profiles.serializers import ProfileSerializer
from profiles.custompermission import IsCurrentUserOwnerOrReadOnly
from profiles.models import Image


class ProfileDetailView(generics.RetrieveUpdateDestroyAPIView):

    def get_queryset(self):
        user = self.request.user.id
        return get_user_model().objects.filter(id=user)

    # I have  overridden this method to make possible to get this view with the link http:.../profile.
    # Otherwise this method will be needed pk argument.
    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())
        obj = get_object_or_404(queryset)
        self.check_object_permissions(self.request, obj)
        return obj

    # There is a restriction according to which when performing profile update in DB will be saved
    # form premium_distance value only if form subscription value is 'Premium', otherwise will be saved None.
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        time_last_updated = instance.last_updated_coordinates
        previous_latitude = instance.latitude
        previous_longitude = instance.longitude
        datetime_now = timezone.now()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)

        related_image_instance = Image.objects.get(user_id=instance.id)
        if 'profile_image' in serializer.validated_data and 'additional_image' in serializer.validated_data:
            new_profile_image = serializer.validated_data['profile_image']
            new_additional_image = serializer.validated_data['additional_image']
            related_image_instance.profile_image = new_profile_image
            related_image_instance.additional_image = new_additional_image
            related_image_instance.save()
        elif 'profile_image' in serializer.validated_data:
            new_profile_image = serializer.validated_data['profile_image']
            related_image_instance.profile_image = new_profile_image
            related_image_instance.save()
        elif 'additional_image' in serializer.validated_data:
            new_additional_image = serializer.validated_data['additional_image']
            related_image_instance.additional_image = new_additional_image
            related_image_instance.save()

        if serializer.validated_data['subscription'] != 'Premium':
            serializer.validated_data['premium_distance'] = None

        # There I've implemented update-coordinates logic (if previous updating of coordinates where
        # performed less then 2 hours before so new coordinates won't be putted in DB)
        if serializer.validated_data['latitude'] != previous_latitude or \
                serializer.validated_data['longitude'] != previous_longitude:
            if (datetime_now - time_last_updated).seconds // 3600 < 2:
                serializer.validated_data['latitude'] = previous_latitude
                serializer.validated_data['longitude'] = previous_longitude
            else:
                instance.last_updated_coordinates = datetime_now
        self.perform_update(serializer)
        return Response(serializer.data)

    serializer_class = ProfileSerializer
    name = 'profile-detail'
    permission_classes = (
        IsCurrentUserOwnerOrReadOnly,
    )
