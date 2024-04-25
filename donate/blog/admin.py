from django.contrib import admin
from .models import *

@admin.register(blogModel)
class blogAdmin(admin.ModelAdmin):
    list_display = ['title' , 'status'] 
    search_fields = ['title' , 'body']
    list_filter = ['status']
    prepopulated_fields = {'slug':('title',)}


@admin.register(ReplyComment)
class ReplyCommentAdmin(admin.ModelAdmin):
    list_display = ['comment' , 'replyText' , 'isActive' ]   
    raw_id_fields = ['comment']


class ReplyInLine(admin.TabularInline):
    model = ReplyComment
    extra = 0
    

    
@admin.register(commentModel)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['body' , 'blog' , 'name' ]    
    list_filter = ['recomment']
    #readonly_fields = ['blog' , 'user' , 'name' ,'date']


