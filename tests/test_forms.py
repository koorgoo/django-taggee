from django.test import TestCase
from .forms import EmptyTagForm, TagForm


class TagFormTestCase(TestCase):
    """ The TagForm form derives from 'taggee.TagFieldFormMixin'.
        This mixin brings required functionality to set correct value
        in model with 'taggee.TagField'
    """
    def setUp(self):
        self.form = TagForm()
