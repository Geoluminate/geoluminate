from crispy_forms.helper import FormHelper
from crispy_forms.layout import Button, Div, Field, Layout
from django import forms
from fluent_comments.forms import CompactLabelsCommentForm


class CommentForm(CompactLabelsCommentForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["comment"].widget.attrs["rows"] = 5


# ===================== FORMS =====================

FORM_ACTIONS = (
    Div(
        Button("submit", "Save", css_class="btn-primary", form="description-form"),
        css_class="text-right",
        css_id="form-actions",
        hx_swap_oob="true",
    ),
)


class DescriptionForm(forms.ModelForm):
    text = forms.CharField(
        label=False,
        widget=forms.Textarea(attrs={"rows": 8}),
    )

    class Meta:
        fields = ["object", "type", "text"]
        widgets = {
            "object": forms.HiddenInput,
            "type": forms.HiddenInput,
            # "text": TextEditorWidget(),
        }

    def __init__(self, model=None, request=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = "description-form"
        self.helper.render_hidden_fields = True
        self.fields["type"].widget.choices = model.type_vocab.choices
        self.fields["object"].initial = request.GET.get("pk")
        self.helper.layout = Layout(
            Field("text", wrapper_class="m-0"),
            FORM_ACTIONS,
        )
