# contiene las vistas para listar, leer y gestionar entradas del blog.
from django.contrib.auth.decorators import login_required, permission_required, user_passes_test
from django.core.paginator import Paginator
from django.db.models import Prefetch
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect, render

from .forms import CommentForm, PostForm, PostMediaForm
from .models import Comment, Post, PostMedia


# lista las entradas del blog con paginación e información de media.
def post_list(request):
    posts = Post.objects.prefetch_related(
        Prefetch("media", queryset=PostMedia.objects.order_by("pk"), to_attr="media_items")
    )
    page_obj = Paginator(posts, 6).get_page(request.GET.get("page"))
    return render(request, "blog/post_list.html", {"page_obj": page_obj})


# muestra una entrada y permite publicar comentarios desde la misma vista.
def post_detail(request, slug):
    post = get_object_or_404(Post.objects.prefetch_related("media", "comments"), slug=slug)
    form = CommentForm(request.POST if request.method == "POST" else None)
    if request.method == "POST" and form.is_valid():
        comment = form.save(commit=False)
        comment.post = post
        comment.save()
        return redirect(f"{post.get_absolute_url()}#comments")
    return render(request, "blog/post_detail.html", {"post": post, "form": form})


# elimina una entrada y todo su contenido asociado si el usuario tiene permisos.
@login_required(login_url="admin:login")
@permission_required("blog.delete_post", login_url="admin:login", raise_exception=True)
def post_delete(request, slug):
    post = get_object_or_404(Post, slug=slug)
    if request.method == "POST":
        post.delete()
        return redirect("blog:post_list")
    return redirect(post.get_absolute_url())


# elimina un comentario concreto de una entrada y vuelve a la vista del detalle.
@login_required(login_url="admin:login")
@permission_required("blog.delete_comment", login_url="admin:login", raise_exception=True)
def comment_delete(request, slug, comment_id):
    post = get_object_or_404(Post, slug=slug)
    comment = get_object_or_404(Comment, pk=comment_id, post=post)
    if request.method == "POST":
        comment.delete()
        return redirect(f"{post.get_absolute_url()}#comments")
    return redirect(f"{post.get_absolute_url()}#comments")


# permite crear una nueva entrada del blog solo para superusuarios.
@user_passes_test(lambda user: user.is_superuser, login_url="admin:login")
def post_create(request):
    form_data = request.POST if request.method == "POST" else None
    file_data = request.FILES if request.method == "POST" else None
    post_form = PostForm(form_data)
    media_form = PostMediaForm(form_data, file_data)
    if request.method == "POST" and post_form.is_valid() and media_form.is_valid():
        with transaction.atomic():
            post = post_form.save()
            media = media_form.save(commit=False)
            media.post = post
            media.save()
        return redirect(post.get_absolute_url())
    return render(
        request,
        "blog/post_create.html",
        {"post_form": post_form, "media_form": media_form},
    )
