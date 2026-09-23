from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),

    path("theses/", views.thesis_list, name="thesis_list"),

    path(
        "add-thesis/",
        views.add_thesis,
        name="add_thesis",
    ),

    path(
        "thesis/<int:pk>/",
        views.thesis_detail,
        name="thesis_detail",
    ),

    path(
        "thesis/<int:pk>/edit/",
        views.edit_thesis,
        name="edit_thesis",
    ),

    path(
        "thesis/<int:pk>/delete/",
        views.delete_thesis,
        name="delete_thesis",
    ),

    path(
        "thesis/<int:pk>/update-status/",
        views.update_status,
        name="update_status",
    ),

    path(
        "all-students/",
        views.all_students,
        name="all_students",
    ),
]