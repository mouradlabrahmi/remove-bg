import factory
from factory.django import DjangoModelFactory

from rmbg.models import Image


class ImageFactory(DjangoModelFactory):
    class Meta:
        model = Image

    name = factory.Faker("first_name")
    # url = factory.Faker("www.google.com")
    picture = factory.django.ImageField(from_path="rmbg/tests/assets/car.jpg")
