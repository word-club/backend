from django.urls import path

from block.views import BlockACommunity, BlockAUser, BlockDetail

urlpatterns = [
    path("user/<int:pk>/block/", BlockACommunity.as_view()),
    path("community/<int:pk>/block/", BlockAUser.as_view()),
    path("block/<int:pk>/", BlockDetail.as_view()),
]
