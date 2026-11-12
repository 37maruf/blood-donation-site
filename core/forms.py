from django import forms

from .bn import translate


class TranslatingSelect(forms.Select):
    """A <select> whose option labels are shown in Bangla when Bangla is the active language."""

    def create_option(self, name, value, label, *args, **kwargs):
        return super().create_option(name, value, translate(label), *args, **kwargs)


class BootstrapMixin:
    """Adds Bootstrap 5 classes to every widget."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            widget = field.widget
            if isinstance(widget, forms.CheckboxInput):
                css = "form-check-input"
            elif isinstance(widget, (forms.Select, forms.SelectMultiple)):
                css = "form-select"
                if type(widget) is forms.Select:
                    widget.__class__ = TranslatingSelect
            else:
                css = "form-control"
            widget.attrs["class"] = f"{widget.attrs.get('class', '')} {css}".strip()


DATE_WIDGET = forms.DateInput(attrs={"type": "date"}, format="%Y-%m-%d")
DATETIME_LOCAL = forms.DateTimeInput(attrs={"type": "datetime-local"}, format="%Y-%m-%dT%H:%M")
