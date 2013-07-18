import re
from django.db import models
from django import forms
from django.utils.translation import ugettext_lazy as _


class TagField(models.TextField):
    description = _('Tags as text field')

    __metaclass__ = models.SubfieldBase

    def __init__(self, *args, **kwargs):
        self.separator = kwargs.pop('separator', '|')
        kwargs['blank'] = kwargs.get('blank', True)
        super(TagField, self).__init__(*args, **kwargs)

    def get_prep_value(self, value):
        if isinstance(value, list):
            value = self.separator.join(value)
        return value

    def get_prep_lookup(self, lookup_type, value):
        return self.get_prep_value(value)

    def to_python(self, value):
        if not isinstance(value, list):
            value = value.split(self.separator)
        return value

    def value_from_object(self, obj):
        value = super(TagField, self).value_from_object(obj)
        if isinstance(value, list):
            complex_tags = [t for t in value if ' ' in t]
            if complex_tags:
                value = ', '.join(value)
            else:
                value = ' '.join(value)
        return value

    def formfield(self, **kwargs):
        defaults = {'widget': forms.TextInput}
        defaults.update(kwargs)
        return super(TagField, self).formfield(**defaults)
