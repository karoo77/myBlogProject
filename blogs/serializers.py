from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Author, Post


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ('id', 'user', 'avatar', 'bio')


class UserSerializer(serializers.ModelSerializer):
    author = AuthorSerializer()

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'author']





class PostSerializer(serializers.ModelSerializer):
    author = AuthorSerializer(read_only=True)

    class Meta:
        model = Post
        fields = 'all'

    def create(self, validated_data):
        author = Author.objects.get(user=self.context['request'].user)
        validated_data['author'] = author
        return super().create(validated_data)

    def update(self, instance, validated_data):
        author = Author.objects.get(user=self.context['request'].user)
        if instance.author == author:
            return super().update(instance, validated_data)
        else:
            raise serializers.ValidationError("You don't have permission to edit this post.")