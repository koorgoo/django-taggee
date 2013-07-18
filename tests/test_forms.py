from django.forms import TextInput
from django.test import TestCase
from .forms import EmptyTagForm, TagForm, EmptyTagModelForm, TagModelForm
from .models import TagModel


class EmptyFormTestCase(TestCase):
    def test_no_error_when_no_tag_field(self):
        empty_form = EmptyTagForm({'tags': 'tag1, tag2'})
        self.assertTrue(empty_form.is_valid())


class TagFormTestCase(TestCase):
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


class EmptyTagModelFormTestCase(TestCase):
    def test_no_error_when_no_tag_field(self):
        empty_form = EmptyTagModelForm({'tags': 'tag1, tag2'})
        self.assertTrue(empty_form.is_valid())


class TagModelTestCase(TestCase):
    def test_comma_is_a_default_nonspace_separator(self):
        data = {'tags': 'tag1 , tag2'}
        form = TagModelForm(data)
        self.assertTrue(form.is_valid())
        self.assertEqual(['tag1','tag2'], form.instance.tags)

    def test_split_tags_by_separator(self):
        data = {'tags': 'tag1 | tag2'}
        form = TagModelForm(data, tag_separators='|')
        self.assertTrue(form.is_valid())
        self.assertEqual(['tag1','tag2'], form.instance.tags)

    def test_split_tags_by_second_separator(self):
        data = {'tags': 'tag1 | tag2'}
        form = TagModelForm(data, tag_separators=',|')
        self.assertTrue(form.is_valid())
        self.assertEqual(['tag1','tag2'], form.instance.tags)

    def test_split_tags_by_spaces_when_impossible_by_separator(self):
        data = {'tags': 'tag1   tag2'}
        form = TagModelForm(data, tag_separators=',;')
        self.assertTrue(form.is_valid())
        self.assertEqual(['tag1','tag2'], form.instance.tags)

    def test_omit_leading_and_trailing_spaces(self):
        data = {'tags': '     tag     '}
        form = TagModelForm(data)
        self.assertTrue(form.is_valid())
        self.assertEqual(['tag'], form.instance.tags)

    def test_split_tags_and_filter_empty(self):
        data = {'tags': ' , tag1, tag2, '}
        form = TagModelForm(data)
        self.assertTrue(form.is_valid())
        self.assertEqual(['tag1','tag2'], form.instance.tags)

    def test_use_textinput_widget_for_tags(self):
        form = TagModelForm()
        tags_widget = form.fields['tags'].widget
        self.assertTrue(isinstance(tags_widget, TextInput))

    def test_use_space_to_join_one_word_tags_from_instance(self):
        model = TagModel(tags=['tag1', 'tag2'])
        form = TagModelForm(instance=model)
        self.assertEqual('tag1 tag2', form.initial['tags'])

    def test_use_comma_to_join_several_words_tags_from_instance(self):
        model = TagModel(tags=['tag', 'complex tag'])
        form = TagModelForm(instance=model)
        self.assertEqual('tag, complex tag', form.initial['tags'])
