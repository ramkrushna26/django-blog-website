from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from PIL import Image


class Post(models.Model):
    title = models.CharField(max_length=80)
    author_description = models.CharField(max_length=160)
    content = models.TextField()
    posted_on = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.FileField(blank=True, null=True, upload_to='posts')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('posts-detail', kwargs={'pk': self.pk})

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        img = Image.open(self.image.path)
        if img.height > 650 or img.width > 750:
            output_size = (650, 750)
            img.thumbnail(output_size)
            img.save(self.image.path)


class Comment(models.Model):
    full_name = models.CharField(max_length=80)
    email = models.EmailField(max_length=60)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    commented_date = models.DateTimeField(default=timezone.now)
    content = models.TextField()

    def __str__(self):
        return self.content

    class Meta:
        ordering = ['-commented_date']





