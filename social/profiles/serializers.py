from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_auth.registration.serializers import RegisterSerializer
import re
from .models import Image


class MyCustomRegisterSerializer(RegisterSerializer):
    MALE = 'M'
    FEMALE = 'F'
    GENDER_CHOICES = (
        (MALE, 'Male'),
        (FEMALE, 'Female'),
    )

    BASIC = 'Basic'
    VIP = 'VIP'
    PREMIUM = 'Premium'
    SUBSCRIPTION_CHOICES =(
        (BASIC, 'Basic'),
        (VIP, 'VIP'),
        (PREMIUM, 'Premium'),
    )
    user_nickname = serializers.CharField(
        required=False,
        max_length=30,
    )
    gender = serializers.ChoiceField(
        choices=GENDER_CHOICES,
    )
    subscription = serializers.ChoiceField(
        choices=SUBSCRIPTION_CHOICES,
        default=BASIC,
    )
    premium_distance = serializers.IntegerField(allow_null=True)
    profile_image = serializers.ImageField(
        max_length=None,
        required=True,
        use_url=True
    )
    additional_image = serializers.ImageField(
        max_length=None,
        required=False,
        use_url=True
    )

    def get_cleaned_data(self):
        data_dict = super().get_cleaned_data()
        data_dict['user_nickname'] = self.validated_data.get('user_nickname', '')
        data_dict['gender'] = self.validated_data.get('gender', '')
        data_dict['subscription'] = self.validated_data.get('subscription', '')
        data_dict['premium_distance'] = self.validated_data.get('premium_distance', '')
        data_dict['profile_image'] = self.validated_data.get('profile_image', '')
        data_dict['additional_image'] = self.validated_data.get('additional_image', '')
        return data_dict


class ImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Image
        fields = ('id', 'profile_image', 'additional_image')


class MyUserListSerializer(serializers.ModelSerializer):
    images = ImageSerializer(read_only=True, many=True)

    class Meta:
        model = get_user_model()
        fields = ('url', 'username', 'images', 'email', 'user_nickname', 'match', 'latitude', 'longitude')


class MyUserDetailSerializer(serializers.ModelSerializer):
    images = ImageSerializer(read_only=True, many=True)
    like = serializers.BooleanField(default=False, write_only=True)

    class Meta:
        model = get_user_model()
        fields = ('username', 'images', 'email', 'user_nickname', 'my_likes', 'whom_I_liked',
                  'match', 'conversation', 'like')
        extra_kwargs = {
            'username': {'read_only': True},
            'email': {'read_only': True},
            'my_likes': {'read_only': True},
            'whom_I_liked': {'read_only': True},
            'match': {'read_only': True},
            'conversation': {'read_only': True},
            'user_nickname': {'read_only': True}
        }

    # Method is overridden to hide field conversation and its link in case there is no match between users.
    def __init__(self, *args, **kwargs):
        try:
            if len(args) != 0:
                if kwargs['context']['request'].user.id not in args[0].match:
                    del self.fields['conversation']
            else:
                if kwargs['context']['request'].user.id not in kwargs['instance'].match:
                    del self.fields['conversation']
        except AttributeError:
            pass
        super().__init__(*args, **kwargs)


class ProfileSerializer(serializers.ModelSerializer):
    images = ImageSerializer(read_only=True, many=True)
    profile_image = serializers.ImageField(max_length=None, required=False, write_only=True)
    additional_image = serializers.ImageField(max_length=None, required=False, write_only=True)

    class Meta:
        model = get_user_model()
        fields = ('id', 'url', 'username', 'images', 'email', 'user_nickname', 'gender', 'subscription',
                  'premium_distance', 'my_likes', 'whom_I_liked', 'match', 'latitude', 'longitude',
                  'profile_image', 'additional_image')
        extra_kwargs = {
            'my_likes': {'read_only': True},
            'whom_I_liked': {'read_only': True},
            'match': {'read_only': True},
        }

    # Check that latitude and longitude are valid coordinates (if match 'NN.NNNNN' pattern). And there
    # we clean coordinates from users mistakes (for input 'fgdfgNN.NNNNN' will return 'NN.NNNNN')
    def validate(self, data):
        latitude = data['latitude']
        longitude = data['longitude']
        pattern = r'[0-9]{2}\.[0-9]{5,9}'
        cleaned_latitude = re.findall(pattern, latitude)
        cleaned_longitude = re.findall(pattern, longitude)
        if len(cleaned_longitude) == 0 or len(cleaned_latitude) == 0:
            raise serializers.ValidationError("invalid coordinates")
        else:
            data['latitude'] = cleaned_latitude[0]
            data['longitude'] = cleaned_longitude[0]

        subscription = data['subscription']
        premium_distance= data['premium_distance']
        if subscription == 'Premium' and premium_distance == None:
            raise serializers.ValidationError("invalid premium distance")
        return data
