import json
import urllib

from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.template.loader import render_to_string

from account.models import CustomUser
from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
# Create your views here.
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView

import account.models
from product.models import Product, Category

def detail(request, id):
    product = Product.objects.get(id=id)
    context = {
        'product': product,
    }
    return render(request, 'detail.html', context)


@csrf_exempt
def submit_product(request):
    print(request)
    api = request.POST.get("api", None)
    if api != 'Ali123@123':
        return JsonResponse(data={'Err': 'Wrong api'}, safe=False)
    uniq_code = request.POST.get('uniq_code', None)
    asin = request.POST.get('asin', None)
    domain = request.POST.get('domain', None)
    name = request.POST.get('name', None)
    title = request.POST.get('title', None)
    description = request.POST.get('description', None)
    brand = request.POST.get('brand', None)
    category_id = request.POST.get('category_id', None)
    str_category = request.POST.get('str_category', None)
    str_categories = request.POST.get('str_categories', None)
    image = request.POST.get('image', None)
    image_url = request.POST.get('image_url', None)
    images = request.POST.get('images', None)
    url = request.POST.get('url', None)
    # product rates
    rate = request.POST.get('rate', None)
    rating = request.POST.get('rating', None)
    review_count = request.POST.get('review_count', None)
    product_status = request.POST.get('product_status', None)
    p_score = request.POST.get('p_score', None)
    # price
    price = request.POST.get('price', None)
    old_price = request.POST.get('old_price', None)
    prices_alternate = request.POST.get('prices_alternate', None)
    price_alternate_mean = request.POST.get('price_alternate_mean', None)
    price_alternate_med = request.POST.get('price_alternate_med', None)
    min_30_days = request.POST.get('min_30_days', None)
    price_status = request.POST.get('price_status', None)
    # off and discount
    discount_percent = request.POST.get('discount_percent', None)
    discount_start_date = request.POST.get('discount_start_date', None)
    discount_end_date = request.POST.get('discount_end_date', None)
    promo_code = request.POST.get('promo_code', None)
    off_percent = request.POST.get('off_percent', None)
    coupon_off_percent = request.POST.get('coupon_off_percent', None)
    # store
    store_link = request.POST.get('store_link', None)
    store_tag = request.POST.get('store_tag', None)
    store_name = request.POST.get('store_name', None)
    s_score = request.POST.get('s_score', None)
    # agent
    channel = request.POST.get('channel', None)
    agent_tag = request.POST.get('agent_tag', None)
    agent_username = request.POST.get('agent_username', None)

    if not category_id:
        try:
            category_id = (Category.objects.get(name=str_category)).id
        except:
            category_id = (Category.objects.create(name=str_category)).id

    product = Product.objects.create(
        uniq_code=uniq_code,
        asin=asin,
        domain=domain,
        name=name,
        title=title,
        description=description,
        brand=brand,
        category_id=category_id,
        str_category=str_category,
        str_categories=str_categories,
        image=image,
        image_url=image_url,
        images=images,
        url=url,
        # product rate
        rate=rate,
        rating=rating,
        review_count=review_count,
        product_status=product_status,
        p_score=p_score,
        # price
        price=price,
        old_price=old_price,
        prices_alternate=prices_alternate,
        price_alternate_mean=price_alternate_mean,
        price_alternate_med=price_alternate_med,
        min_30_days=min_30_days,
        price_status=price_status,
        # off and discount
        discount_percent=discount_percent,
        discount_start_date=discount_start_date,
        discount_end_date=discount_end_date,
        promo_code=promo_code,
        off_percent=off_percent,
        coupon_off_percent=coupon_off_percent,
        # store
        store_link=store_link,
        store_tag=store_tag,
        store_name=store_name,
        s_score=s_score,
        # agent
        channel=channel,
        agent_tag=agent_tag,
        agent_username=agent_username,
    )
    return JsonResponse(data=json.dumps(product.as_json()), safe=False)


def about(request):
    context = {}
    return render(request, 'about.html', context)

def more_info(request):
    context ={}
    return render(request, 'more_info.html', context)


def contact(request):
    context = {}
    return render(request, 'contact.html', context)

