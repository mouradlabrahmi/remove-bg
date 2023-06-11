import logging

import graphene
from django.core.exceptions import ValidationError
from graphene.utils.str_converters import to_camel_case

logger = logging.getLogger(__name__)


def is_validated_input_field(field):
    from graphql_core.inputs.base import BaseValidatedInput

    # Handle case where field defined like:
    # field = ValidatedInputField(required=True)
    if isinstance(field, BaseValidatedInput):
        return True, field

    # Handle case where input defined like:
    # field = graphene.Field(ValidatedInput, required=True)
    #    or
    # field = graphene.Field(ValidatedInput)
    field_type = field.type
    if isinstance(field.type, graphene.NonNull):
        field_type = field.type.of_type

    if isinstance(field_type, BaseValidatedInput):
        # FIXME
        raise NotImplementedError

    try:
        is_validated_input = issubclass(field_type, BaseValidatedInput)
    except TypeError:
        is_validated_input = False

    if is_validated_input:
        field_type = field_type()

    return is_validated_input, field_type


def raise_gql_validation_errors(errors: dict):
    # The ValidationError logic / the GraphQLErrors don't play nicely with nested errors
    # so flatten them out
    if not errors:
        return

    mapped_errors = {}
    for field, error in errors.items():
        if hasattr(error, "error_dict"):
            for sub_field, sub_error in error.error_dict.items():
                mapped_errors[f"{field}.{sub_field}"] = sub_error
        else:
            mapped_errors[field] = error

    raise ValidationError(mapped_errors)


def validate_input_data(input_cls, info, input_data, mutation_cls=None):
    errors = {}
    validated_data = {}

    for fname, field in input_cls._meta.fields.items():
        value = input_data.get(fname)
        if value is None:
            # Optional fields that have defaults do not get their defaults used if the user
            # passes in an explicit `None` for that value. Adjust behavior so that if the
            # user passes and explicit `None` that the `default_value` gets used instead of
            # the explicit `None`
            if field.default_value is not None:
                value = (
                    field.default_value()
                    if callable(field.default_value)
                    else field.default_value
                )

        # If the value is None and the field is required then the graphql executor
        # would have already thrown an exception that this cannot be None
        if value is None:
            if isinstance(field.type, graphene.NonNull):
                errors[to_camel_case(fname)] = ValidationError(
                    "Cannot be null.", code="required"
                )
            else:
                validated_data[fname] = value

            continue

        is_validated_input, field_type = is_validated_input_field(field)

        if is_validated_input:
            try:
                value = field_type._validate_value(value, info)
            except Exception as e:
                errors[to_camel_case(fname)] = e
                continue

        validators = []
        if hasattr(input_cls, f"validate_{fname}"):
            validators.append(getattr(input_cls, f"validate_{fname}"))

        if mutation_cls and hasattr(mutation_cls, f"validate_{fname}"):
            validators.append(getattr(mutation_cls, f"validate_{fname}"))

        validated_value = value
        had_errors = False
        for validator in validators:
            try:
                validated_value = validator(validated_value, info)
            except Exception as e:
                errors[to_camel_case(fname)] = e
                had_errors = True
                break

        if had_errors:
            continue

        validated_data[fname] = validated_value

    raise_gql_validation_errors(errors)

    return validated_data
