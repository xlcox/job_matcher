from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Resume, Vacancy

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('email', 'full_name', 'is_admin', 'is_staff')
    fieldsets = (
        (None, {'fields': ('email','password')}),
        ('Личные данные', {'fields': ('full_name','phone_number','date_of_birth')}),
        ('Права',       {'fields': ('is_active','is_admin','is_staff','groups','user_permissions')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email','full_name','password1','password2'),
        }),
    )
    ordering = ('email',)

@admin.register(Resume)
class ResumeAdmin(admin.ModelAdmin):
    list_display = ('id','full_name','mail')

@admin.register(Vacancy)
class VacancyAdmin(admin.ModelAdmin):
    list_display = ('id','name')
