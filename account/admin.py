from django.contrib import admin
from .models import CustomUSer
from django.apps import apps

# Register your models here.

admin.site.register(CustomUSer)

app = apps.get_app_config('graphql_auth')
for model_name, model in app.models.items():
    admin.site.register(model)
