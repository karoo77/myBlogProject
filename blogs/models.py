from django.contrib.auth.models import User
from django.db import models

class BaseModel(models.Model):
    is_active = models.BooleanField(default=True)
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Author(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)

    class Meta:
        db_table = 'authors'
        verbose_name = 'Author'
        verbose_name_plural = 'Authors'

    def str(self):
        return self.user.username


class Post(BaseModel):
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    content = models.TextField()
    start_time = models.DateTimeField(blank=True, null=True)
    end_time = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = 'posts'
        verbose_name = 'Post'
        verbose_name_plural = 'Posts'

    def str(self):
        return self.title