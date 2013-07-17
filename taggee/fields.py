import re
from django.db import models
from django.utils.translation import ugettext_lazy as _


class TagField(models.CharField):
    description = _('Tag string (up to %(max_length)s)')

    __metaclass__ = models.SubfieldBase

    def __init__(self, *args, **kwargs):
        self.separator = kwargs.pop('separator', '|')
        kwargs['max_length'] = kwargs.get('max_length', 255)
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
