from tinymce import HTMLField
from django.db import models
from django.contrib.auth import get_user_model # default model user
from django.urls import reverse 
from django.utils import timezone

User = get_user_model() # почему с большой буквы, что это? Our user is equal to default model user
class PostView(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey('Post', on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    content = models.TextField()
    post = models.ForeignKey('Post', related_name='comments', on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username

class NewComment(models.Model):
    post = models.ForeignKey('Post', related_name='new_comments', on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    email = models.EmailField()
    body = models.TextField()
    publish = models.DateTimeField(auto_now_add=True)
    #status = models.BooleanField(default=True)

    class Meta:
        ordering = ("-publish",)

    def __str__(self):
        return f"by {self.name} to post: '{self.post}'"

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
    timestamp = models.DateTimeField(auto_now_add=True)
    content = HTMLField()
    comment_count = models.IntegerField(default=0)
    publish = models.DateTimeField(default=timezone.now)
    views_count = models.IntegerField(default=0) 
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    thumbnail = models.ImageField()
    categories = models.ManyToManyField(Category) #сразу мн.число у переменной; у многих постов могут быть много категорий
    featured = models.BooleanField() # те посты, которые будут показаны на домашней странице
    previous_post = models.ForeignKey('self', related_name='previous', on_delete=models.SET_NULL, blank=True, null=True )
    next_post = models.ForeignKey('self', related_name='next', on_delete=models.SET_NULL, blank=True, null=True )

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={
            'id': self.id
        })

    def get_update_url(self):
        return reverse('post-update', kwargs={
            'id': self.id
        })

    def get_delete_url(self):
        return reverse('post-delete', kwargs={
            'id': self.id
        })

    @property
    def get_comments(self):
        return self.comments.all().order_by('-timestamp')

    @property
    def view_count(self):
        return Comment.objects.filter(post=self).count()  

    @property
    def view_count(self):
        return PostView.objects.filter(post=self).count()   



