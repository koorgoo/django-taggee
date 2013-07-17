django-taggee
=============

**django-taggee** is a Django package providing with a simple tag field implementation.

Getting Started
---------------

1. Install from GitHub
::
    pip install git+git://github.com/koorgoo/django-taggee.git#egg=django-taggee
::

2. Add field to your model
::
    from django.db import models
    from taggee.fields import TagField
    
    class Fruit(models.Model):
        name = models.CharField(max_length=100)
        tags = TagField()
::
