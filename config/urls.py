
from django.contrib import admin
from django.views.decorators.csrf import csrf_exempt
from django.urls import path,include
from graphene_django.views import GraphQLView

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('', include('book.urls')),
    # path('', include('quiz.urls')),
    path('graphql',csrf_exempt(GraphQLView.as_view(graphiql=True)),)
]
