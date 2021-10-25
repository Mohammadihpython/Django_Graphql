import graphene
from graphene.types.generic import GenericScalar
from graphql_jwt.decorators import login_required

from django_graphql.product.models import Products
from .models import Cart

class CartInput(graphene.InputObjectType):
    product_id = graphene.ID(required=True)
    variant_id = graphene.ID(required=True)
    quantity = graphene.ID(required=True)

class AddCart(graphene.Mutation):
    class Arguments():
        input = CartInput(description='this fields are required', required=True)
    response = GenericScalar()

    @login_required
    def mutate(parent, info, product_id, variant_id, quantity):

        if info.context.is_authenticated:
            product = Products.object.get(id=product_id)
            if product.option_status != 'None':
                data = Cart.objects.filter(user_id=info.context.user.id, variant_id=variant_id)
                if data:
                    check = 'yes'
                else:
                    check = 'no'
            else:
                data = Cart.objects.filter(user_id=info.context.user.id, product_id=product_id)
                if data:
                    check = 'yes'
                else:
                    check = 'no'
            if check == 'yes':
                if product.option_status != 'None':
                    obj = Cart.objects.get(user_id=info.context.user.id, variant_id=variant_id)
                else:
                    obj = Cart.objects.get(user_id=info.context.user.id, product_id=product_id)
                obj.quantity += quantity
                obj.save()
                return AddCart(response={'status': 'success', 'message': 'the product added to cart before and quantity of updated'})
            else:
                Cart.objects.create(user_id=info.context.user.id, product_id=product_id,
                                    variant_id=variant_id, quantity=quantity)
                return AddCart(response={'status': 'success', 'message': 'the product added to cart'})
        else:
            return AddCart(None)


class DeleteItem(graphene.Mutation):
    class Arguments:
        row_id = graphene.ID(required=True)

    response = GenericScalar()

    @login_required
    def mutate(parent, info, row_id):

        user = info.context.user
        try:
            Cart.objects.get(user_id=user.id, id=row_id)
            return DeleteItem(response={'status': 'success', 'message': 'the product deleted from cart'})
        except Exception:
            return AddCart(response={'status': 'error', 'message': 'data in not valid or need authenticated'})


class ClearCart(graphene.Mutation):
    def Mutate(parent, info,):
        Cart.objects.filter(user_id=info.context.user.id).delete()


class CartMutation(graphene.ObjectType):
    add_to_cart = AddCart.Field()
    delete_cart = DeleteItem.Field()
    clear_cart = ClearCart.Field()
