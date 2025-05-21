from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    image = models.ImageField(
         upload_to='profile_images/', 
         blank=True, null=True, 
         verbose_name="Изображение профиля"
    )
    bio = models.TextField(
        blank=True, null=True, 
        verbose_name="Биография"
    )

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
        ordering = ['username']     


class Task(models.Model):
    title = models.CharField(max_length=255, verbose_name="Название задачи")
    description = models.TextField(blank=True, null=True, verbose_name="Описание")
    completed = models.BooleanField(default=False, verbose_name="Выполнено")
    user = models.ForeignKey(
        CustomUser, 
        on_delete=models.CASCADE, 
        related_name='tasks', 
        verbose_name="Пользователь"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")
    

    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = "Задача"
        verbose_name_plural = "Задачи"
