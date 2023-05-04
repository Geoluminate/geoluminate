from crispy_forms.layout import Field, Layout
from fluent_comments.forms import CommentFormHelper, FluentCommentForm


class SuperCommentForm(FluentCommentForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = CommentFormHelper(self)
        self.helper.form_show_labels = False
        self.helper.layout = Layout(
            Field("comment", rows="5", placeholder="Start typing here..."),
        )
