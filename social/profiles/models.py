from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.postgres.fields import ArrayField


def nameFile(instance, filename):
    return '/'.join(['images', str(instance.user), filename])


class UserProfile(AbstractUser):
    MALE = 'M'
    FEMALE = 'F'
    GENDER_CHOICES = (
        (MALE, 'Male'),
        (FEMALE, 'Female'),
    )

    BASIC = 'Basic'
    VIP = 'VIP'
    PREMIUM = 'Premium'
    SUBSCRIPTION_CHOICES = (
        (BASIC, 'Basic'),
        (VIP, 'VIP'),
        (PREMIUM, 'Premium'),
    )

    id = models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    user_nickname = models.CharField(max_length=30, blank=True)
    gender = models.CharField(
        max_length=2,
        choices=GENDER_CHOICES,
        default=MALE,
    )
    subscription = models.CharField(
        max_length=7,
        choices=SUBSCRIPTION_CHOICES,
        default=BASIC,
    )
    premium_distance = models.IntegerField(null=True)
    my_likes = ArrayField(models.IntegerField(), default=list)
    whom_I_liked = ArrayField(models.IntegerField(), default=list)
    match = ArrayField(models.IntegerField(), default=list)
    conversation = models.URLField(max_length=200)
    latitude = models.CharField(max_length=100, default="53.905284084578696")
    longitude = models.CharField(max_length=100, default="27.559287074770122")
    today_is = models.DateField(null=True)
    todays_queryset = ArrayField(models.CharField(max_length=300), default=list)
    last_updated_coordinates = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        self.conversation = f"http://127.0.0.1:8000/api/v1/userprofile/{self.id}/messages/"
        super(UserProfile, self).save()

    def __str__(self):
        return self.user_nickname

    class Meta:
        ordering = ('id',)


class Image(models.Model):
    user = models.ForeignKey(
        UserProfile,
        related_name='images',
        on_delete=models.CASCADE
    )
    profile_image = models.ImageField(upload_to=nameFile, null=True, blank=True)
    additional_image = models.ImageField(upload_to=nameFile, null=True, blank=True)
