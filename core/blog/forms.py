from django.forms import ModelForm, TextInput, Textarea

from blog.models import Profile, BlogPost


class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = ('bio', 'facebook', 'instagram', 'linkedin', 'image', )


class BlogPostForm(ModelForm):
    class Meta:
        model = BlogPost
        fields = ('title', 'slug', 'content', 'image')
        widgets = {
            'title': TextInput(attrs={'class': 'form-control',
                                            'placeholder': 'Title of the Blog'}),
            'slug': TextInput(attrs={'class': 'form-control',
                                           'placeholder': 'Copy the title with no space and a hyphen in between'}),
            'content': Textarea(attrs={'class': 'form-control',
                                             'placeholder': 'Content of the Blog'}),
        }
