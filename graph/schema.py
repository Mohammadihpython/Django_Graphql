import graphene

from account.mutations import AuthMutation
from product.queries import ProductQuery
from product.mutiaion import ProductMutations
from graphql_auth.schema import UserQuery, MeQuery


class Query(UserQuery, MeQuery, ProductQuery, graphene.ObjectType):
    pass


class Mutation(ProductMutations,AuthMutation,  graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)
