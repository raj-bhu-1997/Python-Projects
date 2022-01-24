from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import CreateView
from django.http import HttpResponseRedirect
from .models import Post, Comment, Profile
from .forms import Post_form, Comment_form, Profile_form
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import UpdateView, DeleteView
from django.urls import reverse_lazy
# Create your views here.


class home_page(LoginRequiredMixin, View):
  def get(self, request, *args, **kwargs):
    login_user = request.user
    Post_detail = Post.objects.filter(author__profile__followers__in = [login_user.id]).order_by('-created_on')
    context = {'post_detail': Post_detail,}
    return render(request, 'socialapp/home.html',context)
    
class My_post(View):
  def get(self, request, *args, **kwargs):
    author = request.user
    my_post = Post.objects.filter(author=author)
    context = { 'my_post':my_post }
    return render(request, 'socialapp/my_post.html', context)
 
class Post_create(LoginRequiredMixin, CreateView):
  model = Post
  form_class = Post_form
  template_name = 'socialapp/post_create.html'
  success_url = reverse_lazy('socialapp:welcome')
  def form_valid(self,form):
    new_post = form.save(commit= False)
    new_post.author = self.request.user
    new_post.save()
    return super().form_valid(form)
    
class Postdetail_page(View, LoginRequiredMixin):
  def get(self, request, pk, *args, **kwargs):
    post = Post.objects.get(pk=pk)
    form = Comment_form()
    comments = Comment.objects.filter(post=post).order_by('-created_on')
    context = {'post': post, 'form': form, 'comments': comments}
    
    
    return render(request, 'socialapp/post_detail.html', context)
    
  def post(self, request, pk, *args, **kwargs):
    post = Post.objects.get(pk=pk)
    form = Comment_form(request.POST)
    if form.is_valid():
      new_comment = form.save(commit = False)
      new_comment.author = request.user
      new_comment.post = post
      new_comment.save()
    
    comments = Comment.objects.filter(post=post).order_by('-created_on')
    
    context = {'post': post, 'form': form, 'comments': comments}
    
    
    return render(request, 'socialapp/post_detail.html', context)
    
class Postupdate_page(UpdateView):
  model = Post
  fields = ['text']
  template_name = 'socialapp/update.html'
  success_url = reverse_lazy('socialapp:welcome')
  
class Postdelete_page(DeleteView):
  model = Post
  template_name = 'socialapp/delete.html'
  success_url = reverse_lazy('socialapp:welcome')
  
  
class Profile_page(View):
  def get(self, request, pk,  *args, **kwargs):
    profile = Profile.objects.get(pk=pk)
    form = Profile_form()
    user = profile.user
    # Create Followers 
    following = profile.followers.all()
    
    if len(following) == 0:
      is_following = False
    for follower in following:
      if request.user == follower:
        is_following = True
        break
      else:
        is_following = False
    no_of_follower = len(following)
    context = {'profile':profile, 'form':form, 'user': user, 'no_of_follower': no_of_follower, 'is_following': is_following}
    return render(request, 'socialapp/profile.html', context)
  
class Profileedit_page(LoginRequiredMixin, UpdateView):
  model = Profile
  fields = '__all__'
  template_name = 'socialapp/profile_edit.html'
  success_url = reverse_lazy('socialapp:welcome')

# Create the class for create followers 

class Add_follower(LoginRequiredMixin, View):
  def post(self, request, pk, *args, **kwargs):
    profile = Profile.objects.get(pk= pk)
    profile.followers.add(request.user)
    return redirect ('socialapp:profile', pk= profile.pk)

class Remove_follower(LoginRequiredMixin, View):
  def post(self, request, pk, *args, **kwargs):
    profile = Profile.objects.get(pk=pk)
    profile.followers.remove(request.user)
    return redirect ('socialapp:profile', pk=profile.pk)

# class for Like and Dislike
class Add_like(LoginRequiredMixin, View):
  def post(self, request, pk, *args, **kwargs):
    post = Post.objects.get(pk=pk)
    
    is_dislike = False
    for dislike in post.dislikes.all():
      if dislike == request.user:
        is_dislike = True
        break
    if is_dislike:
      post.dislikes.remove(request.user)
      
    is_like = False
    for like in post.likes.all():
      if like == request.user:
        is_like = True
        break
    if not is_like:
      post.likes.add(request.user)
    else:
      post.likes.remove(request.user)
    next = request.POST.get('next', '/')
    return HttpResponseRedirect(next)
      
class Add_dislike(LoginRequiredMixin, View):
  def post(self, request, pk, *args, **kwargs):
    post = Post.objects.get(pk=pk)
    
    is_like = False
    for like in post.likes.all():
      if like == request.user:
        is_like = True
        break
    if is_like:
      post.likes.remove(request.user)
      
    is_dislike = False
    for dislike in post.dislikes.all():
      if dislike == request.user:
        is_dislike = True
        break
    if not is_dislike:
      post.dislikes.add(request.user)
    else:
      post.dislikes.remove(request.user)
    next = request.POST.get('next', '/')
    return HttpResponseRedirect(next)
    
class Search_user(LoginRequiredMixin, View):
  def get(self, request, *args, **kwargs):
    query = self.request.GET.get('query')
    user_list = Profile.objects.filter(Q(user__username__icontains = query))
    context = { 'user_list': user_list}
    return render (request, 'socialapp/search_user.html', context)
    
class Search_followers(View):
  def get(self, request, pk, *args, **kwargs):
    profile = Profile.objects.get(pk=pk)
    followers = profile.followers.all()
    context = {'profile': profile, 'followers': followers }
    return render(request, 'socialapp/list_follower.html', context)
    
class Comment_like(LoginRequiredMixin, View):
  def post(self, request, pk, *args, **kwargs):
    comment = Comment.objects.get(pk=pk)
    is_dislike = False
    for dislikes in comment.dislike.all():
      if dislikes == request.user:
        is_dislike = True 
        break
    if is_dislike:
      comment.dislike.remove(request.user)
      
    is_like = False
    for likes in comment.like.all():
      if likes == request.user:
        is_like = True 
        break
    if not is_like:
      comment.like.add(request.user)
    else:
      comment.like.remove(request.user)
    next = request.POST.get('next', '/')
    return HttpResponseRedirect(next)
 
class Comment_dislike(LoginRequiredMixin, View):
  def post(self, request, pk, *args, **kwargs):
    comment = Comment.objects.get(pk=pk)
    is_like = False
    for likes in comment.like.all():
      if likes == request.user:
        is_like = True 
        break
    if is_like:
      comment.like.remove(request.user)
    is_dislike = False
    for dislikes in comment.dislike.all():
      if dislikes == request.user:
        is_dislike = True 
        break
    if not is_dislike:
      comment.dislike.add(request.user)
    else:
      comment.dislike.remove(request.user)
    next = request.POST.get('next', '/')
    return HttpResponseRedirect(next)