from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth import authenticate, get_user_model
from django.contrib.contenttypes.models import ContentType

from .forms import UserChangeForm, UserCreationForm

User = get_user_model()


class CustomUserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm
    model = User
    ordering = ('email',)

    list_display = (
        'username', 'email', 'is_active', 'is_staff', 'is_admin', 'is_superuser',
        'created', 'modified'
    )
    fieldsets = (
        (None, {'fields': (
            'username', 'email', 'password', 'is_active', 'is_staff', 'is_admin', 'is_superuser',
            'last_login',
            'groups')}),
    )

    add_fieldsets = (
        (None, {
            'fields': (
                'username', 'email', 'password1', 'password2', 'is_active', 'is_staff', 'is_admin',
                'is_superuser'),
        }),
    )
    filter_horizontal = ()


admin.site.register(User, CustomUserAdmin)
