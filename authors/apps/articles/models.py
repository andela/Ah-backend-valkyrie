from datetime import datetime
from django.db import models
from django.contrib.auth import get_user_model
from django.template.defaultfilters import slugify
from .helper import FavoriteHelper
from django_currentuser.middleware import get_current_user


class Article(models.Model):
    favorite_helper = FavoriteHelper()
    
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
    
    @property
    def favorited(self):
        return self.favorite_helper.is_favorited(
            model=FavoriteArticle,
            article_id=self.pk,
            user_id=get_current_user().id
        )


    @property 
    def favorites_count(self):
        return self.favorite_helper.favorite_count(
            model=FavoriteArticle,
            article_id=self.pk
        )

class ArticleImage(models.Model):
    property = models.ForeignKey(
        Article,
        related_name='images',
        on_delete=models.CASCADE
    )
    image = models.ImageField()

class FavoriteArticle(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, null=True)
    author = models.ForeignKey(
        get_user_model(), 
        on_delete=models.CASCADE, null=True
    )
    Timestamp = models.DateTimeField(auto_now=True)
  

    def __str__(self):
        return self.article


     