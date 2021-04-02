from allauth.account.adapter import DefaultAccountAdapter
from profiles.models import Image
# from .geo_script import get_coordinates_from_ip


# Adapter is needed for using MyCustomRegisterSerializer
class CustomAccountAdapter(DefaultAccountAdapter):

    def save_user(self, request, user, form, commit=False):

        user = super().save_user(request, user, form, commit)
        data = form.cleaned_data
        user.user_nickname = data.get('user_nickname')
        user.gender = data.get('gender')
        user.subscription = data.get('subscription')
        profile_image = data.get('profile_image')
        additional_image = data.get('additional_image')

        # Script listed below is designed for auto getting coordinates from users ip and to put them in DB.
        # While using in development purposes I commented it and saving in DB userprofile-model default
        # values. Notice, after creating new user in DB wll be automatically saved last_updated_coordinates
        # time, and user will get an ability to update his coordinates (from default values) only through
        # 2 hours after creating his profile.

        # x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        # if x_forwarded_for:
        #     ip = x_forwarded_for.split(',')[0]
        # else:
        #     ip = request.META.get('REMOTE_ADDR')
        # print(ip)
        # latitude = get_coordinates_from_ip(ip)[0]
        # longitue = get_coordinates_from_ip(ip)[1]
        # user.latitude = data.get('latitude')
        # user.longitude = data.get('longitude')

        # According tho this restriction only users with subscription 'Premium' can save in DB value
        # of premium distance, in other cases there will be Null.
        if user.subscription == 'Premium':
            user.premium_distance = data.get('premium_distance')
        else:
            user.premium_distance = None
        user.save()
        Image.objects.create(user=user, profile_image=profile_image, additional_image=additional_image)
        return user