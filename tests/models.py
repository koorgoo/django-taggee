from django.db import models
from taggee import TagField


class TagModel(models.Model):
    tags = TagField()
