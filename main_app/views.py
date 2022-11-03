from django.shortcuts import render, redirect
from .models import Post, Profile, Group, LikePost, Comment
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from .forms import ProfileForm, CommentForm
from django.http import HttpResponse




# Create your views here.
def home(request):
  return render(request, 'home.html')


def about(request):
  return render(request, 'about.html')


def signup(request):
  error_message = ''
  if request.method == 'POST':
    # This is how to create a 'user' form object
    # that includes the data from the browser
    form = UserCreationForm(request.POST)
    if form.is_valid():
      # This will add the user to the database
      user = form.save()
      # Create Global Group if it doesnt exist
      if not Group.objects.filter(name="Global"):
        Group.objects.create(name='Global')
        user.profile.save()
      else:
        group = Group.objects.get(name="Global")
        user.profile.groups.add(group)
        user.profile.save()
      # This is how we log a user in via code
      login(request, user)
      return redirect('profiles_detail', user.id)
    else:
      error_message = 'Invalid sign up - try again'
  # A bad POST or a GET request, so render signup.html with an empty form
  form = UserCreationForm()
  context = {'form': form, 'error_message': error_message}
  return render(request, 'registration/signup.html', context)
  
  
@login_required
def groups_index(request):
  user = User.objects.get(id=request.user.id)
  groups = user.profile.groups.all()
  
  return render(request, 'groups/index.html', {'groups': groups})

@login_required
def group(request, group_id):
  group = Group.objects.get(id=group_id)
  
  posts = Post.objects.filter(group_id = group_id)
  
  return render(request, 'group/main.html', {'group': group, 'posts': posts})
 
@login_required  
def post_detail(request, group_id, post_id):
  post = Post.objects.get(id=post_id)
  group = Group.objects.get(id=group_id)
  
  comment_form = CommentForm()
  return render(request, 'group/post.html', {'post': post, "comment_form": comment_form})
  
    
class PostCreate(LoginRequiredMixin ,CreateView):
  model = Post
  fields = ['content']
 
  
  def form_valid(self, form):
    form.instance.user = self.request.user
    group = Group.objects.get(id=self.kwargs['group_id'])
    form.instance.group = group
    return super().form_valid(form)
 
      
class PostUpdate(LoginRequiredMixin, UpdateView):
  model = Post
  fields = ['content']

  def form_valid(self, form):
      self.object = form.save(commit=False)
      self.object.save()
      return redirect ('post_detail', self.object.group.id, self.object.id)
    
       
class PostDelete(LoginRequiredMixin, DeleteView):
  model = Post
  def get_success_url(self): 
    return reverse_lazy( 'group', kwargs = {'group_id': self.kwargs['group_id']},)
 
@login_required
def like_post(request, group_id, post_id):
  username = request.user.username
  
  post =  Post.objects.get(id = post_id)
  
  like_filter = LikePost.objects.filter(post_id=post_id, username=username).first()
  
  if like_filter == None:
    new_like = LikePost.objects.create(post_id=post_id, username=username)
    new_like.save()
    post.no_of_likes = post.no_of_likes + 1
    post.save()
    return redirect('post_detail', group_id, post_id)
  else:
    like_filter.delete()
    post.no_of_likes = post.no_of_likes - 1
    post.save()
    return redirect('post_detail', group_id, post_id)
    
     
@login_required
def add_comment(request, group_id,  post_id):
  form = CommentForm(request.POST)
  if form.is_valid():
    new_comment = form.save(commit=False)
    new_comment.post_id = post_id
    new_comment.user_id = request.user.id
    new_comment.save()
  return redirect('post_detail', group_id, post_id)


@login_required
def remove_comment(request, group_id,  post_id, comment_id):
  comment = Comment.objects.get(id=comment_id)
  if request.user.id == comment.user.id:
    comment.delete()
  return redirect('post_detail', group_id, post_id)


@login_required
def profiles_index(request):
  users = User.objects.exclude(id=request.user.id)
  logged_in_user = User.objects.get(id=request.user.id)
  
  return render(request, 'profiles/index.html', {'users': users, 'logged_in_user': logged_in_user})
  
  
@login_required
def profiles_detail(request, user_id):
  user_object = User.objects.get(pk=user_id)
  user_profile = Profile.objects.get(user=request.user.id)
  user_posts = Post.objects.filter(user=user_id)
  
  context = {
    'user': user_object,
    'user_posts': user_posts,
    'user_id': user_id,
    'user_profile': user_profile,
    'user_posts_length': len(user_posts)
  }
  
  return render(request, 'profiles/detail.html', context)


@login_required
def profile_image_view(request):
  
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES)
  
        if form.is_valid():
            form.save()
            return redirect('success')
    else:
        form = ProfileForm()
    return render(request, 'profiles.html', {'form' : form})
  
@login_required 
def success(request):
  return HttpResponse('successfully uploaded')


class ProfileUpdate(LoginRequiredMixin, UpdateView):
  model = Profile
  form_class = ProfileForm

  def form_valid(self, form):
      self.object = form.save(commit=False)
      if not Group.objects.filter(name=self.object.state):
        self.object.groups.clear()
        self.object.groups.add(Group.objects.get(name='Global'))
        new_group = Group.objects.create(name=self.object.state)
        self.object.groups.add(new_group)
      else:
        self.object.groups.clear()
        self.object.groups.add(Group.objects.get(name='Global'))
        self.object.groups.add(Group.objects.get(name=self.object.state))
      self.object.save()
      return redirect ('profiles_detail', self.object.id )
  
class ProfileDelete(LoginRequiredMixin, DeleteView):
  model = User
  success_url = ('/')