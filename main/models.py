from django.db import models

# Create your models here.

class Task(models.Model):
    title = models.CharField(max_length=255, verbose_name="Название задачи")
    description = models.TextField(blank=True, null=True, verbose_name="Описание")
    completed = models.BooleanField(default=False, verbose_name="Выполнено")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")
    

    def __str__(self):
        return self.title
    
class Meta:
        verbose_name = "Задача"
        verbose_name_plural = "Задачи"
