from django.urls import path

from . import views

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
    
    # path('global/<int:post_id>/', views.global_post_detail, name='global_post_detail'), #this is equal to my_profile
    # path('global/create/', views.GlobalPostCreate.as_view(), name='global_post_create'),
    # path('global/<int:pk>/update/', views.GlobalPostUpdate.as_view(), name='global_post_update'), # this one 
    # path('global/<int:pk>/delete/', views.GlobalPostDelete.as_view(), name='global_post_delete'),
    # path('global/<int:post_id>/add_comment/', views.add_comment, name='add_comment'),
    path('profiles/', views.profiles_index, name='profiles_index'),
    path('profiles/<int:user_id>/', views.profiles_detail, name='profiles_detail'),
    path('my_profile/', views.my_profile, name='my_profile'),
    path('my_profile/<int:pk>/update/', views.ProfileUpdate.as_view(), name='profile_update'),
    path('my_profile/<int:pk>/delete/', views.ProfileDelete.as_view(), name='profile_delete')
]
