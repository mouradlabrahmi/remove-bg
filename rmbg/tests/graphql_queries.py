from gql import gql

from rmbg.tests.image_fragment import IMAGE_FRAGMENT

QUERY_IMAGE = gql(
    IMAGE_FRAGMENT
    + """
query GetImage($pk: ID!) {
  image(pk: $pk) {
    ...ImageNodeFragment
  }
}
"""
)
