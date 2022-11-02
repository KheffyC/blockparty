from django.urls import path
from .views import *
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', views.home, name="home"),
    path('about/', views.about, name='about'),
    path('accounts/signup/', views.signup, name='signup'),
    path('groups/', views.groups_index, name='groups_index'),
    path('group/<int:group_id>/', views.group, name='group'),
    path('group/<int:group_id>/posts/create', views.PostCreate.as_view(), name='post_create'),
    path('group/<int:group_id>/posts/<int:post_id>/', views.post_detail, name='post_detail'),
    path('group/<int:group_id>/posts/<int:pk>/update', views.PostUpdate.as_view(), name='post_update'),
    path('group/<int:group_id>/posts/<int:pk>/delete', views.PostDelete.as_view(), name='post_delete'),
    path('groups/<int:group_id>/posts/<int:post_id>/add_comments/', views.add_comment, name='add_comment'),
    path('groups/<int:group_id>/posts/<int:post_id>/<int:comment_id>/remove_comment/', views.remove_comment, name='remove_comment'),
    path('groups/<int:group_id>/posts/<int:post_id>/like_post', views.like_post, name='like_post'),
    path('profiles/', views.profiles_index, name='profiles_index'),
    path('profiles/<int:user_id>/', views.profiles_detail, name='profiles_detail'),
    path('profiles/<int:pk>/update/', views.ProfileUpdate.as_view(), name='profile_update'),
    path('profiles/<int:pk>/delete/', views.ProfileDelete.as_view(), name='profile_delete')
]
