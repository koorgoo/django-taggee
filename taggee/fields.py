import re
from django.db import models
from django.utils.six import with_metaclass


def split_tags(s, pattern='\s*,\s*', is_re=True):
    if is_re:
        tags = re.split(pattern, s)
    else:
        tags = s.split(pattern)
    return [t.strip() for t in tags if t]


class TagField(with_metaclass(models.SubfieldBase, models.CharField)):
    description = 'Tag (string) array field'

    def __init__(self, *args, **kwargs):
        self.db_separator = kwargs.pop('db_separator', '|')
        kwargs['max_length'] = kwargs.get('max_length', 255)
        kwargs['blank'] = kwargs.get('blank', True)
        super(TagField, self).__init__(*args, **kwargs)

    def get_db_prep_value(self, value, connection, prepared=False):
        if not prepared:
            value = self.db_separator.join(value)
        return value

    def to_python(self, value):
        """ Due to subclassing from the SubfieldBase class
            the method is called every time
            the instance of the field is assigned a value.
        """
        if isinstance(value, (list, tuple)):
            return value

        value = super(TagField, self).to_python(value)
        if self.db_separator in value:
            value = split_tags(value, self.db_separator, False)
        else:
            value = split_tags(value)
        return value

    def value_from_object(self, obj):
        value = getattr(obj, self.attname)
        if isinstance(value, (list, tuple)):
            value = ', '.join(value)
        return value
