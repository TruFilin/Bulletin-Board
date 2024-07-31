from django.db import models
from django.contrib.auth.models import User

class Announcement(models.Model):
    CATEGORY_CHOICES = [
        ('tanks', 'Танки'),
        ('healers', 'Хилы'),
        ('dd', 'ДД'),
        ('traders', 'Торговцы'),
        ('guildmasters', 'Гилдмастеры'),
        ('questgivers', 'Квестгиверы'),
        ('blacksmiths', 'Кузнецы'),
        ('tanners', 'Кожевники'),
        ('potionmasters', 'Зельевары'),
        ('spellmasters', 'Мастера заклинаний'),
    ]

    title = models.CharField(max_length=200)
    content = models.TextField()
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='announcements_images/', blank=True, null=True)
    video = models.FileField(upload_to='announcements_videos/', blank=True, null=True)

    def __str__(self):
        return self.title

class Response(models.Model):
    announcement = models.ForeignKey(Announcement, on_delete=models.CASCADE, related_name='responses')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Отклик от {self.user.username} на "{self.announcement.title}"'

class News(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title