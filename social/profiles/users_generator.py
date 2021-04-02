import random

MALE_USER_NAMES = ('Ivan', 'Petr', 'Dzianis', 'Ihar', 'Dzima', 'Kastus', 'Mikita', 'Mikola', 'Nick', 'Mike')
FEMALE_USER_NAMES = ('Marja', 'Paulina', 'Tania', 'Katsiaryna', 'Nina', 'Volga', 'Tasia', 'Ylia', 'Polia', 'Liza')
SUBSCRIPTION_CHOICES = ('Basic', 'VIP', 'Premium')
LATITUDES = (53.83071813303805, 53.97359072296476)
LONGITUDES = (27.399722783103154, 27.697288329096935)


def generate_nickname(seq):
    name = random.choice(seq)
    appendix = str(int(random.random() * 10000000000000))
    return name + appendix


def create_user(seq):
    user_nickname = generate_nickname(seq)
    if seq == MALE_USER_NAMES:
        gender = 'M'
    else:
        gender = 'F'
    email = user_nickname + '@gmail.com'
    subscription = random.choice(SUBSCRIPTION_CHOICES)
    if subscription == 'Premium':
        premium_distance = random.randint(50, 200)
    else:
        premium_distance = None
    latitude = random.uniform(LATITUDES[0], LATITUDES[1])
    longitude = random.uniform(LONGITUDES[0], LONGITUDES[1])
    user = {'username': user_nickname, 'user_nickname': user_nickname, 'email': email, 'gender': gender,
            'subscription': subscription, 'premium_distance': premium_distance, 'latitude': latitude,
            'longitude': longitude}
    return user
