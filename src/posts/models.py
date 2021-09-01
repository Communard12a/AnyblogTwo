from django.db import models
from django.contrib.auth import get_user_model # default model user


User = get_user_model() # почему с большой буквы, что это? Our user is equal to default model user

class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField()

    def __str__(self):
        return self.user.username # почему не просто user, a user.username?

class Category(models.Model):
    title = models.CharField(max_length=20)

    def __str__(self):
        return self.title

class Post(models.Model):
    title = models.CharField(max_length=100)
    overview = models.TextField()
    temestamp = models.DateTimeField(auto_now_add=True)
    comment_count = models.IntegerField(default=0)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    thumbnail = models.ImageField()
    categories = models.ManyToManyField(Category) #сразу мн.число у переменной; у многих постов могут быть много категорий
    featured = models.BooleanField() # те посты, которые будут показаны на домашней странице

    def __str__(self):
        return self.title