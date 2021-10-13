from django.contrib import admin
from django.db import models

from .models import Author, Category, Post, Comment, PostView, NewComment

admin.site.register(Author)
admin.site.register(Category)
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(PostView)

admin.site.register(NewComment)
class NewCommentAdmin(admin.ModelAdmin):
    list_display = ("post", "name", "email", "publish")
    list_filter = ("status", "email", "body")