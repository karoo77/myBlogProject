from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from .views import TokenAPI, CurrentUserAPIView, PostList, PostDetail

app_name = 'api'

urlpatterns = [
    path('token/', TokenAPI.as_view(), name='api-token'),
    path('me/', CurrentUserAPIView.as_view(), name='current-user'),
    path('posts/', PostList.as_view(), name='post-list'),
    path('posts/<int:pk>/', PostDetail.as_view(), name='post-detail'),
    path('api-token-auth/', obtain_auth_token, name='api-token-auth'),
]