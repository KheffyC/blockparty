from django.forms import ModelForm
from .models import Profile, Comment
from django.contrib.auth.models import User



class UserForm(ModelForm):
    class Meta:
        model = User
        fields =('username',)
class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = ('state', 'bio', 'birth_date', 'profileimg')

class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['content']