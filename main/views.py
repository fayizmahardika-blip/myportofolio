import datetime
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404

from main.models import Experience, Education
from main.forms import EducationForm, ExperienceForm
from django.core import serializers
from django.http import HttpResponse

from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied

def show_main(request):

    last_login = request.COOKIES.get(
    "last_login",
    "Belum ada sesi login / Cookie tidak ditemukan",
    )
    context = {
        "name": "Fayiz Mahardika Ghulam Afandi",
        "npm": "2506617374",
        "study_program": "S1 Ilmu Komputer",
        "bio": (
            "CS student at Universitas Indonesia for longer than planned."
        ),
        "last_login": last_login,
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

@login_required(login_url="/login/")
def create_experience(request):
    if not request.user.is_superuser:
        raise PermissionDenied

    form = ExperienceForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(
            request,
            "Experience berhasil ditambahkan!"
        )
        return redirect("main:show_experience")

    context = {
        "name": "Fayiz Mahardika Ghulam Afandi",
        "form": form,
    }

    return render(
        request,
        "experience_form.html",
        context,
    )

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

@login_required(login_url="/login/")
def edit_experience(request, experience_id):
    if not request.user.is_superuser:
        raise PermissionDenied

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
            "Experience berhasil diperbarui!"
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


@login_required(login_url="/login/")
def delete_experience(request, experience_id):
    if not request.user.is_superuser:
        raise PermissionDenied

    experience = get_object_or_404(
        Experience,
        pk=experience_id,
    )

    if request.method == "POST":
        experience.delete()
        messages.success(
            request,
            "Experience berhasil dihapus!"
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
    use_natural_foreign_keys=True,
    )

    return HttpResponse(
        experience_json,
        content_type="application/json",
    )

def register(request):
    form = UserCreationForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(
            request,
            "Akun berhasil dibuat. Silakan login."
        )
        return redirect("main:login")

    context = {
        "name": "Fayiz Mahardika Ghulam Afandi",
        "form": form,
    }

    return render(
        request,
        "register.html",
        context,
    )

def login_user(request):
    form = AuthenticationForm(
        request,
        data=request.POST or None,
    )

    if request.method == "POST" and form.is_valid():
        user = form.get_user()

        login(request, user)

        response = redirect("main:show_main")

        response.set_cookie(
            "last_login",
            datetime.datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            ),
        )

        return response

    context = {
        "name": "Fayiz Mahardika Ghulam Afandi",
        "form": form,
    }

    return render(
        request,
        "login.html",
        context,
    )

def logout_user(request):
    logout(request)

    response = redirect("main:show_main")
    response.delete_cookie("last_login")

    return response

@login_required(login_url="/login/")
def toggle_star_experience(request, experience_id):
    experience = get_object_or_404(
        Experience,
        pk=experience_id,
    )

    if request.method == "POST":
        if request.user in experience.starred_by.all():
            experience.starred_by.remove(request.user)
        else:
            experience.starred_by.add(request.user)

    return redirect("main:show_experience")