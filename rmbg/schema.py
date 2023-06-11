from graphene import ObjectType, Schema

from rmbg.graphql import mutations, queries


class Query(queries.ImageQuery, ObjectType):
    pass


class Mutation(mutations.ImageMutation, ObjectType):
    pass


schema = Schema(query=Query, mutation=Mutation)