class HomeView(ListView):
    model = Product
    template_name = 'index.html'
    paginate_by = 15  # if pagination is desired
    context_object_name = 'products'

    def get_queryset(self):
       qs = super().get_queryset()
       #return qs
       if self.request.GET:
           kwargs = {}
           self.q = self.request.GET.get("q", '')
           self.selected_category = self.request.GET.get("category", 0)
           self.selected_category = int(self.selected_category) if self.selected_category != '' else 0
           if self.q != '':
               kwargs['name__icontains'] = self.q
           if self.selected_category > 0:
               kwargs['category_id'] = int(self.selected_category)
           qs = qs.filter(**kwargs)
       self.sort = self.request.GET.get("sort", "new").lower()
       if self.sort == "new":
           qs = qs.order_by("-create_date")
       elif self.sort == "name":
           qs = qs.order_by("name","-create_date")
       elif self.sort == "price_low":
           qs = qs.order_by("old_price","-create_date")
       elif self.sort == "price_high":
           qs = qs.order_by("-old_price","-create_date")
       elif self.sort == "p_score_low":
           qs = qs.order_by("-p_score","-create_date")
       elif self.sort == "discount_high":
           qs = qs.order_by("-discount_percent","-off_percent","-coupon_off_percent","-create_date")

       return qs

    def get_context_data(self, **kwargs):
        self.selected_category = 0
        context = super().get_context_data(**kwargs)
        self.get_queryset()
        context['q'] = self.request.GET.get("q", '')
        context["selected_category"] = int(self.selected_category)
        context['sort'] = self.sort
        context["user"] = get_user(self.request)

        return context

def get_user(request):
    user = CustomUser.objects.filter(username=request.user.username).first()
    if not user:
        user = CustomUser.get_or_register_user(ip=get_client_ip(request),
                                               session_key=get_session_key(request))
    return user

def commands(request, command):
    if request.method == "POST":
        valuse = command.split('_')
        user = get_user(request)
        if len(valuse) > 1:
            m_command = valuse[0]
            id = valuse[1]
            product = Product.objects.get(id=id)
            if m_command == 'b':#boght it
                if product.is_bought(user.id):
                    product.buys.remove(user)
                else:
                    product.buys.add(user)
            elif m_command == 'e':#ends
                if product.is_ended(user.id):
                    product.ends.remove(user)
                else:
                    product.ends.add(user)
            elif m_command == 'f':#favorites
                if product.is_favorite(user.id):
                    product.favorites.remove(user)
                else:
                    product.favorites.add(user)
            elif m_command == 'l':#liked it
                if product.is_liked(user.id):
                    product.likes.remove(user)
                else:
                    product.likes.add(user)
            elif m_command == 's':#shares
                if product.is_shared(user.id):
                    product.shares.remove(user)
                else:
                    product.shares.add(user)
            product.save()
        else:
            id = valuse[0]
            product = Product.objects.get(id=id)
        context = {
            'product': product,
            'user': user,
        }
        if request.is_ajax():
            html = render_to_string('cart_buttons.html', context, request=request)
            return JsonResponse({'form': html})
        #return HttpResponseRedirect(reverse('index'))

def redirect(request, command):
    valuse = command.split('_')
    user = get_user(request)
    if len(valuse) > 1:
        m_command = valuse[0]
        uniq_code = valuse[1]
        product = Product.objects.get(uniq_code=uniq_code)
        if m_command == 'c':
            if not product.is_clicked(user.id):
                product.clicks.add(user)
                product.save()
    else:
        uniq_code = valuse[0]
        product = Product.objects.get(uniq_code=uniq_code)
    #return HttpResponseRedirect("https://g.com")
    return HttpResponseRedirect(product.tagged_url())


def dislike(request, id):
    if request.method == "POST":
        #make sure user can't like the post more than once.
        user = User.objects.get(username=request.user.username)
        #find whatever post is associated with like
        product = Product.objects.get(id=id)

        # newLike = Like(user=user, post=post)
        # newLike.alreadyLiked = True
        #
        # post.likes += 1
        # #adds user to Post
        # post.user_likes.add(user)
        # post.save()
        # newLike.save()
        return HttpResponseRedirect(reverse('index'))


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[-1].strip()
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def get_session_key(request):
    if not request.session.session_key:
        request.session.create()
    return request.session.session_key