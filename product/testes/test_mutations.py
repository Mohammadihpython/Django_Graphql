from graphql_jwt.testcases import JSONWebTokenTestCase
from django.contrib.auth import get_user_model


class ProductMutationTest(JSONWebTokenTestCase):
    @classmethod
    def setUp(cls):
        cls.user = get_user_model.objects.create_user(
            username='test',
            password='test',
            email='test',
        )

    def test_mutation_create_product(self):
        query = """
              mutation create_product($input: ProductInput!){
                  CreateProduct(input:$input){
                     product{
                       id
                       name
                       price
                       description
                       quantity}
                    }
                }
        """
