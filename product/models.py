from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=40)

    def __str__(self):
        return self.name


class Product(models.Model):
    uniq_code = models.CharField(max_length=40, null=True, blank=True,unique=True)
    name = models.CharField(max_length=100, null=True, blank=True)
    title = models.CharField(max_length=150, null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    image = models.ImageField(default="not_found.jpg", upload_to="photos", null=True, blank=True)
    image_1_url = models.URLField(null=True, blank=True)
    image_2_url = models.URLField(null=True, blank=True)
    image_3_url = models.URLField(null=True, blank=True)
    image_4_url = models.URLField(null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    str_category = models.CharField(max_length=60, null=True, blank=True)
    str_categories = models.CharField(max_length=250, null=True, blank=True)
    rate = models.DecimalField(max_digits=5, decimal_places=2,default=0)
    review_count = models.IntegerField(default=0)
    discount_percent = models.DecimalField(max_digits=6, decimal_places=2,default=0)
    discount_start_date = models.DateTimeField(null=True, blank=True)
    discount_end_date = models.DateTimeField(null=True, blank=True)
    discount_code = models.CharField(max_length=30, null=True, blank=True)
    special_discount = models.DecimalField(max_digits=6, decimal_places=2,default=0)
    store_link = models.URLField(null=True, blank=True)
    product_status = models.DecimalField(max_digits=5, decimal_places=2,default=0)
    price_status = models.DecimalField(max_digits=5, decimal_places=2,default=0)
    description = models.TextField(null=True, blank=True)
    channel = models.CharField(max_length=30, null=True, blank=True)

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
            image_1_url=self.image_1_url,
            image_2_url=self.image_2_url,
            image_3_url=self.image_3_url,
            image_4_url=self.image_4_url,
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
