import graphene

from rmbg.models import Image

from . import types


class ImageQuery(object):
    images = graphene.List(types.ImageType)
    image = graphene.Field(types.ImageType, pk=graphene.ID())

    def resolve_images(self, info):
        return Image.objects.all()

    def resolve_image(self, info, pk):
        return Image.objects.get(pk=pk)
