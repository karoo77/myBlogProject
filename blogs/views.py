from django.contrib.auth import authenticate, login
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from rest_framework.views import APIView
from rest_framework import authentication, generics, permissions, throttling
from rest_framework.response import Response

from .models import Post
from .serializers import PostSerializer, AuthorSerializer

# Api Token
#------------------------------------
class TokenAPI(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(request, username=username, password=password)
        if user is None:
            return Response({'error': 'Invalid username or password.'}, status=400)

        login(request, user)

        token_generator = default_token_generator
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = token_generator.make_token(user)

        return Response({'token': f'{uid}-{token}'}, status=200)

#------------------------------------

# Api me
#------------------------------------
class CurrentUserAPIView(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, format=None):
        author = request.user.author
        serializer = AuthorSerializer(author)
        return Response(serializer.data)

#------------------------------------

# Api posts
#------------------------------------


class PostThrottle(throttling.AnonRateThrottle):
    rate = '10/minute'

class PostList(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.AllowAny]
    throttle_classes = [PostThrottle]

class PostDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.AllowAny]

    def perform_update(self, serializer):
        serializer.save(author=self.request.user.author)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user.author)

    def get_object(self):
        obj = super().get_object()
        if not self.request.user.is_authenticated or not self.request.user.author == obj.author:
            self.permission_denied(self.request)
        return obj

#------------------------------------