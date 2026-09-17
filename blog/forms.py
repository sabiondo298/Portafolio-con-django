from django import forms

from .models import Comment


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["author", "body"]
        labels = {"author": "Tu nombre", "body": "Tu comentario"}
        widgets = {
            "author": forms.TextInput(attrs={"placeholder": "Nombre", "autocomplete": "name"}),
            "body": forms.Textarea(attrs={"placeholder": "Escribi una idea...", "rows": 5}),
        }
