import pytest
from faker import Faker

from rmbg.factories import ImageFactory
from rmbg.models import Image
from rmbg.tests.conftest import JsonClient, MultipartClient

faker = Faker()


@pytest.fixture
def gql_client_file():
    return MultipartClient()


@pytest.fixture
def gql_user_client():
    return JsonClient()


@pytest.mark.django_db(transaction=True)
class TestImage:
    def test_retrieve_image(self, gql_user_client):
        image = ImageFactory()

        response = gql_user_client.query(
            "image",
            arguments="pk: {}".format(image.id),
            payload="id name picture",
        )
        assert response.status_code == 200
        assert response.json()["data"]["image"]["id"] == str(image.id)
        assert response.json()["data"]["image"]["name"] == image.name
        assert response.json()["data"]["image"]["picture"] == image.picture.url

    def test_add_image(self, gql_client_file, faker):
        assert Image.objects.count() == 0
        name = faker.name()

        response = gql_client_file.mutation(
            "createImage",
            arguments='name: "{}", picture: $file'.format(name),
            payload="success image {id name picture} outputPath ",
            fp=open("rmbg/tests/assets/car.jpg", "rb"),
        )
        assert response.status_code == 200
        image = Image.objects.last()
        assert response.json()["data"]["createImage"]["success"] == True
        assert response.json()["data"]["createImage"]["image"]["id"] == str(image.id)
        assert (
            response.json()["data"]["createImage"]["image"]["name"]
            == image.name
            == name
        )
        assert (
            response.json()["data"]["createImage"]["image"]["picture"]
            == image.picture.url
        )

    # def test_remove_bg(self, gql_user_client):
    #     image = ImageFactory()

    #     response = gql_user_client.mutation(
    #         "removeBackground",
    #         arguments="pk: {}".format(image.id),
    #         payload="success",
    #     )
    #     assert response.status_code == 200
    #     assert response.json()["data"]["removeBackground"]["success"] == True
