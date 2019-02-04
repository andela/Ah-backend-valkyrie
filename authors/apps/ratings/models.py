from django.db import models
from django.core.validators import (
    MinValueValidator, MaxValueValidator
)

from authors.apps.authentication.models import User

# Create your models here.


class Rating(models.Model):

    points = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)])
    rater = models.ForeignKey(User, on_delete=models.CASCADE)
    article = models.ForeignKey('articles.Article', on_delete=models.CASCADE)
