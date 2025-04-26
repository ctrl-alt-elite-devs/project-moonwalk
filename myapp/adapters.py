from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from allauth.account.adapter import DefaultAccountAdapter
from django.contrib import messages
import re

class MySocialAccountAdapter(DefaultSocialAccountAdapter):
    def populate_user(self, request, sociallogin, data):
        user = super().populate_user(request, sociallogin, data)

        email = data.get("email")
        if email:
            user.email = email
            user.username = email  # ✅ Set username to email at creation time

        return user
    
class MyAccountAdapter(DefaultAccountAdapter):
    def add_message(self, request, level, message_template, message_context=None):
        # suppress the default "logged_in.txt" message
        if message_template == "account/messages/logged_in.txt":
            user = message_context.get("user") or request.user
            messages.success(request, f"Welcome back, {user.first_name}!")
            return
        super().add_message(request, level, message_template, message_context)