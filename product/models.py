from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=40)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=40, null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    image = models.ImageField(default="not_found.jpg", upload_to="photos", null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    rate = models.IntegerField(default=0)
    review_count = models.IntegerField(default=0)
    discount_percent = models.IntegerField(default=0)
    discount_start_date = models.DateField(null=True, blank=True)
    discount_end_date = models.DateField(null=True, blank=True)
    discount_code = models.CharField(max_length=200, null=True, blank=True)
    special_discount = models.IntegerField(default=0)
    store_link = models.URLField(null=True, blank=True)
    product_status = models.IntegerField(default=0)
    price_status = models.IntegerField(default=0)
    description = models.TextField(null=True, blank=True)

    def as_json(self):

        image_address = None
        if self.image:
            image_address = self.image.url

        category = None
        if self.category:
            category = self.category.name
        return dict(
            id=self.id,
            name=self.name,
            price=self.price,
            image=image_address,
            category=category,
            rate=self.rate,
            review_count=self.review_count,
            discount_percent=self.discount_percent,
            discount_start_date=self.discount_start_date,
            discount_end_date=self.discount_end_date,
            discount_code=self.discount_code,
            special_discount=self.special_discount,
            store_link=self.store_link,
            product_status=self.price_status,
            price_status=self.price_status,
            description=self.description,
        )

        def __str__(self):
            return self.name
