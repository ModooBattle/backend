from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Accuse, BannedUser, Location, User


# Register your models here.
@admin.register(User)
class CustomUserAdmin(UserAdmin):
    fieldsets = (
        (
            "Profile",
            {
                "fields": (
                    "username",
                    "email",
                    "age",
                    "gender",
                    "sport",
                    "years",
                    "gym",
                    "weight",
                ),
                "classes": ("wide",),
            },
        ),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "yellow_card"
                    # "user_permissions",
                ),
            },
        ),
        (
            "Important Dates",
            {
                "fields": ("password", "last_login", "date_joined", "uuid"),
                "classes": ("collapse",),  # 접었다폈다
            },
        ),
    )
    list_display = (
        "id",
        "is_superuser",
        "username",
        "email",
        "age",
        "gender",
        "sport",
        "gym",
        "weight",
        "user_location",
        "date_joined",
        "last_login",
    )
    list_filter = ("is_superuser", "is_staff", "age", "sport", "gender", "yellow_card", "gym", "weight", "years")
    search_fields = ("username", "email")
    ordering = ("id",)
    # filter_horizontal = (
    #     "groups",
    #     "user_permissions",
    # )

    readonly_fields = ("date_joined", "last_login", "uuid")


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "address",
        "latitude",
        "longitude",
    )


@admin.register(BannedUser)
class BannedAdmin(admin.ModelAdmin):
    list_display = (
        "email",
        "created_at",
    )


@admin.register(Accuse)
class AccuseAdmin(admin.ModelAdmin):
    list_display = ("reporter", "reported_user", "created_at", "admin_confirm")
    list_filter = ("admin_confirm",)
