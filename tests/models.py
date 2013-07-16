from django.db import models
from taggee import TagField


class TagModel(models.Model):
    tags = TagField()


class TagModel2(models.Model):
    tags = TagField(form_separator=' | ')

