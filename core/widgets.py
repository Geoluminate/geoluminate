from crispy_forms.layout import Field

class CustomCheckbox(Field):
    """Properly renders the bootstrap 5 checkbox"""
    template = 'forms/checkbox.html'