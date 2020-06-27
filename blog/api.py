from tastypie.resources import ModelResource
from tastypie.constants import ALL
from django.contrib import admin
from django.contrib.auth.models import User
from tastypie import fields

from blog.models import Post, TagType

class UserResource(ModelResource):
	class Meta:
		queryset = User.objects.all()
		resource_name = 'user'
		# excludes = ['email', 'active', 'is_active', 'is_staff', 'is_superuser']
		allowed_methods = ['get']

class PostResource(ModelResource):
	author = fields.ForeignKey(UserResource, 'author')
	class Meta:
		queryset = Post.objects.all()
		resource_name = 'post'
		filtering = {'title' : ALL}

class TagTypeResource(ModelResource):
	class Meta:
		queryset = TagType.objects.all()
		resource_name = 'tagtype'
		filtering = {'title' : ALL}

