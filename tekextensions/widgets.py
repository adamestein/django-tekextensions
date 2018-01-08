from django import forms
from django.contrib.admin.widgets import FilteredSelectMultiple
from django.template import Context, Template
from django.template.loader import render_to_string


class PopUpBaseWidget(forms.Widget):
    def __init__(self, model=None, template=None, *args, **kwargs):
        self.model = model
        self.template = template
        super(PopUpBaseWidget, self).__init__(*args, **kwargs)

    def render(self, name, *args, **kwargs):
        html = super(PopUpBaseWidget, self).render(name, *args, **kwargs)

        if not self.model:
            self.model = name

        if not self.template:
            anchor = """
{% load static %}
<a href="/add/{{ model }}/" class="add-another" id="add_id_{{ field }}" onclick="return showAddAnotherPopup(this);">
    <img src="{% static 'admin/img/icon-addlink.svg' %}">
</a>
"""
            popupplus = Template(anchor).render(Context({'field': name, 'model': self.model}))
        else:
            popupplus = render_to_string(self.template, {'field': name, 'model': self.model})

        return html + popupplus

    # noinspection PyClassHasNoInit
    class Media:
        js = ("admin/js/admin/RelatedObjectLookups.js", )


class FilteredMultipleSelectWithPopUp(PopUpBaseWidget, FilteredSelectMultiple):
    pass


class MultipleSelectWithPopUp(PopUpBaseWidget, forms.SelectMultiple):
    pass


class SelectWithPopUp(PopUpBaseWidget, forms.Select):
    pass
