from crispy_forms.helper import FormHelper
from django import forms
from fluent_comments.forms import CompactLabelsCommentForm

from .models import Date, Description


class CommentForm(CompactLabelsCommentForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["comment"].widget.attrs["rows"] = 5


class DescriptionForm(forms.ModelForm):
    value = forms.CharField(
        required=False,
        label=False,
        widget=forms.Textarea(
            attrs={
                "rows": 5,
                "placeholder": "Enter a description...",
                # "autofocus": "autofocus",
                "x-data": "{}",
                "x-ref": "textarea",
                "x-init": "$nextTick(() => $refs.textarea.style.height = $refs.textarea.scrollHeight + 'px')",
                "x-on:input": "$refs.textarea.style.height = 'auto'; $refs.textarea.style.height = $refs.textarea.scrollHeight + 'px';",
                "style": "overflow: hidden; resize: none;",
                "class": "w-100 border-0",
            }
        ),
    )

    class Meta:
        model = Description
        fields = ["value", "type"]
        widgets = {
            "type": forms.HiddenInput,
        }

    def __init__(self, model=None, request=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.render_hidden_fields = True


class DateForm(forms.ModelForm):
    class Meta:
        model = Date
        fields = ["value", "type"]
        widgets = {
            "type": forms.HiddenInput,
            "value": forms.TextInput(attrs={"x-mask": "****/**/**", "placeholder": "YYYY/MM/DD"}),
        }

    def __init__(self, model=None, request=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["value"].label = kwargs.get("initial", {}).get("type", "Date")
