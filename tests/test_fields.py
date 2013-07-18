from django.db import models
from django import forms
from django.test import SimpleTestCase, TransactionTestCase
from taggee.fields import TagField
from .models import TagModel


class TagFieldTestCase(SimpleTestCase):
    def setUp(self):
        self.tags = TagField()
        self.model = TagModel()

    def test_default_separator(self):
        self.assertEqual('|', self.tags.separator)

    def test_separator_parameter(self):
        tags = TagField(separator=',')
        self.assertEqual(',', tags.separator)

    def test_default_blank(self):
        self.assertTrue(self.tags.blank)

    def test_blank_parameter(self):
        tags = TagField(blank=False)
        self.assertFalse(tags.blank)

    def test_to_python_string(self):
        actual = self.tags.to_python('tag1|tag2')
        expected = ['tag1', 'tag2']
        self.assertEqual(expected, actual)

    def test_to_python_list(self):
        actual = self.tags.to_python(['tag1', 'tag2'])
        expected = ['tag1', 'tag2']
        self.assertEqual(expected, actual)


class TagModelTestCase(TransactionTestCase):
    def setUp(self):
        TagModel.objects.create(tags='tag1')
        TagModel.objects.create(tags='tag2|tag3')
        TagModel.objects.create(tags='tag1|tag2|tag3|tag4')

    def test_model_field_from_tag_string(self):
        model = TagModel(tags='tag1|tag2')
        self.assertEqual(['tag1','tag2'], model.tags)

    def test_model_field_from_tag_list(self):
        model = TagModel(tags=['tag1','tag2'])
        self.assertEqual(['tag1','tag2'], model.tags)

    def test_model_saves_and_parses_tags(self):
        model = TagModel.objects.create(tags=['tag1','tag2'])
        self.assertEqual(['tag1', 'tag2'], TagModel.objects.get(pk=model.pk).tags)

    def test_filter_equals_is_ok(self):
        self.assertEqual(1, TagModel.objects.filter(tags='tag1').count())
        self.assertEqual(1, TagModel.objects.filter(tags=['tag2','tag3']).count())
        self.assertEqual(1, TagModel.objects.filter(tags='tag2|tag3').count())

    def test_filter_exact_is_ok(self):
        self.assertEqual(1, TagModel.objects.filter(tags__exact='tag1').count())
        self.assertEqual(1, TagModel.objects.filter(tags__exact=['tag2','tag3']).count())
        self.assertEqual(1, TagModel.objects.filter(tags__exact='tag2|tag3').count())

    def test_filter_iexact_is_ok(self):
        self.assertEqual(1, TagModel.objects.filter(tags__iexact='TAG1').count())
        self.assertEqual(1, TagModel.objects.filter(tags__iexact=['TAG2','TAG3']).count())
        self.assertEqual(1, TagModel.objects.filter(tags__iexact='TAG2|TAG3').count())

    def test_filter_contains_is_ok(self):
        self.assertEqual(2, TagModel.objects.filter(tags__contains='tag3').count())
        self.assertEqual(1, TagModel.objects.filter(tags__contains=['tag3','tag4']).count())
        self.assertEqual(1, TagModel.objects.filter(tags__contains='tag3|tag4').count())

    def test_filter_icontains_is_ok(self):
        self.assertEqual(2, TagModel.objects.filter(tags__icontains='TAG3').count())
        self.assertEqual(1, TagModel.objects.filter(tags__icontains=['TAG3','TAG4']).count())
        self.assertEqual(1, TagModel.objects.filter(tags__icontains='TAG3|TAG4').count())
