from django.forms import (
    ModelForm,
    NumberInput,
    Select,
    Textarea,
    TextInput,
    URLInput,
    DateTimeInput,
)

from main.models import Education, Experience
from django.core.exceptions import ValidationError
from django.utils.html import strip_tags


class EducationForm(ModelForm):
    class Meta:
        model = Education

        fields = [
            "institution",
            "level",
            "field_of_study",
            "start_year",
            "end_year",
            "grade",
            "activities",
            "achievements",
            "description",
            "school_image",
            "school_url",
        ]

        labels = {
            "institution": "Institution",
            "level": "Education Level",
            "field_of_study": "Field of Study",
            "start_year": "Start Year",
            "end_year": "End Year",
            "grade": "Grade / GPA",
            "activities": "Activities & Societies",
            "achievements": "Achievements",
            "description": "Description",
            "school_image": "School Image URL",
            "school_url": "School Website URL",
        }

        widgets = {
            "institution": TextInput(
                attrs={
                    "placeholder": "Universitas Indonesia",
                }
            ),
            "level": Select(),
            "field_of_study": TextInput(
                attrs={
                    "placeholder": "Computer Science",
                }
            ),
            "start_year": NumberInput(
                attrs={
                    "placeholder": "2025",
                }
            ),
            "end_year": NumberInput(
                attrs={
                    "placeholder": "Leave empty if ongoing",
                }
            ),
            "grade": TextInput(
                attrs={
                    "placeholder": "3.90 / 4.00",
                }
            ),
            "activities": Textarea(
                attrs={
                    "placeholder": "Organizations, clubs, committees, etc.",
                    "rows": 3,
                }
            ),
            "achievements": Textarea(
                attrs={
                    "placeholder": "Academic or non-academic achievements",
                    "rows": 3,
                }
            ),
            "description": Textarea(
                attrs={
                    "placeholder": "Short description about this education",
                    "rows": 4,
                }
            ),
            "school_image": URLInput(
                attrs={
                    "placeholder": "https://...",
                }
            ),
            "school_url": URLInput(
                attrs={
                    "placeholder": "https://...",
                }
            ),
            "ended_at": DateTimeInput(
                attrs={
                    "type": "datetime-local",
                }
            ),
        }

class ExperienceForm(ModelForm):
    class Meta:
        model = Experience

        fields = [
            "title",
            "description",
            "category",
            "thumbnail",
            "ended_at",
        ]

        def clean_title(self):
            title = strip_tags(
                self.cleaned_data["title"]
            ).strip()

            if not title:
                raise ValidationError(
                    "Title tidak boleh hanya berisi tag HTML."
                )

            return title


        def clean_description(self):
            return strip_tags(
                self.cleaned_data["description"]
            ).strip()

        labels = {
            "title": "Title",
            "description": "Description",
            "category": "Category",
            "thumbnail": "Thumbnail URL",
            "ended_at": "End Date",
        }

        widgets = {
            "title": TextInput(
                attrs={
                    "placeholder": "Human Resources - Open House Fasilkom UI",
                }
            ),
            "description": Textarea(
                attrs={
                    "placeholder": "Describe your experience",
                    "rows": 4,
                }
            ),
            "category": Select(),
            "thumbnail": URLInput(
                attrs={
                    "placeholder": "https://...",
                }
            ),
        }
        