import graphene
from .types import CommentType

class CommentQuery(graphene.objectType):
    comments = graphene.List(CommentType)

    def resolve_comments(parent, info,product_id):
        user = info.context.user
        return user.cart.all()
