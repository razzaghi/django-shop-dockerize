import json

from django.http import JsonResponse
from django.shortcuts import render
# Create your views here.
from django.views.decorators.csrf import csrf_exempt

from product.models import Product, Category


def home(request):
    products = Product.objects.all()
    categories = Category.objects.all()
    selected_category = 0
    if request.GET:
        query_string = request.GET.get("q", None)
        category = request.GET.get("category", 0)
        if query_string and category:
            selected_category = category
            products = Product.objects.filter(name__contains=query_string, category_id=category)
        elif query_string:
            products = Product.objects.filter(name__contains=query_string)
        elif category:
            selected_category = category
            products = Product.objects.filter(category_id=category)

    context = {
        'products': products,
        "categories": categories,
        "q": request.GET.get("q", ""),
        "selected_category": int(selected_category)
    }
    return render(request, 'index.html', context)


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
    return render(request, 'about.html', {})


def contact(request):
    return render(request, 'contact.html', {})
