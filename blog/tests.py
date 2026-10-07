import tempfile

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, override_settings
from django.urls import reverse

from .models import Comment, Post, PostMedia
from .validators import MAX_MEDIA_SIZE, validate_media_size


class BlogViewsTests(TestCase):
    def create_post(self, title, published_at=None):
        post = Post.objects.create(
            title=title,
            excerpt="Una bajada de prueba.",
            body="Contenido de prueba.",
        )
        if published_at:
            Post.objects.filter(pk=post.pk).update(published_at=published_at)
            post.refresh_from_db()
        return post

    def test_posts_are_ordered_newest_first(self):
        older = self.create_post("Entrada antigua", "2025-01-01T12:00:00+00:00")
        newer = self.create_post("Entrada reciente", "2025-02-01T12:00:00+00:00")

        response = self.client.get(reverse("blog:post_list"))

        self.assertEqual(response.status_code, 200)
        self.assertLess(
            response.content.index(newer.title.encode()),
            response.content.index(older.title.encode()),
        )

    def test_commenters_can_comment_without_an_account(self):
        post = self.create_post("Entrada abierta")

        response = self.client.post(
            post.get_absolute_url(),
            {"author": "Visitante", "body": "Buen artículo."},
        )

        self.assertRedirects(response, f"{post.get_absolute_url()}#comments")
        self.assertEqual(
            Comment.objects.get(post=post).body,
            "Buen artículo.",
        )

    def test_public_route_does_not_create_posts(self):
        response = self.client.get("/blog/add/")

        self.assertEqual(response.status_code, 404)

    def test_detail_renders_supported_media_types(self):
        post = self.create_post("Entrada con archivos")
        PostMedia.objects.create(post=post, file="blog/video.mp4")
        PostMedia.objects.create(post=post, file="blog/audio.mp3")

        response = self.client.get(post.get_absolute_url())

        self.assertContains(response, "<video", html=False)
        self.assertContains(response, "<audio", html=False)

    def test_comments_are_in_a_collapsible_section_and_form_opens_on_error(self):
        post = self.create_post("Comentarios plegables")

        response = self.client.get(post.get_absolute_url())

        self.assertContains(response, "<details", html=False)
        self.assertContains(response, "Comentarios")
        self.assertContains(response, "Comentar")
        self.assertContains(response, 'id="comment-form"', html=False)

        invalid_response = self.client.post(
            post.get_absolute_url(),
            {"author": "", "body": ""},
        )

        self.assertEqual(invalid_response.status_code, 200)
        self.assertContains(invalid_response, "<details", html=False)
        self.assertContains(invalid_response, "Revisá los campos marcados")
        self.assertContains(invalid_response, "Este campo es obligatorio")

    def test_post_list_is_paginated(self):
        for number in range(7):
            self.create_post(f"Entrada {number}")

        first_page = self.client.get(reverse("blog:post_list"))
        second_page = self.client.get(reverse("blog:post_list"), {"page": 2})

        self.assertEqual(first_page.context["page_obj"].paginator.num_pages, 2)
        self.assertEqual(len(first_page.context["page_obj"].object_list), 6)
        self.assertEqual(len(second_page.context["page_obj"].object_list), 1)


class PostMediaValidationTests(TestCase):
    def test_media_kind_is_detected_for_images_video_audio_and_documents(self):
        post = Post.objects.create(
            title="Multimedia",
            excerpt="Una bajada.",
            body="Contenido.",
        )
        for file_name, expected_type in (
            ("photo.webp", "image"),
            ("clip.mp4", "video"),
            ("song.mp3", "audio"),
            ("notes.pdf", "file"),
        ):
            with self.subTest(file_name=file_name):
                media = PostMedia(
                    post=post,
                    file=SimpleUploadedFile(file_name, b"sample"),
                )
                self.assertEqual(media.media_type, expected_type)

    def test_unsupported_file_extension_is_rejected(self):
        post = Post.objects.create(
            title="Formato no permitido",
            excerpt="Una bajada.",
            body="Contenido.",
        )
        media = PostMedia(
            post=post,
            file=SimpleUploadedFile("script.exe", b"not a media file"),
        )

        with self.assertRaises(ValidationError):
            media.full_clean()

    def test_media_size_limit_is_twenty_megabytes(self):
        oversized_file = SimpleUploadedFile(
            "large.mp4",
            b"x" * (MAX_MEDIA_SIZE + 1),
        )

        with self.assertRaises(ValidationError):
            validate_media_size(oversized_file)


