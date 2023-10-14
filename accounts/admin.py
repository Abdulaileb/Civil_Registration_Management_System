from django.contrib import admin

from django.contrib.auth.admin import UserAdmin
from accounts.models import CustomUser

# Register your models here.

class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email','role','full_name', 'gender', 'occupation', 'is_staff',)
    list_filter = ('role', 'role')
    fieldsets = (
        (None, {'fields': ('username', 'password', 'email')}),
        ('Personal Info', {'fields': ('email', 'full_name')}),
        ('Role', {'fields': ('role')}),
        ('Client Info', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
        ('Registration_OFficer Info', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
        ('Important Dates', {'fields': ('last_login', 'data_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'role', 'full_name', 'is_staff'),
        }),
    )
    search_fields = ('username', 'email', 'full_name', 'region', 'district')
    ordering = ('username',)

# Register the CustomUser model with the CustomUserAdmin class
admin.site.register(CustomUser, CustomUserAdmin)
