from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('about/', views.about, name='about'),
    path('accounts/signup/', views.signup, name='signup'),
    path('global/', views.global_index, name='global_index'),
    path('global/create/', views.GlobalPostCreate.as_view(), name='global_post_create'),
]
