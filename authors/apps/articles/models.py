from datetime import datetime
from django.db import models
from django.contrib.auth import get_user_model
from django.template.defaultfilters import slugify


class Article(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField(null=True)
    description = models.CharField(max_length=300)
    body = models.TextField()
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE, null=False
    )
    
    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.pk:
            self.slug = slugify(self.title)
            while Article.objects.filter(slug=self.slug).exists():
                article_pk = Article.objects.latest('pk').pk + 1
                self.slug = f'{self.slug}-{article_pk}'            

        super(Article, self).save(*args, **kwargs)

    class Meta:
        ordering = ('createdAt',)


class ArticleImage(models.Model):
    property = models.ForeignKey(
        Article,
        related_name='images',
        on_delete=models.CASCADE
    )
    image = models.ImageField()
