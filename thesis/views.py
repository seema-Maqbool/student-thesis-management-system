from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render

from .forms import ThesisForm, SignupForm
from .models import Thesis


def is_admin(user):
    """Returns True if the logged-in user's profile role is 'admin'."""
    return hasattr(user, "profile") and user.profile.role == "admin"


def signup(request):
    if request.method == "POST":
        form = SignupForm(request.POST)

        if form.is_valid():
            user = form.save()

            # Save the extra university/department fields
            # into the user's Profile (created automatically
            # by our post_save signal).
            user.profile.university = form.cleaned_data["university"]
            user.profile.department = form.cleaned_data["department"]
            user.profile.save()

            login(request, user)

            messages.success(
                request,
                "Account created successfully!",
            )

            return redirect("home")

    else:
        form = SignupForm()

    return render(
        request,
        "registration/signup.html",
        {"form": form},
    )


@login_required
def home(request):
    if is_admin(request.user):
        theses = Thesis.objects.all().order_by("-id")
    else:
        theses = Thesis.objects.filter(owner=request.user).order_by("-id")

    total_theses = theses.count()
    in_progress_count = theses.filter(status="in_progress").count()
    submitted_count = theses.filter(status="submitted").count()
    completed_count = theses.filter(status="completed").count()

    context = {
        "theses": theses,
        "total_theses": total_theses,
        "in_progress_count": in_progress_count,
        "submitted_count": submitted_count,
        "completed_count": completed_count,
        "is_admin": is_admin(request.user),
    }

    return render(request, "thesis/home.html", context)


@login_required
def thesis_list(request):
    if is_admin(request.user):
        theses = Thesis.objects.all().order_by("-id")
    else:
        theses = Thesis.objects.filter(owner=request.user).order_by("-id")

    search = request.GET.get("search", "")
    department = request.GET.get("department", "")

    if search:
        theses = theses.filter(
            title__icontains=search
        ) | theses.filter(
            student_name__icontains=search
        ) | theses.filter(
            supervisor_name__icontains=search
        )

    if department:
        theses = theses.filter(department=department)

    departments = (
        Thesis.objects
        .values_list("department", flat=True)
        .distinct()
    )

    paginator = Paginator(theses, 6)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        "theses": page_obj,
        "page_obj": page_obj,
        "departments": departments,
        "search": search,
        "selected_department": department,
        "is_admin": is_admin(request.user),
    }

    return render(request, "thesis/thesis_list.html", context)


@login_required
def thesis_detail(request, pk):
    thesis = get_object_or_404(Thesis, pk=pk)

    if not is_admin(request.user) and thesis.owner != request.user:
        raise PermissionDenied

    context = {
        "thesis": thesis,
        "is_admin": is_admin(request.user),
    }

    return render(
        request,
        "thesis/thesis_detail.html",
        context,
    )


@login_required
def add_thesis(request):
    if request.method == "POST":
        form = ThesisForm(
            request.POST,
            request.FILES,
        )

        if form.is_valid():
            thesis = form.save(commit=False)
            thesis.owner = request.user
            thesis.save()

            messages.success(
                request,
                "Thesis added successfully!",
            )

            return redirect("thesis_list")

        messages.error(
            request,
            "Please correct the errors below.",
        )

    else:
        form = ThesisForm()

    return render(
        request,
        "thesis/add_thesis.html",
        {"form": form},
    )


@login_required
def edit_thesis(request, pk):
    thesis = get_object_or_404(Thesis, pk=pk)

    if not is_admin(request.user) and thesis.owner != request.user:
        raise PermissionDenied

    user_is_admin = is_admin(request.user)

    if request.method == "POST":
        form = ThesisForm(
            request.POST,
            request.FILES,
            instance=thesis,
        )

        if not user_is_admin:
            form.fields["status"].disabled = True

        if form.is_valid():
            form.save()

            messages.success(
                request,
                "Thesis updated successfully!",
            )

            return redirect(
                "thesis_detail",
                pk=thesis.pk,
            )

        messages.error(
            request,
            "Please correct the errors below.",
        )

    else:
        form = ThesisForm(instance=thesis)

        if not user_is_admin:
            form.fields["status"].disabled = True

    context = {
        "form": form,
        "thesis": thesis,
        "is_admin": user_is_admin,
    }

    return render(
        request,
        "thesis/edit_thesis.html",
        context,
    )


@login_required
def delete_thesis(request, pk):
    thesis = get_object_or_404(Thesis, pk=pk)

    if not is_admin(request.user):
        raise PermissionDenied

    if request.method == "POST":
        thesis.delete()

        messages.success(
            request,
            "Thesis deleted successfully!",
        )

        return redirect("thesis_list")

    return render(
        request,
        "thesis/delete_thesis.html",
        {"thesis": thesis},
    )


@login_required
def profile(request):
    return render(
        request,
        "registration/profile.html",
        {"user": request.user},
    )


@login_required
def all_students(request):
    if not is_admin(request.user):
        raise PermissionDenied

    students = User.objects.filter(
        profile__role="student"
    ).order_by("username")

    student_data = []

    for student in students:
        thesis_count = Thesis.objects.filter(owner=student).count()

        student_data.append({
            "user": student,
            "thesis_count": thesis_count,
        })

    context = {
        "student_data": student_data,
        "is_admin": True,
    }

    return render(
        request,
        "thesis/all_students.html",
        context,
    )

@login_required
def update_status(request, pk):
    thesis = get_object_or_404(Thesis, pk=pk)

    if not is_admin(request.user):
        raise PermissionDenied

    if request.method == "POST":
        new_status = request.POST.get("status")

        valid_statuses = [choice[0] for choice in Thesis.STATUS_CHOICES]

        if new_status in valid_statuses:
            thesis.status = new_status
            thesis.save()

            messages.success(
                request,
                "Status updated successfully!",
            )
        else:
            messages.error(
                request,
                "Invalid status selected.",
            )

    next_url = request.POST.get("next", "thesis_list")
    return redirect(next_url)