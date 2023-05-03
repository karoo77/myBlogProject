from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token

from .views import PostList, PostDetail, AuthorList, AuthorDetail, TokenAPIView, MyInfo


urlpatterns = [
    path('posts/', PostList.as_view(), name='post_list'),
    path('posts/<int:pk>/', PostDetail.as_view(), name='post_detail'),
    path('authors/', AuthorList.as_view(), name='author_list'),
    path('authors/<int:pk>/', AuthorDetail.as_view(), name='author_detail'),
    path('api-token-auth/', obtain_auth_token, name='api_token_auth'),
    path('api-token/', TokenAPIView.post, name='api_token'),
    path('myinfo/', MyInfo.get, name='my_info'),
]
