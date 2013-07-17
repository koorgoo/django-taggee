from django.test import TestCase
from .forms import EmptyTagForm, TagForm


class TagFormTestCase(TestCase):
    def test_no_exception_when_no_tag_field(self):
        empty_form = EmptyTagForm({'tags': 'tag1, tag2'})
        self.assertTrue(empty_form.is_valid())

    def test_comma_is_a_default_nonspace_separator(self):
        data = {'tags': 'tag1 , tag2'}
        form = TagForm(data)
        self.assertTrue(form.is_valid())
        self.assertEqual(['tag1','tag2'], form.cleaned_data['tags'])

    def test_split_tags_by_separator(self):
        data = {'tags': 'tag1 | tag2'}
        form = TagForm(data, tag_separators='|')
        self.assertTrue(form.is_valid())
        self.assertEqual(['tag1','tag2'], form.cleaned_data['tags'])

    def test_split_tags_by_second_separator(self):
        data = {'tags': 'tag1 | tag2'}
        form = TagForm(data, tag_separators=',|')
        self.assertTrue(form.is_valid())
        self.assertEqual(['tag1','tag2'], form.cleaned_data['tags'])

    def test_split_tags_by_spaces_when_impossible_by_separator(self):
        data = {'tags': 'tag1   tag2'}
        form = TagForm(data, tag_separators=',;')
        self.assertTrue(form.is_valid())
        self.assertEqual(['tag1','tag2'], form.cleaned_data['tags'])

    def test_omit_leading_and_trailing_spaces(self):
        data = {'tags': '     tag     '}
        form = TagForm(data)
        self.assertTrue(form.is_valid())
        self.assertEqual(['tag'], form.cleaned_data['tags'])

    def test_split_tags_and_filter_empty(self):
        data = {'tags': ' , tag1, tag2, '}
        form = TagForm(data)
        self.assertTrue(form.is_valid())
        self.assertEqual(['tag1','tag2'], form.cleaned_data['tags'])
