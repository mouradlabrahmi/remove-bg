from gql import gql

from rmbg.tests.image_fragment import IMAGE_FRAGMENT

CREATE_IMAGE = gql(
    IMAGE_FRAGMENT
    + """
    mutation CreateImage(
        $name: String
        $picture: ImageUpload
    ){
        createImage(
            input: {
                name: $name
                picture: $picture
            }
        ){
            image{
                ...ImageNodeFragment
            }
        }
    }
    """
)
