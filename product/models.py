from enum import Enum

from django.db import models
from django.db.models import Sum

from account.models import CustomUser


class Category(models.Model):
    name = models.CharField(max_length=60)
    title = models.CharField(max_length=40,blank=True,null=True)

    def __str__(self):
        return self.name

    @property
    def title_(self):
        return self.title if self.title else self.name


class Product(models.Model):
    #main product attr
    create_date = models.DateTimeField(auto_now_add=True)
    uniq_code = models.CharField(max_length=40, null=True, blank=True,unique=True)
    asin = models.CharField(max_length=20, null=True, blank=True)
    domain = models.CharField(max_length=10, null=True, blank=True)
    name = models.CharField(max_length=100, null=True, blank=True)
    title = models.CharField(max_length=150, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    brand = models.CharField(max_length=50, null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    str_category = models.CharField(max_length=60, null=True, blank=True)
    str_categories = models.CharField(max_length=250, null=True, blank=True)
    image = models.ImageField(default="not_found.jpg", upload_to="photos", null=True, blank=True)
    image_url = models.URLField(null=True, blank=True)
    images = models.TextField(null=True, blank=True)
    url = models.URLField(max_length=500, null=True, blank=True)
    #product rates
    rate = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    rating = models.CharField(max_length=80, null=True, blank=True)
    review_count = models.IntegerField(default=0)
    product_status = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    p_score = models.DecimalField(max_digits=7, decimal_places=2, default=0)
    #price
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    old_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    prices_alternate = models.CharField(max_length=200, null=True, blank=True)
    price_alternate_mean = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    price_alternate_med = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    min_30_days = models.BooleanField(null=True, blank=True)
    price_status = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    #off and discount
    discount_percent = models.DecimalField(max_digits=6, decimal_places=2,default=0)
    discount_start_date = models.DateTimeField(null=True, blank=True)
    discount_end_date = models.DateTimeField(null=True, blank=True)
    promo_code = models.CharField(max_length=30, null=True, blank=True)
    off_percent = models.DecimalField(max_digits=6, decimal_places=2,default=0)
    coupon_off_percent = models.DecimalField(max_digits=6, decimal_places=2,default=0)
    #store
    store_link = models.URLField(null=True, blank=True)
    store_tag = models.CharField(max_length=30, null=True, blank=True)
    store_name = models.CharField(max_length=30, null=True, blank=True)
    s_score = models.DecimalField(max_digits=7, decimal_places=2,default=0)
    #agent
    channel = models.CharField(max_length=30, null=True, blank=True)
    agent_tag = models.CharField(max_length=30, null=True, blank=True)
    agent_username = models.CharField(max_length=30, null=True, blank=True)
    #buttons data
    # likes = models.ManyToManyField(CustomUser, blank=True, related_name='likes')
    # views = models.ManyToManyField(CustomUser, blank=True, related_name='views')
    # clicks = models.ManyToManyField(CustomUser, blank=True, related_name='clicks')
    # buys = models.ManyToManyField(CustomUser, blank=True, related_name='buys')
    # favorites = models.ManyToManyField(CustomUser, blank=True, related_name='favorites')
    # shares = models.ManyToManyField(CustomUser, blank=True, related_name='shares')
    # ends = models.ManyToManyField(CustomUser, blank=True, related_name='ends')
    # #views = models.ManyToManyField(CustomUser, blank=True, related_name='views')

    @property
    def product_score(self):
        r = 0
        if self.rate >= 4.5  and self.review_count >= 100:
            r = 5
        elif self.rate >= 4 and self.review_count >= 1000:
            r = 5
        elif self.rate >= 4 and self.review_count >= 100:
            r = 4
        elif self.rate == 0:
            r = 2.5
        else:
            r = 1.5
        return Tools.star_html(r)

    @property
    def bought_count(self):
        return ActionsLog.action_count(self,ActionType.Bought)

    @property
    def ends_count(self):
        return ActionsLog.action_count(self,ActionType.End)

    @property
    def favorites_count(self):
        return ActionsLog.action_count(self,ActionType.Favorite)

    @property
    def likes_count(self):
        return ActionsLog.action_count(self,ActionType.Like)

    @property
    def shares_count(self):
        return ActionsLog.action_count(self,ActionType.Share)

    @property
    def clicks_count(self):
        return ActionsLog.action_count(self,ActionType.Click)

    @property
    def views_count(self):
        return ActionsLog.action_count(self,ActionType.View)

    def _views_count_add(self, requset):
        if not self.is_viewed(requset):
            ActionsLog.add_action(requset,self,ActionType.View,1)
        return ActionsLog.action_count(self,ActionType.View)

    def is_bought(self,requset):
        return ActionsLog.get_action_status(requset,self,ActionType.Bought,1)

    def is_ended(self, requset):
        return ActionsLog.get_action_status(requset,self,ActionType.End,1)

    def is_favorite(self, requset):
        return ActionsLog.get_action_status(requset,self,ActionType.Favorite,1)

    def is_liked(self,requset):
        return ActionsLog.get_action_status(requset,self,ActionType.Like,1)

    def is_shared(self,requset):
        return ActionsLog.get_action_status(requset,self,ActionType.Share,1)

    def is_clicked(self,requset):
        return ActionsLog.get_action_status(requset,self,ActionType.Click,1)

    def is_viewed(self,requset):
        return ActionsLog.get_action_status(requset,self,ActionType.View,1)

    @property
    def store_score(self):
        return Tools.star_html(self.s_score/2)

    @property
    def price_score(self):
        return Tools.star_html(self.price_status)

    @property
    def total_discount(self):
        return int(min(100,self.off_percent + (100-self.off_percent)*(self.discount_percent + self.coupon_off_percent)/100))

    #total_discount = property(_total_discount)

    def total_discount_str(self):
        m_str = ''
        m_str += '📦' if self.discount_percent > 0 else ''
        m_str += '🔖' if self.off_percent > 0 else ''
        m_str += '✂' if self.coupon_off_percent > 0 else ''
        return m_str

    def final_price(self):
        return format((100-self.total_discount) * self.old_price / 100,',.2f')

    def disp_image(self):
        return self.image.url if self.image else self.image_url

    def tagged_url(self):
        if self.url:
            return f'{self.url}{"&"if self.url.__contains__("?") else "?"}tag={self.agent_tag}'
        return "-"

    def tagged_store_link(self):
        if self.store_link:
            return f'{self.store_link}{"&"if self.store_link.__contains__("?") else "?"}tag={self.agent_tag}'
        return "-"

    def product_rating_html(self):
        return Tools.star_html(self.product_status)

    def as_json(self):
        return dict(
            id=self.id,
            uniq_code=self.uniq_code,
            asin=self.asin,
            domain=self.domain,
            name=self.name,
            title=self.title,
            description=self.description,
            brand=self.brand,
            category_id=self.category.id,
            str_category=self.str_category,
            str_categories=self.str_categories,
            image=self.image.url if self.image else self.image_url,
            images=self.images,
            url=self.url,
            # product rates
            rate=self.rate,
            rating=self.rating,
            review_count=self.review_count,
            product_status=self.product_status,
            p_score=self.p_score,
            # price
            price=self.price,
            old_price=self.old_price,
            prices_alternate=self.prices_alternate,
            price_alternate_mean=self.price_alternate_mean,
            price_alternate_med=self.price_alternate_med,
            min_30_days=self.min_30_days,
            price_status=self.product_status,
            # off and discount
            discount_percent=self.discount_percent,
            discount_start_date=self.discount_start_date,
            discount_end_date=self.discount_end_date,
            promo_code=self.promo_code,
            off_percent=self.off_percent,
            coupon_off_percent=self.coupon_off_percent,
            # store
            store_link=self.store_link,
            store_tag=self.store_tag,
            store_name=self.store_name,
            s_score=self.s_score,
            # agent
            channel=self.channel,
            agent_tag=self.agent_tag,
            agent_username=self.agent_username,
        )

    def __str__(self):
        return self.name


class User_Functions:
    @staticmethod
    def get_or_register_user(ip,session_key):
        user_ = CustomUser.objects.filter(ip=ip,session_key=session_key).first()
        if user_:
            return user_
        else:
            return CustomUser.objects.create_user(username=f'{session_key}_{ip}'.replace('.', '_'),ip=ip,session_key=session_key)

    @staticmethod
    def get_user(request):
        user = CustomUser.objects.filter(username=request.user.username).first()
        return user

    @staticmethod
    def get_client_ip(request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[-1].strip()
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip

    @staticmethod
    def get_session_key(request):
        if not request.session.session_key:
            request.session.create()
        return request.session.session_key


class ActionType(Enum):
    Like = "Like"
    Bought = "Bought"
    Share = "Share"
    Favorite = "Favorite"
    End = "End"
    View = "View"
    Click = "Click"

    @classmethod
    def choices(cls):
        return tuple((i.name, i.value) for i in cls)

class ActionsLog(models.Model):
    create_date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(CustomUser,blank=True,null=True,on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE,blank=True,null=True)
    session_key = models.CharField(max_length=40,blank=True,null=True)
    ip = models.CharField(max_length=20,blank=True,null=True)
    action = models.CharField(choices=ActionType.choices(),max_length=20)
    value = models.IntegerField(default=1)

    @staticmethod
    def get_action_status(request,_product,_action_type,_value):
        _user = User_Functions.get_user(request)
        _session_key = User_Functions.get_session_key(request)
        _ip = User_Functions.get_client_ip(request)
        if _user:
            res = ActionsLog.objects.filter(user_id=_user.id,product_id=_product.id,action=_action_type.value).last()
        else:
            res = ActionsLog.objects.filter(session_key=_session_key,ip=_ip,product_id=_product.id,action=_action_type.value).last()
        if res:
            return res.value == _value

    @staticmethod
    def add_action(request,_product,_action_type,_value):
        _user = User_Functions.get_user(request)
        _session_key = User_Functions.get_session_key(request)
        _ip = User_Functions.get_client_ip(request)
        ActionsLog.objects.create(
            user_id=_user.id if _user else None,
            product_id=_product.id,
            session_key=_session_key,
            ip=_ip,
            action=_action_type.value,
            value=_value
        )

    @staticmethod
    def action_count(_product, _action_type):
        res = ActionsLog.objects.filter(product_id=_product.id,
                                        action=_action_type.value).aggregate(Sum('value'))['value__sum']
        return res if res else 0



class Tools:
    @staticmethod
    def star_html(rate=5):
        return '✅✅✅✅' if rate>=4.5 else '✅✅✅' if rate>=3 else '✅✅' if rate>=2 else '✅'


