from django.urls import path
from . import views

urlpatterns = [
    path('<str:key>/comments', views.CommentListView.as_view(), name='comment_list'),
    path('<str:key>/sub_comment/<int:pk>', views.SubCommentView.as_view(), name='sub_comment'),
    path('<str:key>/like/<int:pk>', views.LikeView.as_view(), name='like'),
    path('<str:key>/dislike/<int:pk>', views.DisLikeView.as_view(), name='dislike'),
]
