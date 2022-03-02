from django.urls import path

from hide.views import HideAPublication, HideAComment, HideDetail

urlpatterns = [
    path('publication/<int:pk>/hide/', HideAPublication.as_view()),
    path('comment/<int:pk>/hide/', HideAComment.as_view()),
    path('hide/<int:pk>/', HideDetail.as_view()),
]