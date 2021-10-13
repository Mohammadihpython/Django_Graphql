import graphene
from graphene import relay
from graphene_django.filter import DjangoFilterConnectionField

from .types import ProductType, VariantType
from product.models import Products, variants


class ProductQuery(graphene.ObjectType):
    product_variants = graphene.List(VariantType, pk=graphene.ID())
    product = relay.Node.Field(ProductType)
    all_products = DjangoFilterConnectionField(ProductType,
                                     )

    def resolve_products(root, info):
        # query a list of product
        return Products.objects.all()

    def resolve_product(root, info, pk):
        # query a list of product
        product = Products.objects.get(id=pk)

        return product

    def resolve_product_variants(root, info, pk):
        return variants.objects.filter(product_variant_id=pk)
