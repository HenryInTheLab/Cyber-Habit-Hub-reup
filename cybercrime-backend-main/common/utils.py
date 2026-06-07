import datetime
from urllib.parse import urlencode

import ulid
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.http import Http404
from django.shortcuts import get_object_or_404
from rest_framework import serializers


def make_mock_object(**kwargs):
    """
    Creates a simple mock object with the given attributes.
    """
    return type("", (object,), kwargs)

def get_object(model_or_queryset, **kwargs):
    """
    Reuse get_object_or_404 since the implementation supports both Model && queryset.
    Catch Http404 & return None
    """
    try:
        return get_object_or_404(model_or_queryset, **kwargs)
    except Http404:
        return None

def assert_settings(required_settings, error_message_prefix=""):
    """
    Checks if each item from `required_settings` is present in Django settings
    """
    not_present = []
    values = {}

    for required_setting in required_settings:
        if not hasattr(settings, required_setting):
            not_present.append(required_setting)
            continue
        values[required_setting] = getattr(settings, required_setting)

    if not_present:
        if not error_message_prefix:
            error_message_prefix = "Required settings not found."
        stringified_not_present = ", ".join(not_present)
        raise ImproperlyConfigured(f"{error_message_prefix} Could not find: {stringified_not_present}")
    return values

def create_serializer_class(name, fields):
    """
    Dynamically creates a DRF Serializer class with the given name and fields.
    """
    return type(name, (serializers.Serializer,), fields)

def inline_serializer(*, fields, data=None, **kwargs):
    """
    Creates and optionally instantiates a dynamic DRF Serializer with the given fields.
    """
    serializer_class = create_serializer_class(name=str(ulid.new()),fields=fields)
    if data is not None:
        return serializer_class(data=data, **kwargs)
    return serializer_class(**kwargs)

def build_url(base, path="", params=None):
    """
    Builds a URL from a base, optional path, and optional query parameters.
    """
    url = f"{base}{path}"
    if params:
        query_string = urlencode(params)
        url = f"{url}?{query_string}"
    return url

def extract_fields(obj, fields):
    """
    Extracts specified fields from any object, formatting datetime fields as ISO strings.
    """
    def format_value(value):
        if isinstance(value, list):
            return [format_value(v) for v in value]
        if isinstance(value, (datetime.date, datetime.datetime)):
            return value.isoformat()
        return value

    return {
        field: format_value(getattr(obj, field, None))
        for field in fields
    }