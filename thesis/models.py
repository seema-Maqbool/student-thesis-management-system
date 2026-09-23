from django.conf import settings
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class Thesis(models.Model):

    STATUS_CHOICES = [
        ("proposed", "Proposed"),
        ("approved", "Approved"),
        ("in_progress", "In Progress"),
        ("submitted", "Submitted"),
        ("under_review", "Under Review"),
        ("completed", "Completed"),
    ]

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="theses",
        null=True,
        blank=True,
    )

    title = models.CharField(max_length=255)
    student_name = models.CharField(max_length=150)
    supervisor_name = models.CharField(max_length=150)
    department = models.CharField(max_length=150)
    university = models.CharField(max_length=200)

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="proposed",
    )

    description = models.TextField(
        blank=True,
        null=True,
    )

    document = models.FileField(
        upload_to="thesis_documents/",
        blank=True,
        null=True,
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title


# ============================
# ROLE-BASED ACCESS: PROFILE MODEL
# ============================

class Profile(models.Model):

    ROLE_CHOICES = [
        ("student", "Student"),
        ("admin", "Admin"),
    ]

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="profile",
    )

    role = models.CharField(
        max_length=10,
        choices=ROLE_CHOICES,
        default="student",
    )

    university = models.CharField(
        max_length=200,
        blank=True,
    )

    department = models.CharField(
        max_length=150,
        blank=True,
    )

    def __str__(self):
        return f"{self.user.username} ({self.role})"


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    else:
        Profile.objects.get_or_create(user=instance)