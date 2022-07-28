from django import forms
from django.forms import ModelForm
from .models import Bid, Category, Listing, Comment

style = 'form-control rounded-0 shadow-none'

class LoginForm(forms.Form):
    template_name = 'auctions/snippets/form.html'
    username = forms.CharField(max_length=100, widget=forms.TextInput(attrs={
        'class': style,
        'placeholder': 'Username',
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': style,
        'placeholder': 'Password',
    }))


class RegisterForm(forms.Form):
    template_name = 'auctions/snippets/form.html'
    username = forms.CharField(max_length=100, widget=forms.TextInput(attrs={
        'class': style,
        'placeholder': 'Username',
    }))
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'class': style,
        'placeholder': 'Email',
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': style,
        'placeholder': 'Password',
    }))
    confirmation = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': style,
        'placeholder': 'Confirmation',
    }))


class ListingForm(ModelForm):
    template_name = 'auctions/snippets/form.html'
    category = forms.ModelChoiceField(queryset=Category.objects.all(), initial='', widget=forms.Select(attrs={
        'class': style + " form-select text-start"
    }))
    class Meta:
        model = Listing
        fields = ['title', 'description', 'starting_bid', 'photo', 'category']
        widgets={
            'title': forms.TextInput(attrs={
                'class': style,
                'placeholder': 'Title',
            }),
            'description': forms.Textarea(attrs={
                'class': style,
                'style': 'height: 130px',
                'placeholder': 'Description',
            }),
            'starting_bid': forms.NumberInput(attrs={
                'class': 'form-control rounded-0',
                'placeholder': 'Enter Bid',
            }),
            'photo': forms.ClearableFileInput(attrs={
                'class': 'form-control rounded-0 shadow-none',
                'type': 'file'
            })
        }
   
class PlaceBidForm(ModelForm):
    template_name = 'auctions/snippets/form.html'
    class Meta:
        model = Bid
        fields = ['value']
        labels = {
            'value': "Enter Bid"
        }
        widgets={
            'value': forms.NumberInput(attrs={
                'class': 'form-control rounded-0 shadow-none border-0',
                'placeholder': 'Enter Bid',
            })
        }


class AddCommentForm(ModelForm):
    template_name = 'auctions/snippets/form.html'
    class Meta:
        model = Comment
        fields = ['content']
        labels = {
            'content': 'What are your thoughts?'
        }
        widgets = {
            'content': forms.Textarea(attrs={
                'class': style,
                'style': 'height: 130px'
            })
        }