from datetime import datetime

from django.contrib.auth import get_user_model
from django.contrib.sites.shortcuts import get_current_site
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.template.defaultfilters import slugify
from .helper import FavoriteHelper, StatsHelper
from django_currentuser.middleware import get_current_user
from gunicorn.util import get_username
from notifications.models import Notification
from notifications.signals import notify
from rest_framework.reverse import reverse

from authors.apps.authentication.models import User
from authors.apps.notify.helper import Notifier
from authors.apps.profiles.models import Profile

from .helper import FavoriteHelper
from django.core.mail import send_mass_mail

from authors.apps.ratings.utils import fetch_rating_average
from authors.apps.ratings.models import Rating
from .helper import LikeHelper


class Tag(models.Model):
    tag = models.CharField(max_length=50)
    slug = models.SlugField(default=tag)
    created = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.tag


class Article(models.Model):
    helper = LikeHelper()
    favorite_helper = FavoriteHelper()
    read_helper = StatsHelper()
    title = models.CharField(max_length=100)
    slug = models.SlugField(null=True)
    description = models.CharField(max_length=300)
    body = models.TextField()
    tagList = models.ManyToManyField(Tag)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE, null=False
    )

    @property
    def average_rating(self):
        return fetch_rating_average(Rating, self.pk).get('points__avg')

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

    @property
    def read_count(self):
        return self.read_helper.read_count(
            model=ReadingStats,
            article_id=self.pk
        )

    def likes(self):
        return self.helper.get_likes_or_dislike(
            model=LikeArticle,
            like=True,
            article_id=self.pk
        )

    @property
    def dislikes(self):
        return self.helper.get_likes_or_dislike(
            model=LikeArticle,
            like=False,
            article_id=self.pk
        )


class LikeArticle(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    like = models.BooleanField(default=False)
    created_at = models.DateField(auto_now_add=True)
    modified_at = models.DateField(auto_now=True)


class ArticleImage(models.Model):
    article = models.ForeignKey(
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


class BookmarkArticle(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(
        get_user_model(), on_delete=models.CASCADE,
        null=True
    )


class ReadingStats(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, null=True)
    author = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        null=True
    )
    read_on = models.DateTimeField(auto_now=True)


class HighlightedText(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, null=True)
    author = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE, null=True
    )
    startIndex = models.IntegerField()
    endIndex = models.IntegerField()
    comment = models.TextField(blank=True)
    created = models.DateTimeField(auto_now=True)

    @property
    def selected_text(self):
        return Article.objects.get(
            id=self.article_id
        ).body[self.startIndex:self.endIndex]


@receiver(post_save, sender=Article)
def article_notifications_handler(sender, **kwargs):
    # notification
    article_instance = kwargs['instance']
    author = article_instance.author
    profile = Profile.objects.get(user=author)
    followers = profile.followers.all()

    article_url = "api/v1/articles/{}".format(article_instance.slug)
    url = reverse('mail-list-status')

    Notifier.batch_follower_email_notifier(
        author, followers, article_url=article_url, url=url)
