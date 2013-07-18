django-taggee
=============

**django-taggee** is a Django package providing with a simple tag field implementation.

.. image:: https://api.travis-ci.org/koorgoo/django-taggee.png

Getting Started
---------------

Installation
^^^^^^^^^^^^
::

    pip install django-taggee
::


Usage in Models
^^^^^^^^^^^^^^^
::

    from django.db import models
    from taggee.fields import TagField
    
    class Fruit(models.Model):
        name = models.CharField(max_length=100)
        tags = TagField()
::

Usage in ModelForms
^^^^^^^^^^^^^^^^^^^^
To allow ModelForm to parse submitted tags derive it from ``taggee.forms.TagFormMixin``.
::

    from django import forms
    from taggee.forms import TagFormMixin
    from .models import Fruit
    
    class FruitForm(TagFormMixin, forms.ModelForm):
        class Meta:
            model = Fruit
::
