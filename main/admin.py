from django.contrib import admin
from django.utils.html import format_html
from django.utils.safestring import mark_safe

from main.models import Task, CustomUser

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'display_image', 'is_staff')
    list_filter = ('is_staff', 'is_active', 'date_joined')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    readonly_fields = ('last_login', 'date_joined', 'preview_image')
    fieldsets = (
        ('Основная информация', {
            'fields': ('username', 'email', 'password')
        }),
        ('Персональная информация', {
            'fields': ('first_name', 'last_name', 'image', 'preview_image', 'bio')
        }),
        ('Права доступа', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
            'classes': ('collapse',)
        }),
        ('Важные даты', {
            'fields': ('last_login', 'date_joined')
        }),
    )
    
    def display_image(self, obj):
        if obj.image:
            return format_html(
                '<div style="width:30px; height:30px; overflow:hidden; border-radius:3px; display:flex; align-items:center; justify-content:center;">'
                '<img src="{}" style="object-fit:cover; width:100%; height:100%;" />'
                '</div>', 
                obj.image.url
            )
        return "Нет изображения"
    display_image.short_description = "Фото"
    
    def preview_image(self, obj):
        if obj.image:
            return format_html(
                '<div style="width:200px; height:200px; overflow:hidden; border-radius:5px; display:flex; align-items:center; justify-content:center;">'
                '<img src="{}" style="object-fit:cover; width:100%; height:100%;" />'
                '</div>', 
                obj.image.url
            )
        return "Нет изображения"
    preview_image.short_description = "Предпросмотр изображения"


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'completed_status', 'created_at', 'updated_at')
    list_filter = ('completed', 'created_at', 'updated_at')
    search_fields = ('title', 'description', 'user__username')
    readonly_fields = ('created_at', 'updated_at')
    list_per_page = 25
    date_hierarchy = 'created_at'
    fieldsets = (
        ('Информация о задаче', {
            'fields': ('title', 'description', 'user', 'completed')
        }),
        ('Даты', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def completed_status(self, obj):
        if obj.completed:
            return format_html('<span style="color: green; font-weight: bold;">✓</span>')
        return format_html('<span style="color: red; font-weight: bold;">✗</span>')
    completed_status.short_description = "Статус"


