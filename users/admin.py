from django.contrib import admin
from .models import Profile


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'profile_pic']

    def phone_number(self, obj):
        return obj.phone_number

    def home_address(self, obj):
        return obj.home_address

    def location(self, obj):
        return obj.location
