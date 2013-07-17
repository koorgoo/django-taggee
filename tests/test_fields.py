from django.db import models
from django import forms
from django.test import SimpleTestCase, TransactionTestCase
from taggee.fields import split_tags, TagField
from .models import TagModel, TagModel2


class SplitTagsTestCase(SimpleTestCase):
    def test_re_pattern(self):
        """ Can split string with comma (default pattern).
        """
        cases = {''     : [],
                 'tag'  : ['tag'],
                 ' tag' : ['tag'],
                 'tag ' : ['tag'],
                 ' tag ': ['tag'],
                 't1 , t2': ['t1', 't2'],
                 ' t1,t2 ': ['t1', 't2']}

        for k in cases.keys():
            expected = cases[k]
            actual = split_tags(k)
            self.assertEqual(expected, actual)

    def test_non_re_pattern(self):
        """ Can split tags when they are joined with a special character.
        """
        expected = ['tag1', 'tag2']
        actual = split_tags('tag1|tag2', '|', is_re=False)
        self.assertEqual(expected, actual)


###
## Field tests.
###

class TagFieldTestCase(SimpleTestCase):
    def setUp(self):
        self.tags = TagField()
        self.model = TagModel()

    def test_default_separator(self):
        self.assertEqual('|', self.tags.separator)

    def test_separator_parameter(self):
        tags = TagField(separator=',')
        self.assertEqual(',', tags.separator)

    def test_default_form_separator(self):
        self.assertEqual(', ', self.tags.form_separator)

    def test_form_separator_parameter(self):
        tags = TagField(form_separator='; ')
        self.assertEqual('; ', tags.form_separator)

    def test_default_max_length(self):
        self.assertEqual(255, self.tags.max_length)

    def test_max_length_parameter(self):
        tags = TagField(max_length=50)
        self.assertEqual(50, tags.max_length)

    def test_default_blank(self):
        self.assertTrue(self.tags.blank)

    def test_blank_parameter(self):
        tags = TagField(blank=False)
        self.assertFalse(tags.blank)

    def test_to_python_splits_string(self):
        actual = self.tags.to_python('tag1, tag2')
        expected = ['tag1', 'tag2']
        self.assertEqual(expected, actual)

    def test_to_python_splits_db_string(self):
        db_string = 'tag1|tag2'
        actual = self.tags.to_python(db_string)
        self.assertEqual(['tag1','tag2'], actual)

    def test_db_prepare_returns_string(self):
        self.model.tags = ['tag1', 'tag2']
        prepared = self.tags.get_db_prep_value(self.model.tags, None, False)
        self.assertEqual('tag1|tag2', prepared)


###
## TagModel tests.
###

class TagModelTestCase(TransactionTestCase):
    def setUp(self):
        TagModel.objects.create(tags='tag1')
        TagModel.objects.create(tags='tag2, tag3')
        TagModel.objects.create(tags='tag1, tag2, tag3, tag4')

    def test_tags_are_created_from_string(self):
        model = TagModel.objects.create(tags='tag1, tag2')
        self.assertEqual(['tag1','tag2'], model.tags)

    def test_tags_are_created_from_list(self):
        model = TagModel.objects.create(tags=['tag1','tag2'])
        self.assertEqual(['tag1','tag2'], model.tags)

    def test_db_value_transformed_to_list(self):
        model = TagModel()
        model.tags = ['tag1', 'tag2']
        model.save()
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


###
## Form tests.
###

class TagForm(forms.ModelForm):
    class Meta:
        model = TagModel


class TagForm2(forms.ModelForm):
    class Meta:
        model = TagModel2


class TagFromTestCase(SimpleTestCase):
    def test_form_field_is_assigned_text_input_widget(self):
        form = TagForm(instance = TagModel.objects.create())
        self.assertTrue(isinstance(form.fields['tags'].widget, forms.TextInput))

    def test_form_field_is_set_from_instance(self):
        model = TagModel.objects.create(tags='tag1, tag2')
        form = TagForm(instance=model)
        form_tags = form.initial['tags']
        self.assertEqual('tag1, tag2', form_tags)

    def test_form_field_is_set_from_instance_with_custom_separator(self):
        model = TagModel2(tags='tag1, tag2')
        model.save()
        form = TagForm2(instance=model)
        form_tags = form.initial['tags']
        self.assertEqual('tag1 | tag2', form_tags)

    def test_model_field_is_set_from_form(self):
        form = TagForm({'tags': 'tag1, tag2'})
        self.assertTrue(form.is_valid())
        self.assertEqual(['tag1','tag2'], form.instance.tags)
