from django.apps import apps
from django.forms.models import modelform_factory


def normalize_model_name(model_name):
    return model_name.capitalize() if model_name.lower() == model_name else model_name


def get_model_form(model_name):
    for model in apps.get_models():
        if model.__name__ == model_name: 
            return modelform_factory(model, exclude=[])

    raise Exception('Did not find the model %s' % model_name)

