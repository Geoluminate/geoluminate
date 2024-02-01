from fluent_comments.forms import CompactLabelsCommentForm
from formset.renderers import bootstrap


class DefaultFormRenderer(bootstrap.FormRenderer):
    def __init__(self, **kwargs):
        kwargs.setdefault("form_css_classes", "row")
        kwargs.setdefault("fieldset_css_classes", "row")
        kwargs.setdefault("field_css_classes", {"*": "mb-3 col-12"})
        # kwargs.setdefault("control_css_classes", "form-control")
        # kwargs.setdefault("collection_css_classes", {"*": "col-12"})
        super().__init__(**kwargs)

    # form_css_classes = "row"
    # field_css_classes = {"*": "mb-3 col-12"}
    # label_css_classes="pb-2",
    # fieldset_css_classes={"*": "col-12"},
    # control_css_classes="form-control",
    # collection_css_classes={"*": "col-12"}


class CommentForm(CompactLabelsCommentForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["comment"].widget.attrs["rows"] = 5
