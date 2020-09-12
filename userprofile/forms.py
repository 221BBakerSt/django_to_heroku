from django import forms
# from django.contrib.auth.models import User
from .models import User


class ProfileForm(forms.ModelForm):
    class Meta:
        # refer to the database User
        model = User
        # the columns (in admin) that front-end can modify
        fields = ["avatar"]
