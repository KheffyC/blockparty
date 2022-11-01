from distutils.log import Log
from django.shortcuts import render, redirect
from .models import Post, Profile, Group
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from .forms import ProfileForm, CommentForm




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
      # This is how we log a user in via code
      login(request, user)
      return redirect('my_profile')
    else:
      error_message = 'Invalid sign up - try again'
  # A bad POST or a GET request, so render signup.html with an empty form
  form = UserCreationForm()
  context = {'form': form, 'error_message': error_message}
  return render(request, 'registration/signup.html', context)
  
@login_required
def groups_index(request):
  groups = Group.objects.all()
  
  return render(request, 'groups/index.html', {'groups': groups})

def group(request, group_id):
  group = Group.objects.get(id=group_id)
  
  posts = Post.objects.filter(group_id = group_id).values()
  
  return render(request, 'group/main.html', {'group': group, 'posts': posts})
  
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
def add_comment(request, group_id,  post_id):
  form = CommentForm(request.POST)
  if form.is_valid():
    new_comment = form.save(commit=False)
    new_comment.post_id = post_id
    new_comment.user_id = request.user.id
    new_comment.save()
  return redirect('post_detail', group_id, post_id )

@login_required
def profiles_index(request):
  users = User.objects.all()
  
  return render(request, 'profiles/index.html', {'users': users})
  
@login_required
def profiles_detail(request, user_id):
  user = User.objects.get(pk=user_id)
  
  return render(request, 'profiles/detail.html', {'user': user})

@login_required
def my_profile(request):

  return render(request, 'my_profile.html') 


class ProfileUpdate(LoginRequiredMixin, UpdateView):
  model = Profile
  form_class = ProfileForm

  def form_valid(self, form):
      self.object = form.save(commit=False)
      self.object.save()
      return redirect ('my_profile' )
  
  
class ProfileDelete(LoginRequiredMixin, DeleteView):
  model = User
  success_url = ('/')