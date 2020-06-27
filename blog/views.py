from datetime import datetime

from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.utils import timezone
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
    TemplateView
)
from .models import Post, Comment, Subscription, Notification, Tag, TagType
from .filters import remove_hash
remove_hash
def string_to_bool(str):
    return str and str.lower() in ['true', '1', 'yes']

# def home(request):
#     context = {
#         'posts': Post.objects.all()
#     }
#     return render(request, 'blog/home.html', context)


class PostListView(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'blog/home.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 5

    def get_queryset(self):
        user = self.request.user
        posts = Post.objects.order_by('-date_posted').all()
        for p in posts:
            p.is_user_subscribed = p.subscriptions.filter(user__id__exact=user.id).exists()
            p.is_user_subscribed_not = not p.is_user_subscribed

        return posts


class PostListView2(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'blog/home2.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 5

    def get_queryset(self):
        user = self.request.user
        posts = Post.objects.order_by('-date_posted').all()
        for p in posts:
            p.is_user_subscribed = p.subscriptions.filter(user__id__exact=user.id).exists()
            p.is_user_subscribed_not = not p.is_user_subscribed

        return posts


class UserPostListView(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'blog/user_posts.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    paginate_by = 5

    def get_queryset(self):
        user = self.request.user
        posts = Post.objects.filter(author=user).order_by('-date_posted').all()
        for p in posts:
            p.is_user_subscribed = p.subscriptions.filter(user__id__exact=user.id).exists()
            p.is_user_subscribed_not = not p.is_user_subscribed

        return posts


# region Post - Views


class PostDetailView(LoginRequiredMixin, DetailView):
    model = Post

    def get_object(self, queryset=None):
        obj = super(PostDetailView, self).get_object()
        user = self.request.user
        obj.is_user_subscribed = obj.subscriptions.filter(user__id__exact=user.id).exists()
        obj.is_user_subscribed_not = not obj.is_user_subscribed
        return obj


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content', 'anonymous']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content', 'anonymous']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


# endregion

# region Comment - Views
class CommentDetailView(DetailView):
    model = Comment
    # ordering = ['-date_posted']
    template_name = 'blog/comment_detail.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        is_editable = string_to_bool(self.request.GET.get('editable'))
        commentId = self.kwargs['pk']
        obj = Comment.objects.get(id=commentId)

        return {'comment':obj, 'editable': is_editable, 'post':obj.post}

class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    fields = ['content', 'anonymous']
    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.post = Post.objects.get(pk=self.kwargs.get('post_id'))
        return super().form_valid(form)


class CommentUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Comment
    fields = ['content', 'anonymous']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


# class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
#     model = Comment
#     success_url = '/'
#
#     def test_func(self):
#         post = self.get_object()
#         if self.request.user == post.author:
#             return True
#         return False


# endregion


def about(request):
    return render(request, 'blog/about.html', {'title': 'About'})


# region - Subscription

def subscribe_post(request, post_id):
    user = request.user
    post = Post.objects.get(pk=post_id)

    is_already_subscribed = Subscription.objects.filter(user__id__exact=user.id, post__id__exact=post.id).exists()
    if not is_already_subscribed:
        s = Subscription(user=user, post=post)  # Creating Like Object
        s.save()  # saving it to store in database
        is_saved = Subscription.objects.filter(user__id__exact=user.id, post__id__exact=post.id).exists()
    else:
        is_saved = True

    data = {
        'result': is_saved
    }
    return JsonResponse(data)


def unsubscribe_post(request, post_id):
    user = request.user
    post = Post.objects.get(pk=post_id)

    ss = Subscription.objects.filter(user__id__exact=user.id, post__id__exact=post.id)
    ss.delete()
    is_deleted = not Subscription.objects.filter(user__id__exact=user.id, post__id__exact=post.id).exists()

    data = {
        'result': is_deleted
    }
    return JsonResponse(data)
# endregion
#
# def user_notifications_get(request, username):
#     user = request.user
#
#     nn = Notification.objects.filter(subscription__user=user)
#
#     result = []
#     for n in nn:
#         user_notification = {'comment_id': n.comment.id,
#                              'comment_text': n.comment.content,
#                              'username': n.comment.author.username,
#                              'post_title': n.comment.post.title,
#                              'posted_on': n.comment.date_posted}
#         result.append(user_notification)
#
#     data = {'result': result}
#     final = JsonResponse(data, safe=False)
#
#     return final


# region - Tags



def post_tag_save(request, post_id):
    user = request.user
    post = Post.objects.get(pk=post_id)
    choice = request.POST.get('data_item[choice]')
    tag_type = TagType.objects.get(name=choice)

    is_already_tagged = Tag.objects.filter(post__id__exact=post.id, type__name__exact=choice).exists()
    if not is_already_tagged:
        t = Tag(type=tag_type, post=post)  # Creating Like Object
        t.save()  # saving it to store in database
        is_saved = Tag.objects.filter(post__id__exact=post.id, type__name__exact=choice).exists()
    else:
        is_saved = True

    data = {
        'result': is_saved
    }
    return JsonResponse(data)


def tag_delete(request, tag_id):
    t = Tag.objects.get(pk=tag_id)
    t.delete()
    is_deleted = not Tag.objects.filter(pk=tag_id).exists()

    data = {
        'result': is_deleted
    }
    return JsonResponse(data)


class TagPostsTemplateView(LoginRequiredMixin, TemplateView):
    template_name = 'blog/tag_posts.html'  # <app>/<model>_<viewtype>.html

    def get_context_data(self, *, object_list=None, **kwargs):
        choices = self.kwargs['tag_choices']

        choices = choices.split('/')

        posts = Post.objects.all() # 1000
        for choice in choices:  # Financial, #Political
            tags = Tag.objects.filter(type__name__exact='#' + choice).all()
            posts = posts.filter(tags__in=[tt.id for tt in tags]).order_by('-date_posted').all()

        remaining_choices = set()
        for p in posts:
            p.is_user_subscribed = p.subscriptions.filter(user__id__exact=self.request.user.id).exists()
            p.is_user_subscribed_not = not p.is_user_subscribed
            for t in p.tags.all():
                if remove_hash(t.type.name) not in choices:
                    remaining_choices.add(t.type.name)
            #remaining_choices.append(list(map(lambda t: t.choice if remove_hash(t.choice) in choices else None, p.tags.all())))

        page_size = 2
        is_paginated = posts.count() > page_size
        paginator = Paginator(posts, page_size)  # Show 25 contacts per page

        page = 1
        try:
            page = self.request.GET['page']
        except:
            page = 1

        try:
            posts = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            posts = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            posts = paginator.page(paginator.num_pages)

        return {'filtered_choices': choices,
                'remaining_choices': remaining_choices,
                'posts': posts,
                'page_obj': posts,
                'is_paginated': is_paginated}

# endregion



def comment_save(request, post_id):
    user = request.user
    post = Post.objects.get(pk=post_id)
    content = request.POST.get('data_item[content]')
    anonymous = string_to_bool(request.POST.get('data_item[anonymous]'))

    s = Comment(author=user, post=post, content=content, anonymous = anonymous )           # Creating Like Object
    s.save()  # saving it to store in database
    is_saved = Comment.objects.filter(author_id__exact=user.id, post_id__exact=post.id,
                         content__exact=content, anonymous__exact=anonymous).exists()

    data = {
             'result':is_saved,
             'comment':{'id':s.id, 'anonymous':s.anonymous,
                        'author':{'profile':{'image': {'url': s.author.profile.image.url}},
                                  'username': s.author.username},
                        'date_posted':s.date_posted,
                        'content':s.content
                        }
           }

    return JsonResponse(data)


def comment_edit(request, comment_id):
    content = request.POST.get('data_item[content]')
    anonymous = string_to_bool(request.POST.get('data_item[anonymous]'))

    s = Comment.objects.get(id=comment_id)
    prev_anonymous = s.anonymous
    author_name = s.author.username
    author_profile_pic = s.author.profile.image.url

    s.content = content
    s.anonymous = anonymous
    s.date_posted = timezone.now()
    s.save()

    data = {
             'result': True,
             'prev_anonymous': prev_anonymous,
             'author_name': author_name,
             'author_profile_pic': author_profile_pic,
             'date_posted': datetime.strftime(s.date_posted, '%Y-%m-%dT%H:%M')
           }

    return JsonResponse(data)

def comment_delete(request, comment_id):

    c = Comment.objects.get(id=comment_id)
    c.delete()

    data = { 'result': True }

    return JsonResponse(data)

def user_notifications(request, username):
    user = request.user

    nn = Notification.objects.filter(subscription__user=user)
    context = {
        'notifications': nn
    }
    return render(request, 'blog/user_notifications.html', context)




