from django import forms
from taggee.forms import TagFormMixin


class EmptyTagForm(TagFormMixin, forms.Form):
    pass


class TagForm(TagFormMixin, forms.Form):
    tags = forms.CharField()
