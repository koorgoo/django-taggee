from django import forms
from taggee.forms import TagFormMixin
from .models import TagModel


class EmptyTagForm(TagFormMixin, forms.Form):
    pass


class TagForm(TagFormMixin, forms.Form):
    tags = forms.CharField()


class EmptyTagModelForm(TagFormMixin, forms.ModelForm):
    class Meta:
        model = TagModel
        fields = []


class TagModelForm(TagFormMixin, forms.ModelForm):
    class Meta:
        model = TagModel
