from django.contrib import admin

# Register your models here.

from posts.models import Post


class PostModelAdmin(admin.ModelAdmin):
    list_display = ["title", "publish", "updated"]
    list_filter = ["publish", "updated"]
    list_display_links = ["publish", "updated"]
    search_fields = ["title", "content"]
    list_editable = ["title"]
    class Meta:
        model = Post

admin.site.register(Post, PostModelAdmin)
