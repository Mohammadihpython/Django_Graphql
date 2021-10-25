import graphene
from .types import CartType

class CartQuery(graphene.objectType):
    cart = graphene.List(CartType)

    def resolve_cart(parent, info,):
        user = info.context.user
        return user.cart.all()
