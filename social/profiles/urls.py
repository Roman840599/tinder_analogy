from rest_framework import routers
from django.urls import path
from profiles.views import profile_view, users_view, root_view
from communication.views import messages_view, dialogs_view


router = routers.SimpleRouter()
router.register(r'userprofile', users_view.UsersViewSet, basename='userprofile')
router.register(r'dialog', dialogs_view.DialogViewSet, basename='dialog')

urlpatterns = [
    path('', root_view.ApiRoot.as_view()),
    path('profile/', profile_view.ProfileDetailView.as_view(), name=profile_view.ProfileDetailView.name),
    path('userprofile/<int:pk>/messages/', messages_view.MessageList.as_view(), name=messages_view.MessageList.name),
]

urlpatterns += router.urls
