from comments.models import Comment
from django.contrib import admin


class CommentAdmin(admin.ModelAdmin):
    list_display = ("author", "content", "created_at")


admin.site.register(Comment, CommentAdmin)
