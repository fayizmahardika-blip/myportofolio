
from django.contrib.auth.models import User
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase, APIClient  

from main.models import Project


class ProjectAPITests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            password="testpass123"
        )

        self.owner = User.objects.create_superuser(
            username="owner",
            email="owner@example.com",
            password="testpass123"
        )

        self.project = Project.objects.create(
            title="Project Test",
            description="Testing Django REST Framework",
            tech_stack="Django"
        )

        self.list_url = reverse("api:project-list")
        self.detail_url = reverse(
            "api:project-detail",
            args=[self.project.id]
        )
        self.star_url = reverse(
            "api:project-star",
            args=[self.project.id]
        )

    def test_anonymous_can_list_projects(self):
        response = self.client.get(self.list_url)

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )
        self.assertEqual(len(response.data), 1)

    def test_anonymous_can_view_project_detail(self):
        response = self.client.get(self.detail_url)

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )
        self.assertEqual(
            response.data["title"],
            "Project Test"
        )

    def test_anonymous_cannot_create_project(self):
        response = self.client.post(
            self.list_url,
            {
                "title": "Unauthorized Project",
                "description": "Should not be created",
                "tech_stack": "Python"
            },
            format="json"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN
        )
        self.assertEqual(Project.objects.count(), 1)

    def test_regular_user_cannot_create_project(self):
        self.client.force_authenticate(user=self.user)

        response = self.client.post(
            self.list_url,
            {
                "title": "Unauthorized Project",
                "description": "Should not be created",
                "tech_stack": "Python"
            },
            format="json"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN
        )

    def test_owner_can_create_project(self):
        self.client.force_authenticate(user=self.owner)

        response = self.client.post(
            self.list_url,
            {
                "title": "New Project",
                "description": "Created by owner",
                "tech_stack": "Django"
            },
            format="json"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )
        self.assertEqual(Project.objects.count(), 2)

    def test_user_can_toggle_star(self):
        self.client.force_authenticate(user=self.user)

        first_response = self.client.post(
            self.star_url,
            {},
            format="json"
        )

        self.assertEqual(
            first_response.status_code,
            status.HTTP_200_OK
        )
        self.assertEqual(
            first_response.data["star_count"],
            1
        )
        self.assertTrue(
            first_response.data["is_starred"]
        )

        second_response = self.client.post(
            self.star_url,
            {},
            format="json"
        )

        self.assertEqual(
            second_response.status_code,
            status.HTTP_200_OK
        )
        self.assertEqual(
            second_response.data["star_count"],
            0
        )
        self.assertFalse(
            second_response.data["is_starred"]
        )

    def test_anonymous_cannot_star(self):
        response = self.client.post(
            self.star_url, {}, format="json"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN
        )
        self.assertEqual(
            self.project.starred_by.count(), 0
        )

    def test_regular_user_cannot_update_project(self):
        self.client.force_authenticate(user=self.user)

        response = self.client.patch(
            self.detail_url,
            {"title": "Unauthorized Update"},
            format="json"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN
        )
        self.project.refresh_from_db()
        self.assertEqual(self.project.title, "Project Test")

    def test_owner_can_patch_project(self):
        self.client.force_authenticate(user=self.owner)

        response = self.client.patch(
            self.detail_url,
            {"title": "Updated Project"},
            format="json"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )
        self.project.refresh_from_db()
        self.assertEqual(
            self.project.title, "Updated Project"
        )

    def test_owner_can_delete_project(self):
        self.client.force_authenticate(user=self.owner)

        response = self.client.delete(self.detail_url)

        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT
        )
        self.assertFalse(
            Project.objects.filter(pk=self.project.pk).exists()
        )

    def test_invalid_title_is_rejected(self):
        self.client.force_authenticate(user=self.owner)

        response = self.client.post(
            self.list_url,
            {
                "title": "<b>   </b>",
                "description": "Invalid title test",
                "tech_stack": "Django"
            },
            format="json"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )
        self.assertEqual(Project.objects.count(), 1)

    def test_filter_projects_by_title(self):
        Project.objects.create(
            title="Other Project",
            description="Another project",
            tech_stack="Python"
        )

        response = self.client.get(
            self.list_url,
            {"title": "Project Test"}
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )
        self.assertEqual(len(response.data), 1)
        self.assertEqual(
            response.data[0]["title"],
            "Project Test"
        )

    def test_csrf_is_required_for_session_post(self):
        csrf_client = APIClient(
            enforce_csrf_checks=True
        )
        csrf_client.force_login(self.owner)

        response = csrf_client.post(
            self.list_url,
            {
                "title": "No CSRF Project",
                "description": "Should be rejected",
                "tech_stack": "Django"
            },
            format="json"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN
        )
        self.assertEqual(Project.objects.count(), 1)
