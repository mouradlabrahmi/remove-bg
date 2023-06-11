import graphene
from graphene_file_upload.scalars import Upload

from rmbg.forms import CreateImageMutationForm
from rmbg.models import Image
from rmbg.utils import removebg

from . import types

# from urllib import request, parse

# def path2url(path):
#     return parse.urljoin(
#       'file:', request.pathname2url(path))


class CreateImage(graphene.Mutation):
    form = CreateImageMutationForm

    class Arguments:
        name = graphene.String()
        picture = Upload(required=True)

    image = graphene.Field(types.ImageType)
    success = graphene.Boolean()
    output_path = graphene.String()

    def mutate(self, info, picture=None, **data):
        """Mutate method."""
        file_data = {}
        if picture:
            file_data = {"picture": picture}

        # https://docs.djangoproject.com/en/3.2/ref/forms/api/#binding-uploaded-files-to-a-form
        # Binding file data to the Form.
        f = CreateImage.form(data, file_data)
        if f.is_valid():
            f.save()
            image = Image.objects.last()
            input_path = image.picture.url
            image_bg_removed_path = f"/media/Outputs/{image.name}_bg_removed.png"
            removebg(input_path[1:], image_bg_removed_path[1:])
            # url_rbg = path2url(image_bg_removed_path)
            return CreateImage(
                image=image, success=True, output_path=image_bg_removed_path
            )
        else:
            return CreateImage(success=False, errors=f.errors.get_json_data())


# class CreateImage(graphene.Mutation):
#     image = graphene.Field(types.ImageType)

#     class Arguments:
#         name = graphene.String()
#         url = graphene.String()
#         picture = graphene.String()

#     def mutate(self, info, image, **kwargs):
#         breakpoint()
#         image = Image.objects.create(**kwargs)
#         return CreateImage(image=image)


# class RemoveBackground(graphene.Mutation):
#     success = graphene.Boolean()

#     class Arguments:
#         pk = graphene.ID()

#     def mutate(self, info, **kwargs):
#         pk = kwargs.pop("pk")
#         image = Image.objects.get(id=pk)
#         input_path = image.picture.url
#         image_bg_removed_path = f"Output/{image.name}_bg_removed.png"
#         removebg(input_path[1:], image_bg_removed_path)
#         return RemoveBackground(success=True)


class ImageMutation(object):
    create_image = CreateImage.Field()
    # remove_background = RemoveBackground.Field()
