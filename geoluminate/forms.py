from email.policy import default
from django.utils.translation import gettext_lazy as _
from fluent_comments.forms import CommentFormHelper, FluentCommentForm
from crispy_forms.layout import Layout, Field


class SuperCommentForm(FluentCommentForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = CommentFormHelper(self)
        self.helper.form_show_labels = False
        self.helper.layout = Layout(

            Field('comment', rows='5', placeholder='Start typing here...'),
        )
