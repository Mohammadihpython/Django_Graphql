from django.contrib.auth import get_user_model
from graphql_jwt.decorators import login_required
import graphene
from graphene.types.generic import GenericScalar

from product.models import Products

user = get_user_model()

"""   
Here we make inputs for get information from users
then create the product
if your product have variants use CreateVariant classes
if product has not a variants use CreateProduct
"""


class ColorInput(graphene.InputObjectType):
    name = graphene.String()


class SizeInput(graphene.InputObjectType):
    name = graphene.String()


class ProductInput(graphene.InputObjectType):
    name = graphene.String(required=True)
    category = graphene.String()
    quantity = graphene.Int(required=True)
    slug = graphene.String(required=True)
    price = graphene.Decimal(require=True)
    available = graphene.Boolean()
    color = graphene.List(ColorInput)
    size = graphene.List(SizeInput)
    description = graphene.String()
    discount = graphene.Int()
    option_status = graphene.Boolean()


class VariantInput(graphene.InputObjectType):
    name = graphene.String(required=True)
    product_variant = graphene.List(ProductInput)
    color_variant = graphene.List(ColorInput)
    size_variant = graphene.List(SizeInput)
    unit_price = graphene.Decimal(required=True)
    discount = graphene.Int()
    amount = graphene.Int(required=True)


"""
Now we are create or update or delete product with above information that we get
"""


class CreateProduct(graphene.Mutation):
    class Arguments:
        input = ProductInput(description='this fields are required', required=True)

    response = GenericScalar()

    @login_required
    def mutate(parent, info, ):
        if info.cotext.is_superuser:
            try:
                Products.objects.create(
                    name=input.name,
                    category=input.category,
                    quantity=input.quantity,
                    slug=input.slug,
                    price=input.price,
                    color=input.color,
                    size=input.size,
                    description=input.description,
                    option_status=input.option_status,
                )
                return CreateProduct(response={'status': 'success', 'message': 'Product created successfully'})

            except Exception:
                return CreateProduct(response={'status': 'errors', 'message': 'Data is not valid'})
        else:
            return CreateProduct(None)


class UpdateProduct(graphene.Mutation):
    class Arguments:
        input = ProductInput(description='this fields are required', required=True)

    response = GenericScalar()

    #

    @login_required
    def mutate(root, info, product_id, **updated_data):
        name = input.name
        category = input.category
        quantity = input.quantity
        slug = input.slug
        price = input.price
        color = input.color
        size = input.size
        description = input.description
        option_status = input.option_status
        try:
            product = Products.objects.get(id=product_id)
            params = updated_data
            product.objects.update({k: v for k, v in params.items() if params[k]})
            # product.name = name if name is not None else product.name,
            # product.category = category if category is not None else product.category,
            # product.quantity = quantity if quantity is not None else product.quantity,
            # product.slug = slug if slug is not None else product.slug,
            # product.price = price if price is not None else product.price,
            # product.color = color if price is not None else product.color,
            # product.size = size if size is not None else product.size,
            # product.description = description if description is not None else product.description,
            # product.option_status = option_status if option_status is not None else product.option_status,
            # product.save()
            return UpdateProduct(product=product, response={'status': 'success', 'message': 'product updated successfully'})

            #  product.name=update_data.name if update_data.name is not None else product.name

        except Products.DoesNotExist:
            return UpdateProduct(response={'status': 'error', 'message': 'product dose not exist'})


class ProductMutations(graphene.ObjectType):
    update_product = UpdateProduct.Field()
    create_product = CreateProduct.Field()
