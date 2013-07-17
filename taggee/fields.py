import re
from django.db import models
from django.utils.six import with_metaclass


def split_tags(s, pattern='\s*,\s*', is_re=True):
    if is_re:
        tags = re.split(pattern, s)
    else:
        tags = s.split(pattern)
    return [t.strip() for t in tags if t]


class TagField(models.CharField):
    description = 'Tag (string) array field'

    __metaclass__ = models.SubfieldBase

    def __init__(self, *args, **kwargs):
        self.separator = kwargs.pop('separator', '|')
        self.form_separator = kwargs.pop('form_separator', ', ')
        kwargs['max_length'] = kwargs.get('max_length', 255)
        kwargs['blank'] = kwargs.get('blank', True)
        super(TagField, self).__init__(*args, **kwargs)

    def get_prep_value(self, value):
        if isinstance(value, list):
            value = self.separator.join(value)
        return value

    def get_prep_lookup(self, lookup_type, value):
        value = self.get_prep_value(value)
        return super(TagField, self).get_prep_lookup(lookup_type, value)

    def to_python(self, value):
        """ Due to subclassing from the SubfieldBase class
            the method is called every time
            the instance of the field is assigned a value.
        """
        if isinstance(value, list):
            return value

        value = super(TagField, self).to_python(value)
        if self.separator in value:
            value = split_tags(value, self.separator, False)
        else:
            value = split_tags(value)
        return value

    def value_from_object(self, obj):
        value = getattr(obj, self.attname)
        if isinstance(value, list):
            value = self.form_separator.join(value)
        return value