class BlogAdminTests(TestCase):
    def setUp(self):
        self.media_directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.media_directory.cleanup)
        self.settings_override = override_settings(MEDIA_ROOT=self.media_directory.name)
        self.settings_override.enable()
        self.addCleanup(self.settings_override.disable)
        self.admin = get_user_model().objects.create_superuser(
            username="admin",
            email="admin@example.com",
            password="admin",
        )
        self.client.force_login(self.admin)

    def test_only_authenticated_admin_can_open_publish_form(self):
        self.client.logout()

        response = self.client.get(reverse("admin:blog_post_add"))

        self.assertEqual(response.status_code, 302)

    def test_only_superuser_can_open_publication_form(self):
        self.client.logout()

        response = self.client.get(reverse("blog:post_create"))

        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse("admin:login"), response["Location"])

    def test_admin_login_redirects_to_entry_form(self):
        self.client.logout()

        response = self.client.post(
            reverse("admin:login"),
            {
                "username": "admin",
                "password": "admin",
                "next": reverse("blog:post_create"),
            },
        )

        self.assertRedirects(response, reverse("blog:post_create"))
        self.assertTrue(response.wsgi_request.user.is_superuser)

    def test_superuser_can_publish_post_with_name_text_and_attachment(self):
        response = self.client.post(
            reverse("blog:post_create"),
            {
                "title": "Entrada desde el blog",
                "author": "Admin del blog",
                "body": "Esta es una entrada de prueba.",
                "file": SimpleUploadedFile("photo.jpg", b"test-image"),
                "caption": "Foto de prueba",
            },
        )

        self.assertEqual(response.status_code, 302)
        post = Post.objects.get(title="Entrada desde el blog")
        self.assertEqual(post.author, "Admin del blog")
        self.assertEqual(post.body, "Esta es una entrada de prueba.")
        self.assertEqual(post.media.count(), 1)
        self.assertEqual(response["Location"], post.get_absolute_url())

    def test_empty_publication_submission_shows_required_field_errors(self):
        response = self.client.post(
            reverse("blog:post_create"),
            {"title": "", "author": "", "body": ""},
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Este campo es obligatorio")

    def test_admin_can_publish_entry_with_required_media(self):
        add_url = reverse("admin:blog_post_add")
        response = self.client.get(add_url)
        self.assertEqual(response.status_code, 200)

        post_data = {
            "title": "Entrada administrada",
            "author": "Admin",
            "slug": "",
            "excerpt": "Resumen.",
            "body": "Texto completo.",
            "media-TOTAL_FORMS": "1",
            "media-INITIAL_FORMS": "0",
            "media-MIN_NUM_FORMS": "1",
            "media-MAX_NUM_FORMS": "1000",
            "_save": "Guardar",
        }
        missing_media_response = self.client.post(add_url, post_data)
        self.assertEqual(missing_media_response.status_code, 200)
        self.assertFalse(Post.objects.filter(title="Entrada administrada").exists())

        post_data["media-0-file"] = SimpleUploadedFile("cover.jpg", b"test-image")
        post_data["media-0-caption"] = "Imagen de portada"
        response = self.client.post(add_url, post_data)

        self.assertEqual(response.status_code, 302)
        post = Post.objects.get(title="Entrada administrada")
        self.assertEqual(post.media.count(), 1)

    def test_admin_can_delete_comments(self):
        post = Post.objects.create(
            title="Entrada con comentario",
            excerpt="Resumen.",
            body="Texto.",
        )
        comment = Comment.objects.create(post=post, author="Visita", body="Comentario.")

        response = self.client.post(
            reverse("admin:blog_comment_delete", args=[comment.pk]),
            {"post": "yes"},
        )

        self.assertEqual(response.status_code, 302)
        self.assertFalse(Comment.objects.filter(pk=comment.pk).exists())
