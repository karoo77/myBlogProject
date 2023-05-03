# from rest_framework import serializers
# from django.contrib.auth.models import User
# from .models import Author, Post
#
#
# class AuthorSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Author
#         fields = ('id', 'user', 'avatar', 'bio')
#
#
# class UserSerializer(serializers.ModelSerializer):
#     author = AuthorSerializer()
#
#     class Meta:
#         model = User
#         fields = ['id', 'username', 'email', 'author']
#
#
#
#
#
# class PostSerializer(serializers.ModelSerializer):
#     author = AuthorSerializer(read_only=True)
#
#     class Meta:
#         model = Post
#         fields = ['title', 'content', 'is_active', 'create_time', 'update_time', 'author']
#
#     def create(self, validated_data):
#         author = Author.objects.get(user=self.context['request'].user)
#         validated_data['author'] = author
#         return super().create(validated_data)
#
#     def update(self, instance, validated_data):
#         author = Author.objects.get(user=self.context['request'].user)
#         if instance.author == author:
#             return super().update(instance, validated_data)
#         else:
#             raise serializers.ValidationError("You don't have permission to edit this post.")
#
# #-------------------------------------
from django.contrib.auth import authenticate
from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Author, Post

class TokenSerializer(serializers.Serializer):
    """
    Serializer for getting an authentication token.
    """
    username = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=128, write_only=True)

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')

        if username and password:
            user = authenticate(request=self.context.get('request'), username=username, password=password)
            if not user:
                msg = 'Unable to log in with provided credentials.'
                raise serializers.ValidationError(msg, code='authorization')
        else:
            msg = 'Must include "username" and "password".'
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = user
        return attrs


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class AuthorSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    avatar = serializers.ImageField(max_length=None, use_url=True, required=False)

    class Meta:
        model = Author
        fields = '__all__'

class PostSerializer(serializers.ModelSerializer):
    author = AuthorSerializer(read_only=True)

    class Meta:
        model = Post
        fields = '__all__'