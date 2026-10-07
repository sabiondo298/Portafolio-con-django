from django.core.paginator import Paginator
from django.db.models import Prefetch
from django.shortcuts import get_object_or_404, redirect, render

from .forms import CommentForm
from .models import Post, PostMedia


def post_list(request):
    posts = Post.objects.prefetch_related(
        Prefetch("media", queryset=PostMedia.objects.order_by("pk"), to_attr="media_items")
    )
    page_obj = Paginator(posts, 6).get_page(request.GET.get("page"))
    return render(request, "blog/post_list.html", {"page_obj": page_obj})


def post_detail(request, slug):
    post = get_object_or_404(Post.objects.prefetch_related("media", "comments"), slug=slug)
    form = CommentForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        comment = form.save(commit=False)
        comment.post = post
        comment.save()
        return redirect(f"{post.get_absolute_url()}#comments")
    return render(request, "blog/post_detail.html", {"post": post, "form": form})
