from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from main.models import Experience, Education


class MainTest(TestCase):
    def setUp(self):
        self.experience = Experience.objects.create(
            title="Human Resources - Open House Fasilkom UI",
            description="Berperan dalam divisi Human Resources pada kegiatan Open House Fasilkom UI.",
            category="volunteer",
        )

    def test_main_url_is_accessible(self):
        response = self.client.get(reverse("main:show_main"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "index.html")
        self.assertNotContains(response, self.experience.title)
        self.assertContains(
            response,
            f'href="{reverse("main:show_experience")}"'
        )

    def test_nonexistent_page_returns_404(self):
        response = self.client.get("/halaman-yang-tidak-ada/")
        self.assertEqual(response.status_code, 404)

    def test_experience_model(self):
        self.assertEqual(
            str(self.experience),
            "Human Resources - Open House Fasilkom UI"
        )
        self.assertEqual(self.experience.category, "volunteer")
        self.assertTrue(self.experience.is_ongoing)

    def test_experience_page(self):
        response = self.client.get(reverse("main:show_experience"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "experience.html")
        self.assertContains(response, self.experience.title)
        self.assertContains(response, self.experience.description)
        self.assertContains(response, "Volunteer")
        self.assertContains(response, "Sedang berlangsung")
        self.assertContains(
            response,
            f'href="{reverse("main:show_main")}"'
        )

    def test_empty_experience_page(self):
        Experience.objects.all().delete()

        response = self.client.get(reverse("main:show_experience"))

        self.assertContains(
            response,
            "Belum ada pengalaman yang ditambahkan."
        )

    def test_completed_experience(self):
        self.experience.ended_at = timezone.now()
        self.experience.save()

        response = self.client.get(reverse("main:show_experience"))

        self.assertFalse(self.experience.is_ongoing)
        self.assertContains(response, "Selesai")
        self.assertNotContains(response, "Sedang berlangsung")

    def test_create_experience(self):
        response = self.client.post(
            reverse("main:create_experience"),
            {
                "title": "Staff Media BEM",
                "description": "Mengelola publikasi dan dokumentasi.",
                "category": "volunteer",
                "thumbnail": "",
                "ended_at": "",
            },
        )

        self.assertEqual(response.status_code, 302)

        self.assertTrue(
            Experience.objects.filter(
                title="Staff Media BEM"
            ).exists()
        )


    def test_edit_experience(self):
        response = self.client.post(
            reverse(
                "main:edit_experience",
                args=[self.experience.id],
            ),
            {
                "title": "Updated Experience",
                "description": "Updated description",
                "category": "volunteer",
                "thumbnail": "",
                "ended_at": "",
            },
        )

        self.assertEqual(response.status_code, 302)

        self.experience.refresh_from_db()

        self.assertEqual(
            self.experience.title,
            "Updated Experience",
        )


    def test_delete_experience(self):
        response = self.client.post(
            reverse(
                "main:delete_experience",
                args=[self.experience.id],
            )
        )

        self.assertEqual(response.status_code, 302)

        self.assertFalse(
            Experience.objects.filter(
                id=self.experience.id
            ).exists()
        )


    def test_experience_json(self):
        response = self.client.get(
            reverse("main:get_experience_json")
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response["Content-Type"],
            "application/json",
        )

        self.assertContains(
            response,
            self.experience.title,
        )


class EducationTest(TestCase):
    def setUp(self):
        self.education = Education.objects.create(
            institution="Universitas Indonesia",
            level="undergraduate",
            field_of_study="S1 Ilmu Komputer",
            start_year=2025,
            end_year=None,
            grade="-",
            activities="Staff of Media - BEM Fasilkom UI",
            achievements="",
            description=(
                "Mahasiswa Ilmu Komputer di Fakultas Ilmu Komputer "
                "Universitas Indonesia."
            ),
            school_image="/static/img/ui.png",
            school_url="https://www.ui.ac.id/",
        )

    def test_education_url_is_accessible(self):
        response = self.client.get(reverse("main:show_education"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "education.html")

    def test_education_data_appears_on_page(self):
        response = self.client.get(reverse("main:show_education"))

        self.assertContains(response, self.education.institution)
        self.assertContains(response, self.education.field_of_study)
        self.assertContains(response, "Undergraduate")

    def test_empty_education_page(self):
        Education.objects.all().delete()

        response = self.client.get(reverse("main:show_education"))

        self.assertContains(
            response,
            "No education added yet"
        )