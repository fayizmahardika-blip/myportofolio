
import uuid

from django.contrib.auth.models import Group, User
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from main.models import Experience


class ExperienceAPITests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="normaluser",
            password="testpass123",
        )

        self.editor = User.objects.create_user(
            username="editor",
            password="testpass123",
        )

        editor_group = Group.objects.create(name="Editor")
        self.editor.groups.add(editor_group)

        self.owner = User.objects.create_superuser(
            username="owner",
            email="owner@example.com",
            password="testpass123",
        )

        self.experience = Experience.objects.create(
            title="Original Experience",
            description="Testing Experience API",
            category="full-time",
        )

        self.payload = {
            "title": "New Experience",
            "description": "Created through DRF",
            "category": "internship",
        }

        self.list_url = reverse("api:experience-list")

        self.detail_url = reverse(
            "api:experience-detail",
            args=[self.experience.id],
        )

        self.star_url = reverse(
            "api:experience-star",
            args=[self.experience.id],
        )

    def test_anonymous_can_read(self):
        list_response = self.client.get(self.list_url)
        detail_response = self.client.get(self.detail_url)

        self.assertEqual(list_response.status_code, 200)
        self.assertEqual(detail_response.status_code, 200)
        self.assertEqual(len(list_response.data), 1)
        self.assertEqual(
            detail_response.data["title"],
            "Original Experience",
        )
        self.assertIn("star_count", detail_response.data)
        self.assertIn("is_starred", detail_response.data)
        self.assertNotIn("password", detail_response.data)
        self.assertNotIn("email", detail_response.data)

    def test_anonymous_cannot_create_or_star(self):
        create_response = self.client.post(
            self.list_url,
            self.payload,
            format="json",
        )
        star_response = self.client.post(
            self.star_url,
            {},
            format="json",
        )

        self.assertEqual(create_response.status_code, 403)
        self.assertEqual(star_response.status_code, 403)
        self.assertEqual(Experience.objects.count(), 1)
        self.assertEqual(self.experience.starred_by.count(), 0)

    def test_user_can_toggle_star(self):
        self.client.force_authenticate(user=self.user)

        response = self.client.post(
            self.star_url, {}, format="json"
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["star_count"], 1)
        self.assertTrue(response.data["is_starred"])
        self.assertTrue(
            self.experience.starred_by.filter(
                pk=self.user.pk
            ).exists()
        )

        response = self.client.post(
            self.star_url, {}, format="json"
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["star_count"], 0)
        self.assertFalse(response.data["is_starred"])
        self.assertEqual(self.experience.starred_by.count(), 0)

    def test_user_cannot_manage_experience(self):
        self.client.force_authenticate(user=self.user)

        create_response = self.client.post(
            self.list_url, self.payload, format="json"
        )
        update_response = self.client.patch(
            self.detail_url,
            {"title": "Unauthorized"},
            format="json",
        )
        delete_response = self.client.delete(self.detail_url)

        self.assertEqual(create_response.status_code, 403)
        self.assertEqual(update_response.status_code, 403)
        self.assertEqual(delete_response.status_code, 403)

        self.experience.refresh_from_db()
        self.assertEqual(self.experience.title, "Original Experience")
        self.assertEqual(Experience.objects.count(), 1)

    def test_editor_can_patch(self):
        self.client.force_authenticate(user=self.editor)

        response = self.client.patch(
            self.detail_url,
            {"title": "<b>Updated by Editor</b>"},
            format="json",
        )

        self.assertEqual(response.status_code, 200)

        self.experience.refresh_from_db()
        self.assertEqual(
            self.experience.title,
            "Updated by Editor",
        )

    def test_editor_cannot_create_or_delete(self):
        self.client.force_authenticate(user=self.editor)

        create_response = self.client.post(
            self.list_url, self.payload, format="json"
        )
        delete_response = self.client.delete(self.detail_url)

        self.assertEqual(create_response.status_code, 403)
        self.assertEqual(delete_response.status_code, 403)
        self.assertEqual(Experience.objects.count(), 1)
        self.assertTrue(
            Experience.objects.filter(
                pk=self.experience.pk
            ).exists()
        )

    def test_owner_can_create(self):
        self.client.force_authenticate(user=self.owner)

        response = self.client.post(
            self.list_url, self.payload, format="json"
        )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(Experience.objects.count(), 2)

    def test_owner_can_put(self):
        self.client.force_authenticate(user=self.owner)

        response = self.client.put(
            self.detail_url,
            self.payload,
            format="json",
        )

        self.assertEqual(response.status_code, 200)

        self.experience.refresh_from_db()
        self.assertEqual(
            self.experience.title,
            "New Experience",
        )

    def test_owner_can_delete(self):
        self.client.force_authenticate(user=self.owner)

        response = self.client.delete(self.detail_url)

        self.assertEqual(response.status_code, 204)
        self.assertFalse(
            Experience.objects.filter(
                pk=self.experience.pk
            ).exists()
        )

    def test_invalid_title_rejected(self):
        self.client.force_authenticate(user=self.owner)

        payload = {
            **self.payload,
            "title": "<b>   </b>",
        }

        response = self.client.post(
            self.list_url,
            payload,
            format="json",
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(Experience.objects.count(), 1)

    def test_search_by_title(self):
        Experience.objects.create(
            title="Unique Internship",
            description="Another experience",
            category="internship",
        )

        response = self.client.get(
            self.list_url,
            {"title": "Unique"},
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(
            response.data[0]["title"],
            "Unique Internship",
        )

    def test_csrf_required_for_session_post(self):
        client = APIClient(enforce_csrf_checks=True)

        self.assertTrue(
            client.login(
                username="owner",
                password="testpass123",
            )
        )

        response = client.post(
            self.list_url,
            self.payload,
            format="json",
        )

        self.assertEqual(response.status_code, 403)
        self.assertIn(b"CSRF", response.content)
        self.assertEqual(Experience.objects.count(), 1)

    def test_nonexistent_experience_returns_404(self):
        missing_url = reverse(
            "api:experience-detail",
            args=[uuid.uuid4()],
        )

        response = self.client.get(missing_url)

        self.assertEqual(response.status_code, 404)
