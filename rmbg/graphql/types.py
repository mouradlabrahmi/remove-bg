import graphene
from graphene_django.types import DjangoObjectType

from rmbg import models


class ImageType(DjangoObjectType):
    picture = graphene.String()

    class Meta:
        model = models.Image
        fields = (
            "id",
            "name",
            "picture",
        )

    def resolve_picture(self, info):
        return self.picture.url if self.picture else None
