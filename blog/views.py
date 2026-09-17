from django.shortcuts import get_object_or_404, redirect, render

from .forms import CommentForm
from .models import Post


def post_list(request):
    return render(request, "blog/post_list.html", {"posts": Post.objects.all()})


def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug)
    form = CommentForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        comment = form.save(commit=False)
        comment.post = post
        comment.save()
        return redirect(f"{post.get_absolute_url()}#comments")
    return render(request, "blog/post_detail.html", {"post": post, "form": form})
