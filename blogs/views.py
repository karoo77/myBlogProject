from django.contrib.auth import get_user_model
from django.db.models import Q
from rest_framework import generics, status, permissions, filters
from rest_framework.decorators import api_view
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.throttling import AnonRateThrottle
from rest_framework.views import APIView

from .models import Author, Post
from .serializers import PostSerializer, AuthorSerializer, TokenSerializer


class PostList(generics.ListCreateAPIView):
    """
    List all posts, or create a new post.
    """
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    filterset_fields = ['is_active', 'author']
    ordering_fields = ['create_time', 'update_time']
    ordering = ['-create_time']
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user.author)

    def get_queryset(self):
        queryset = super().get_queryset()
        if not self.request.user.is_authenticated:
            queryset = queryset.filter(is_active=True)
        return queryset


class PostDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete a post instance.
    """
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_update(self, serializer):
        serializer.save(author=self.request.user.author)


class AuthorList(generics.ListCreateAPIView):
    """
    List all authors, or create a new author.
    """
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = [permissions.IsAdminUser]


class AuthorDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete an author instance.
    """
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = [permissions.IsAdminUser]


class TokenAPIView(APIView):
    """
    Get the auth token for a user.
    """
    serializer_class = TokenSerializer

    @staticmethod
    @api_view(['POST'])
    def post(request):
        serializer = TokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        User = get_user_model()
        user = User.objects.filter(Q(username=serializer.validated_data['username']) | Q(email=serializer.validated_data['username'])).first()
        if user and user.check_password(serializer.validated_data['password']):
            token = user.auth_token.key
            return Response({'token': token})
        return Response({'error': 'Invalid Credentials'}, status=status.HTTP_401_UNAUTHORIZED)


class MyInfo(APIView):
    """
    Display the current logged in user info.
    """
    permission_classes = [permissions.IsAuthenticated]

    @staticmethod
    @api_view(['GET'])
    def get(request):
        author_serializer = AuthorSerializer(request.user.author)
        return Response({'user': request.user.username, 'author': author_serializer.data})


class PostsPagination(PageNumberPagination):
    """
    Pagination class to limit the number of posts displayed.
    """
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


class LimitedAnonRateThrottle(AnonRateThrottle):
    THROTTLE_RATES = {
        'anon': '10/minute',
    }