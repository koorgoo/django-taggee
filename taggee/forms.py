from django import forms


class TagFormMixin(forms.Form):
    tag_field = 'tags'
