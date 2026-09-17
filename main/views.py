from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404

from main.models import Experience, Education
from main.forms import EducationForm, ExperienceForm
from django.core import serializers
from django.http import HttpResponse



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
    json_response = get_experience_json(request)

    experiences = serializers.deserialize(
        "json",
        json_response.content.decode("utf-8"),
    )

    experiences = [
        experience.object
        for experience in experiences
    ]

    title_query = request.GET.get("title", "").strip()

    context = {
        "name": "Fayiz Mahardika Ghulam Afandi",
        "experience_list": experiences,
        "title_query": title_query,
    }

    return render(
        request,
        "experience.html",
        context,
    )

def create_experience(request):
    form = ExperienceForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Experience berhasil ditambahkan!")
        return redirect("main:show_experience")

    context = {
        "name": "Fayiz Mahardika Ghulam Afandi",
        "form": form,
    }

    return render(request, "experience_form.html", context)

def show_education(request):
    json_response = get_education_json(request)

    educations = serializers.deserialize(
        "json",
        json_response.content.decode("utf-8"),
    )

    educations = [education.object for education in educations]

    institution_query = request.GET.get("institution", "").strip()

    context = {
        "name": "Fayiz Mahardika Ghulam Afandi",
        "education_list": educations,
        "institution_query": institution_query,
    }

    return render(request, "education.html", context)

def create_education(request):
    form = EducationForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Education berhasil ditambahkan!")
        return redirect("main:show_education")

    context = {
        "name": "Fayiz Mahardika Ghulam Afandi",
        "form": form,
    }

    return render(request, "education_form.html", context)

def get_education_json(request):
    institution_query = request.GET.get("institution", "").strip()

    educations = Education.objects.all()

    if institution_query:
        educations = educations.filter(
            institution__icontains=institution_query
        )

    education_json = serializers.serialize("json", educations)

    return HttpResponse(
        education_json,
        content_type="application/json"
    )

def delete_education(request, education_id):
    education = get_object_or_404(Education, pk=education_id)

    if request.method == "POST":
        education.delete()
        messages.success(request, "Education berhasil dihapus!")
        return redirect("main:show_education")

    return redirect("main:show_education")

def edit_experience(request, experience_id):
    experience = get_object_or_404(
        Experience,
        pk=experience_id,
    )

    form = ExperienceForm(
        request.POST or None,
        instance=experience,
    )

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(
            request,
            "Experience berhasil diperbarui!",
        )

        return redirect("main:show_experience")

    context = {
        "name": "Fayiz Mahardika Ghulam Afandi",
        "form": form,
        "experience": experience,
    }

    return render(
        request,
        "experience_form.html",
        context,
    )

def delete_experience(request, experience_id):
    experience = get_object_or_404(
        Experience,
        pk=experience_id,
    )

    if request.method == "POST":
        experience.delete()
        messages.success(
            request,
            "Experience berhasil dihapus!",
        )

    return redirect("main:show_experience")

def get_experience_json(request):
    title_query = request.GET.get("title", "").strip()

    experiences = Experience.objects.all()

    if title_query:
        experiences = experiences.filter(
            title__icontains=title_query
        )

    experience_json = serializers.serialize(
        "json",
        experiences,
    )

    return HttpResponse(
        experience_json,
        content_type="application/json",
    )