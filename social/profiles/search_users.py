from django.contrib.auth import get_user_model
from datetime import date
from random import shuffle
from .geo_script import find_distance


# For implementing a swipe logic (user has limited number of swipes in current day) I've decided to save
# ids of the first result_queryset in current day in DB (in the field 'todays_queryset', and the field
# 'today_is' will be filled with the date of getting 'todays_queryset'). So, when user will try
# to get new queryset in the same day, he will get a list of ids from DB, and according to those ids
# will be returned the same result_queryset.
def find_users(user_instance):
    users_in_distance_queryset = []
    result_queryset = []
    result_queryset_ids = []
    swipes = 0
    user_id = user_instance.id
    today_is = date.today()
    users_today_is = user_instance.today_is
    user_gender = user_instance.gender
    user_subscription = user_instance.subscription

    # There we check if we need to get new queryset or get it from DB.
    if users_today_is != today_is or users_today_is is None:

        user_latitude = float(user_instance.latitude)
        user_longitude = float(user_instance.longitude)

        if user_gender == 'M':
            queryset = list(get_user_model().objects.filter(gender='F'))
        else:
            queryset = list(get_user_model().objects.filter(gender='M'))

        if user_subscription == 'Basic':
            allowed_distance = 10
            allowed_swipes = 20
        elif user_subscription == 'VIP':
            allowed_distance = 25
            allowed_swipes = 100
        else:
            allowed_distance = user_instance.premium_distance

        for instance in queryset:
            instance_latitude = float(instance.latitude)
            instance_longitude = float(instance.longitude)
            distance = find_distance(user_latitude, user_longitude, instance_latitude, instance_longitude)
            if instance.id != user_id and distance <= allowed_distance:
                users_in_distance_queryset.append(instance)

        # result_queruset is only a part of users_in_distance_queryset in accordance with allowed_swipes
        # (it means, for example, when len of users_in_distance_queryset is 10 000 items and allowed_swipes
        # is 20, so result_queryset will be first 20 items of users_in_distance_queryset. So, to be shure
        # that result_querysets in different days will be different we need to shuffle users_in_distance_queryset
        # each time we making new result_queryset.
        shuffle(users_in_distance_queryset)

        for i in users_in_distance_queryset:
            if swipes < (allowed_swipes if user_subscription != 'Premium' else len(users_in_distance_queryset)):
                result_queryset.append(i)
                result_queryset_ids.append(i.id)
                swipes += 1

        user_instance.todays_queryset = result_queryset_ids
        user_instance.today_is = today_is
        user_instance.save()
        return result_queryset
    else:
        result_queryset_ids = user_instance.todays_queryset

        for i in result_queryset_ids:
            instance = get_user_model().objects.get(pk=int(i))
            result_queryset.append(instance)
        return result_queryset
