from django.contrib import admin

from .models import Post, TagType

admin.site.register(Post)
admin.site.register(TagType)
