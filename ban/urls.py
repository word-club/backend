from django.urls import path

from ban.views import BanAModelItemView

urlpatterns = [
    path("ban/", BanAModelItemView.as_view()),
    path("ban/<int:pk>/", BanAModelItemView.as_view()),
]
