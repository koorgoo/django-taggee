django-taggee
=============

**django-taggee** is a Django package providing with a simple tag field implementation.

Installation
------------

1. Install from GitHub
::
    pip install git+git://github.com/koorgoo/django-taggee.git#egg=django-taggee
::

2. Add in INSTALLED_APPS in settings.
::
    INSTALLED_APPS = (
        # other apps
        'taggee',
    )
::

3. Add field to your model
::
    from django.db import models
    from taggee import TagField
    
    class Fruit(models.Model):
        name = models.CharField(max_length=100)
        tags = TagField()
::


Description
-----------

| **TagField** uses :code:`django.forms.TextWidget` to change its value.
| To add several tags you should type desired tags separated by comma.
| For example, the ``orange, juicy`` input will set the **tags** field's value to ``['orange', 'juicy']``.

| Now you can easily loop through models's **tags** to build appropriate HTML in templates.

::

    {% if object.tags %}
        <ul class="tag-list">
            {% for tag in object.tags %}
            <li class="tag-item">{{ tag }}</li>
            {% endfor %}
        </ul>
    {% endif %}
::










