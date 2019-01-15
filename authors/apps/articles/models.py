from django.db import models

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
    createdAt = models.DateTimeField(auto_now=True)
    updatedAt = models.DateTimeField(auto_now=True)
    favorited = models.BooleanField()
    favoritesCount = models.PositiveIntegerField()
    author = models.IntegerField()

    def __str__(self):
        return self.title