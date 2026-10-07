from django.contrib.staticfiles.finders import find
from django.test import TestCase
from django.urls import reverse


class PortfolioViewTests(TestCase):
    def test_homepage_is_served_by_the_portfolio_app(self):
        response = self.client.get(reverse("portfolio:home"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Juan Giuri")
        self.assertContains(response, "Blog")

    def test_static_assets_follow_the_project_structure(self):
        for path in (
            "css/styles.css",
            "js/site.js",
            "js/portfolio.js",
            "images/pancho123.png",
        ):
            with self.subTest(path=path):
                self.assertIsNotNone(find(path))
