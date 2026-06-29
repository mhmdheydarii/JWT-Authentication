from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Profile


# Register your models here.


class CustomUserAdmin(UserAdmin):

    list_display = ("id", "email", "is_superuser", "is_active", "is_verified")
    list_filter = ("is_superuser", "is_active", "is_verified")
    searching_fields = ("email",)
    ordering = ("email",)
    fieldsets = (
        (
            "Authentication",
            {
                "fields": ("email", "password"),
            },
        ),
        (
            "permissions",
            {
                "fields": (
                    "is_staff",
                    "is_active",
                    "is_superuser",
                    "is_verified",
                ),
            },
        ),
        (
            "group permissions",
            {
                "fields": ("groups", "user_permissions", "type"),
            },
        ),
        (
            "important date",
            {
                "fields": ("last_login",),
            },
        ),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "password1",
                    "password2",
                    "is_staff",
                    "is_active",
                    "is_superuser",
                    "is_verified",
                    "type",
                ),
            },
        ),
    )
admin.site.register(User, CustomUserAdmin)

@admin.register(Profile)
class AdminProfile(admin.ModelAdmin):
    list_display = ("id" ,"user", "first_name", "last_name")
    search_fields = ("user",)