*tekextensions* is made for Django 1.11+.

admin popups
====================
> if using grappeli, copy RelatedObjectLookups.js to your admin_media folder from django's admin media 

settings.py
-----------
> *tekextensions* relies on the Django static package.

    STATIC_ROOT = ...
    STATIC_URL = ...
    STATICFILES_DIRS = ...
    STATICFILES_FINDERS = ..._
    TEMPLATE_CONTEXT_PROCESSORS = (
        'tekextensions.context_processors.static_url_prefix',
    )
    INSTALLED_APPS = (
        'tekextensions',
    )
    
Fill in the STATIC variables as appropriate.

urls.py
--------------------
    url(r'^add/(?P<model_name>\w+)/?$', 'tekextensions.views.add_new_model'),

forms.py
--------------------
> override any ModelChoiceField widget with SelectWithPopUp

    from tekextensions.widgets import SelectWithPopUp
    from django import forms
    from .models import MyModel
    
    class CustomForm(forms.Form):
        company = forms.ModelChoiceField(CustomModel.objects, widget=SelectWithPopUp)

    class CustomModelForm(forms.ModelForm):
        class Meta:
            model=MyModel
            widgets = {
                'field1': SelectWithPopup,
                'field2': SelectWithPopup(model='AnotherModel')
            }

If you decide to specify the template argument to SelectWithPopup(), your template will need to contain the following in order to
create the green plus sign link just as Django Admin does:

    {% load static %}
    <a href="/add/{{ model }}/" class="add-another" id="add_id_{{ field }}" onclick="return showAddAnotherPopup(this);">
        <img src="{% static 'admin/img/icon_addlink.gif' %}">
    </a>

The _model_ and _field_ values will be filled in automatically as the template is rendered.

html
----
> create HTML template for the popup

By default, the template is named _popup.html_. This can be overridden by sending in the template name via the url. For example:

    url(r'^add/(?P<model_name>\w+)/?$', 'tekextensions.views.add_new_model', {'template': 'my_template'})
    
An example of a simple template:

    {% load staticfiles %}

    <html>
        <head>
            <title>Add {{ field }}</title>
            <script src="{% static 'admin/js/admin/RelatedObjectLookups.js' %}"></script>
        </head>
    
        <body>
            <h1>Add {{ field }}</h1>
    
            <form method="POST" action="/add/{{ field }}">
                {% csrf_token %}
    
                <table>
                    {{ form.as_table }}
                </table>
    
                <div style="margin-top: 1em;">
                    <input type="submit" value="Add" /> | <a href="javascript:window.close()">Cancel</a>
                </div>
            </form>
        </body>
    </html>
