from django.forms import ModelForm, TextInput, Textarea, URLInput, NumberInput, Select
from main.models import Education


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
            "grade": "Grade",
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
                    "maxlength": 255,
                }
            ),

            "level": Select(),

            "field_of_study": TextInput(
                attrs={
                    "placeholder": "Computer Science",
                    "maxlength": 255,
                }
            ),

            "start_year": NumberInput(
                attrs={
                    "placeholder": "2025",
                }
            ),

            "end_year": NumberInput(
                attrs={
                    "placeholder": "2029",
                }
            ),

            "grade": TextInput(
                attrs={
                    "placeholder": "e.g. GPA 3.50 / 4.00",
                    "maxlength": 100,
                }
            ),

            "activities": Textarea(
                attrs={
                    "placeholder": "Organizations, societies, or activities",
                    "rows": 3,
                }
            ),

            "achievements": Textarea(
                attrs={
                    "placeholder": "Academic or extracurricular achievements",
                    "rows": 3,
                }
            ),

            "description": Textarea(
                attrs={
                    "placeholder": "Brief description of your education",
                    "rows": 4,
                }
            ),

            "school_image": URLInput(
                attrs={
                    "placeholder": "https://example.com/school-logo.png",
                }
            ),

            "school_url": URLInput(
                attrs={
                    "placeholder": "https://www.ui.ac.id",
                }
            ),
        }