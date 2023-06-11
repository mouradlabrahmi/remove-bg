import graphene
from django.core.files.images import ImageFile
from django.utils.translation import ugettext_lazy as _
from django_graphene_permissions import permissions_checker
from graphene import relay
from graphene.utils.thenables import maybe_thenable
from graphql import GraphQLError


class Upload(graphene.types.Scalar):
    @staticmethod
    def serialize(value):
        return value

    @staticmethod
    def parse_literal(node):
        return node

    @staticmethod
    def parse_value(value):
        return value


class ImageUpload(Upload):

    ALLOWED_EXTENSIONS = ["png", "jpg", "jpeg", "bmp", "svg"]
    IMAGE_MAX_SIZE = 4194304  # 4MB

    @classmethod
    def parse_value(cls, value):
        if value.name.split(".")[-1].lower() not in cls.ALLOWED_EXTENSIONS:
            raise GraphQLError(_("Wrong image extension"))

        if value.size > cls.IMAGE_MAX_SIZE:
            raise GraphQLError(_("Maximum file size exceeded"))

        return ImageFile(value)


class ValidatedMutation(relay.ClientIDMutation):

    permissions_classes = None

    class Meta:
        abstract = True

    @classmethod
    def __init_subclass_with_meta__(cls, **kwargs):
        super(ValidatedMutation, cls).__init_subclass_with_meta__(**kwargs)
        mutation_handler = cls.mutate_and_get_payload
        if cls.permissions_classes:
            mutation_handler = permissions_checker(cls.permissions_classes)(
                mutation_handler
            )

        cls._mutation_handler = mutation_handler

    @classmethod
    def mutate_and_get_payload(cls, root, info, **input_data):
        # This traverses all of the fields on the
        from graphql_core.utils import validate_input_data

        input_cls = cls._meta.arguments["input"]
        validated_data = validate_input_data(
            input_cls, info, input_data, mutation_cls=cls
        )

        validated_data = cls.validate_data(info, validated_data)

        payload_kwargs = cls.save(root, info, validated_data)
        return cls(**payload_kwargs)

    @classmethod
    def validate_data(cls, info, validated_data):
        return validated_data

    @classmethod
    def mutate(cls, root, info, input):
        def on_resolve(payload):
            try:
                payload.client_mutation_id = input.get("client_mutation_id")
            except Exception:
                raise Exception(
                    f"Cannot set client_mutation_id in the payload object {repr(payload)}"
                )
            return payload

        result = cls._mutation_handler(root, info, **input)
        return maybe_thenable(result, on_resolve)

    @classmethod
    def save(cls, root, info, validated_data):
        raise NotImplementedError
