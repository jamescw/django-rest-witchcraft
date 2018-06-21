# -*- coding: utf-8 -*-
"""
Some SQLAlchemy specific field types.
"""
# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

from rest_framework import fields, relations


class UriField(relations.HyperlinkedIdentityField):
    """
    Represents a uri to the resource
    """

    def get_url(self, obj, view_name, request, format):
        """
        Same as basic HyperlinkedIdentityField except return uri vs full url.
        """
        return super(UriField, self).get_url(obj, view_name, None, format)


class EnumField(fields.ChoiceField):
    """
    Used for SQLAlchemy's Enum column type used in either mapping python Enum's, or
    a list of valid fields for the column.
    """

    def __init__(self, **kwargs):
        self.enum_class = kwargs.pop("enum_class")
        kwargs["choices"] = [(e.name, e.name) for e in self.enum_class]
        kwargs.pop("max_length", None)
        super(EnumField, self).__init__(**kwargs)

    def to_internal_value(self, data):
        try:
            return self.enum_class(data)

        except (KeyError, ValueError):
            self.fail("invalid_choice", input=data)

    def to_representation(self, value):
        if not value:
            return None

        return value.value


class CharMappingField(fields.DictField):
    """
    Used for Postgresql HSTORE columns for storing key-value pairs.
    """

    child = fields.CharField(allow_null=True)
