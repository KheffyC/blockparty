from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from .models import GlobalPost
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm



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
      return redirect('global_index')
    else:
      error_message = 'Invalid sign up - try again'
  # A bad POST or a GET request, so render signup.html with an empty form
  form = UserCreationForm()
  context = {'form': form, 'error_message': error_message}
  return render(request, 'registration/signup.html', context)

@login_required
def global_index(request):
  posts = GlobalPost.objects.all()
  
  return render(request, 'global_posts/index.html', {'posts': posts})
  
def global_post_detail(request, post_id):
  post = GlobalPost.objects.get(id=post_id)
  
  return render(request, 'global_posts/detail.html', {'post': post})
    
class GlobalPostCreate(LoginRequiredMixin ,CreateView):
  model = GlobalPost
  fields = ['content']
  
  def form_valid(self, form):
      form.instance.user = self.request.user
      return super().form_valid(form)
      
class GlobalPostUpdate(LoginRequiredMixin, UpdateView):
  model = GlobalPost
  fields = ['content']
  
  def form_valid(self, form):
      self.object = form.save(commit=False)
      self.object.save()
      return redirect ('global_post_detail', self.object.id)
    
      
    
class GlobalPostDelete(LoginRequiredMixin, DeleteView):
  model = GlobalPost
  success_url = '/global/'