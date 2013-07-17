from django import forms
from taggee.forms import TagFormMixin
from .models import TagModel


class EmptyTagForm(TagFormMixin, forms.Form):
    pass


class TagForm(TagFormMixin, forms.Form):
    tags = forms.CharField()


class TagModelForm(TagFormMixin, forms.Form):
    class Meta:
        model = TagModel
