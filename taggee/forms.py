
class TagFormMixin(object):
    def __init__(self, *args, **kwargs):
        tag_field = kwargs.pop('tag_field', 'tags')
        tag_separators = kwargs.pop('tag_separators', ',')
        clean_method_name = 'clean_%s' % tag_field
        clean_method = self.clean_tags_method(tag_field, tag_separators)
        setattr(self, clean_method_name, clean_method)
        super(TagFormMixin, self).__init__(*args, **kwargs)

    def clean_tags_method(self, tag_field, tag_separators):
        def clean():
            value = self.cleaned_data[tag_field]
            space = ' '
            separators = tag_separators + space
            for separator in separators:
                dirty_tags = [t.strip() for t in value.split(separator)]
                tags = [t for t in dirty_tags if t]
                if separator is space and len(tags) == 1:
                    return tags
                elif len(tags) == 1:
                    continue
                return tags
        return clean
