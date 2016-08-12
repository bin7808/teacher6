from django import forms
from blog.models import Comment


class CommentModelForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['message', 'jjal']


class CommentForm(forms.Form):
    message = forms.CharField(widget=forms.Textarea)
    author = forms.CharField()

    def __init__(self, *args, **kwargs):
        self.instance = kwargs.pop('instance', None)
        super(CommentForm, self).__init__(*args, **kwargs)
        if self.instance:
            self.fields['message'].initial = self.instance.message
            self.fields['author'].initial = self.instance.author
        else:
            self.instance = Comment()

    def save(self, commit=True):
        self.instance.message = self.cleaned_data['message']
        self.instance.author = self.cleaned_data['author']
        if commit:
            self.instance.save()
        return self.instance
