from django import forms

from .models import Comment, Post, PostMedia


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["title", "author", "body"]
        labels = {
            "title": "Título",
            "author": "Tu nombre",
            "body": "Texto de la entrada",
        }
        widgets = {
            "title": forms.TextInput(attrs={"placeholder": "Título de la entrada"}),
            "author": forms.TextInput(
                attrs={"placeholder": "Nombre del autor", "autocomplete": "name"}
            ),
            "body": forms.Textarea(
                attrs={"placeholder": "Escribí tu entrada...", "rows": 10}
            ),
        }

    def save(self, commit=True):
        post = super().save(commit=False)
        excerpt = " ".join(post.body.split())
        post.excerpt = excerpt if len(excerpt) <= 280 else f"{excerpt[:277]}..."
        if commit:
            post.save()
            self.save_m2m()
        return post


class PostMediaForm(forms.ModelForm):
    class Meta:
        model = PostMedia
        fields = ["file", "caption"]
        labels = {"file": "Archivo multimedia", "caption": "Descripción del archivo"}
        widgets = {
            "file": forms.ClearableFileInput(attrs={"accept": "image/*,video/*,audio/*,.pdf"}),
            "caption": forms.TextInput(attrs={"placeholder": "Descripción (opcional)"}),
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["author", "body"]
        labels = {"author": "Tu nombre", "body": "Tu comentario"}
        widgets = {
            "author": forms.TextInput(
                attrs={"placeholder": "Nombre", "autocomplete": "name", "maxlength": 80}
            ),
            "body": forms.Textarea(
                attrs={
                    "placeholder": "Escribí una idea...",
                    "rows": 5,
                    "maxlength": 1000,
                }
            ),
        }
