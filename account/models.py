from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.postgres.indexes import GinIndex
from django.contrib.postgres.indexes import GistIndex


class GistIndexTrgrmOps(GistIndex):
    def create_sql(self, model, schema_editor):
        # - this Statement is instantiated by the _create_index_sql()
        #   method of django.db.backends.base.schema.BaseDatabaseSchemaEditor.
        #   using sql_create_index template from
        #   django.db.backends.postgresql.schema.DatabaseSchemaEditor
        # - the template has original value:
        #   "CREATE INDEX %(name)s ON %(table)s%(using)s (%(columns)s)%(extra)s"
        statement = super().create_sql(model, schema_editor)
        # - however, we want to use a GIST index to accelerate trigram
        #   matching, so we want to add the gist_trgm_ops index operator
        #   class
        # - so we replace the template with:
        #   "CREATE INDEX %(name)s ON %(table)s%(using)s (%(columns)s gist_trgrm_ops)%(extra)s"
        statement.template = \
            "CREATE INDEX %(name)s ON %(table)s%(using)s (%(columns)s gist_trgm_ops)%(extra)s"

        return statement


class CustomUSer(AbstractUser):
    email = models.EmailField(blank=False, max_length=255, verbose_name='email')

    USERNAME_FIELD = 'username'
    EMAIL_FIELD = 'email'

    class Meta:
        ordering = ('pk',)
        # indexes = [
        #     GinIndex(
        #         name="user_search_gin",
        #         # opclasses and fields should be the same length
        #         fields=['email', ],
        #         opclasses=["gin_trgm_ops"] * 1
        #     )

        # GistIndexTrgrmOps(fields=['email', ])
        # ]
