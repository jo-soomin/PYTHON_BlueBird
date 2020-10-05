from django.contrib import admin
from .models import Post, Comment
# Register your models here.

@admin.register(Post)

class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'title','writer','password','tent','key','content','pub_date')
    list_filter = ('mod_date',)
    search_fields = ('title','content','tent','writer')

@admin.register(Comment)

class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'comment_writer', 'comment_contents', 'comment_date')
    list_filter = ('comment_date',)
    search_fields = ('comment_writer', 'comment_contents', 'comment_date')

