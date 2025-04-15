from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
import re

class MySocialAccountAdapter(DefaultSocialAccountAdapter):
    def populate_user(self, request, sociallogin, data):
        user = super().populate_user(request, sociallogin, data)

        email = data.get("email")
        if email:
            user.email = email
            user.username = email  # ✅ Set username to email at creation time

        return user