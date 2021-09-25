from django.db import models


# Create your models here.
class Books(models.Model):
    title = models.CharField(max_length=100)
    excerpt = models.TextField()

    def __str__(self):
        return self.title


class Order(models.Model):
    paid = models.BooleanField(default=False)
    create = models.DateTimeField(auto_now_add=True)
    discount = models.PositiveIntegerField(blank=True, null=True)
    email = models.EmailField()
    f_name = models.CharField(max_length=250)
    l_name = models.CharField(max_length=250)
    address = models.CharField(max_length=1000)

    def __str__(self):
        return self.f_name
