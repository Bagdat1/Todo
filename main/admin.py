from django.contrib import admin

# Register your models here.


from main.models import Task

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'completed', 'created_at', 'updated_at')
    list_filter = ('completed','title')
    search_fields = ('title','created_at')


    