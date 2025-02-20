from fluent_comments.forms import CompactLabelsCommentForm


class CommentForm(CompactLabelsCommentForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["comment"].widget.attrs["rows"] = 5
