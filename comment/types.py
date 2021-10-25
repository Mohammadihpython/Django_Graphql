
from graphene import relay
from django.contrib.auth import get_user_model
from cart.models import Comment

from graphene_django import DjangoObjectType

user = get_user_model()


class CommentType(DjangoObjectType):
    class Meta:
        model = Comment
        interfaces = (relay.Node,)
