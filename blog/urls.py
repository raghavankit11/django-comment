  
from django.urls import path
from .views import (
    PostListView,
    PostListView2,
    PostDetailView,
    PostCreateView,
    PostUpdateView,
    PostDeleteView,
    UserPostListView,

    CommentCreateView,
    CommentDetailView,
    # CommentUpdateView,
    # CommentDeleteView,
    comment_save,
    comment_edit,
    comment_delete,

    subscribe_post,
    unsubscribe_post,
    user_notifications,

    post_tag_save,
    tag_delete,
    #TagPostsView,
    TagPostsTemplateView,

)
from . import views

urlpatterns = [
    path('', PostListView.as_view(), name='blog-home'),
    path('user/<str:username>', UserPostListView.as_view(), name='user-posts'),
    path('user/<str:username>/notifications', user_notifications, name='user-notifications'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('post/new/', PostCreateView.as_view(), name='post-create'),
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post-update'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),

    path('post/<int:post_id>/comments/new', CommentCreateView.as_view(), name='post-comment-create'),
    path('post/<int:post_id>/comments/new2', comment_save, name='add-comment'),

    path('comment/<int:pk>/', CommentDetailView.as_view(), name='comment-detail'),
    path('comment/<int:comment_id>/update', comment_edit, name='edit-comment'),
    #path('comment/<int:pk>/update/', CommentUpdateView.as_view(), name='comment-update'),
    # path('comment/<int:pk>/delete/', CommentDeleteView.as_view(), name='comment-delete'),
    path('comment/<int:comment_id>/delete', comment_delete, name='comment-delete'),

    path('post/<int:post_id>/subscribe', subscribe_post, name='post-subscription'),
    path('post/<int:post_id>/unsubscribe', unsubscribe_post, name='post-unsubscription'),

    path('post/<int:post_id>/tags/new', post_tag_save, name='post-tag-create'),
    path('tags/<int:tag_id>/delete', tag_delete, name='post-tag-delete'),
 #   path('tags/<str:tag_choice>/posts', TagPostsView.as_view(), name='tag-posts'),
    path('tags/<path:tag_choices>/posts', TagPostsTemplateView.as_view(), name='tag-posts'),

    path('poc', PostListView2.as_view(), name='blog-home'),



    path('about/', views.about, name='blog-about'),
]