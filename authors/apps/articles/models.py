from django.db import models
from django.contrib.auth import get_user_model

class Tag(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Article(models.Model):
    title = models.CharField(max_length=100)
    slug = models.CharField(max_length=120)
    description = models.CharField(max_length=300)
    body = models.TextField()
    tagList = models.ManyToManyField(Tag)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)
    favorited = models.BooleanField()
    favoritesCount = models.PositiveIntegerField()
    author = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE, null=False
    )
    
    def __str__(self):
        return self.title

    class Meta:
        ordering = ('createdAt',)