from django.contrib import admin
from authapp.models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'first_name', 'last_name', 'age', 'is_staff', 'is_active')
    list_per_page = 10
    list_filter = ('username', 'is_staff', 'is_active')
    search_fields = ('username', 'first_name', 'last_name')
    show_full_result_count = False
