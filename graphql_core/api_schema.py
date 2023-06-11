from graphene import Schema

from rmbg.graphql import ImageQueries, mutations


class Query(ImageQueries):
    pass


class Mutation(mutations.CreateImage):
    pass


schema = Schema(query=Query, mutation=Mutation)
