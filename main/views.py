from django.shortcuts import render

# Create your views here.

from main.models import Experience


def show_main(request):
    context = {
        "name": "Fayiz Mahardika Ghulam Afandi",
        "npm": "2506617374",
        "study_program": "S1 Ilmu Komputer",
        "bio": (
            "CS student at Universitas Indonesia for longer than planned."
        ),
    }

    return render(request, "index.html", context)


def show_experience(request):
    context = {
        "name": "Fayiz Mahardika Ghulam Afandi",
        "experience_list": Experience.objects.all(),
    }

    return render(request, "experience.html", context)