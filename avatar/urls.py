from django.urls import path

from avatar.views import AddCommunityAvatarView, AddProfileAvatarView, AvatarDetail

urlpatterns = [
    path("community/<int:pk>/avatar/", AddCommunityAvatarView.as_view()),
    path("profile/avatar/", AddProfileAvatarView.as_view()),
    path("avatar/<int:pk>/", AvatarDetail.as_view()),
]
