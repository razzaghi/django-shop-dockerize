from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=40)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(default="not_found.jpg", upload_to="photos")

    def __str__(self):
        return self.name