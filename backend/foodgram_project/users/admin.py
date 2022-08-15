from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ('pk',
                    'username',
                    'first_name',
                    'last_name',
                    'email',
                    'is_staff',
                    'is_active',)
    search_fields = ('username', 'first_name', 'last_name', 'email',)
    list_filter = ('username', 'email',)
    empty_value_display = '-пусто-'

    class Meta:
        proxy = True
