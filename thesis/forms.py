
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Thesis


class ThesisForm(forms.ModelForm):

    class Meta:
        model = Thesis

        fields = [
            "title",
            "student_name",
            "supervisor_name",
            "department",
            "university",
            "status",
            "description",
            "document",
        ]

        widgets = {
            "title": forms.TextInput(
                attrs={
                    "placeholder": "Enter thesis title",
                }
            ),

            "student_name": forms.TextInput(
                attrs={
                    "placeholder": "Enter student name",
                }
            ),

            "supervisor_name": forms.TextInput(
                attrs={
                    "placeholder": "Enter supervisor name",
                }
            ),

            "department": forms.TextInput(
                attrs={
                    "placeholder": "Enter department",
                }
            ),

            "university": forms.TextInput(
                attrs={
                    "placeholder": "Enter university",
                }
            ),

            "status": forms.Select(),

            "description": forms.Textarea(
                attrs={
                    "placeholder": "Enter thesis description",
                    "rows": 5,
                }
            ),
        }


class SignupForm(UserCreationForm):

    university = forms.CharField(
        max_length=200,
        required=True,
        widget=forms.TextInput(
            attrs={
                "placeholder": "Enter your university name",
            }
        ),
    )

    department = forms.CharField(
        max_length=150,
        required=True,
        widget=forms.TextInput(
            attrs={
                "placeholder": "Enter your department",
            }
        ),
    )

    class Meta:
        model = User

        fields = [
            "username",
            "email",
            "password1",
            "password2",
        ]

