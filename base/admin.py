from django.contrib import admin
from .models import Skill, Contact, Certificate


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ['name', 'knowledge', 'created']


@admin.register(Certificate)
class CertificateAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'organization']


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'email', 'subject', 'created', 'is_read']
