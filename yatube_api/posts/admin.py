from django.contrib import admin
from .models import Group, Post, Comment, Follow

admin.site.register(Group)
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Follow)
