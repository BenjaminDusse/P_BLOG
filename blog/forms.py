from django import forms


from .models import Comment


class CommentForm(forms.ModelForm):
    content = forms.CharField(widget=forms.Textarea(attrs={
        'rows': 4,
        'class': 'form-control',
        'placeholder': 'Comment Here...'
    }))

    class Meta:
        model = Comment
        fields = ['content',]

