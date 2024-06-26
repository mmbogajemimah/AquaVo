from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ("email", "is_staff", "is_active",)
    list_filter = ("email", "is_staff", "is_active",)
    fieldsets = (
        (None, {"fields": ("email", "password", "username")}),
        ("Permissions", {"fields": ("is_staff", "is_shop_owner", "phone_no", "estate", "house_number", "is_active", "groups", "user_permissions")})
    )
    add_fieldsets = (
        (None, {
            "classes":("wide",),
            "fields": (
                "email", "username", "password1", "password2", "is_staff", "is_shop_owner",
                "is_active", "groups", "user_permissions"
            )
        }),
    )
    search_fields = ("email",)
    ordering = ("email",)
    

# Register your models here.
admin.site.register(CustomUser, CustomUserAdmin)
