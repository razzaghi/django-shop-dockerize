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
    api = request.POST.get("api", None)
    if api != 'Ali123@123':
        return JsonResponse(data={'Err': 'Wrong api'}, safe=False)

    uniq_code = request.POST.get("uniq_code", None)
    name = request.POST.get("name", None)
    title = request.POST.get("title", None)
    price = request.POST.get("price", 0)
    image = request.POST.get("image", None)
    image_1_url = request.POST.get("image_1_url", None)
    image_2_url = request.POST.get("image_2_url", None)
    image_3_url = request.POST.get("image_3_url", None)
    image_4_url = request.POST.get("image_4_url", None)
    str_category = request.POST.get("str_category", None)
    str_categories = request.POST.get("str_categories", None)
    category = request.POST.get("category", None)
    rate = request.POST.get("rate", 0)
    review_count = request.POST.get("review_count", 0)
    discount_percent = request.POST.get("discount_percent", 0)
    discount_start_date = request.POST.get("discount_start_date", None)
    discount_end_date = request.POST.get("discount_end_date", None)
    discount_code = request.POST.get("discount_code", None)
    special_discount = request.POST.get("special_discount", 0)
    store_link = request.POST.get("store_link", None)
    product_status = request.POST.get("product_status", 0)
    price_status = request.POST.get("price_status", 0)
    description = request.POST.get("description", "")
    if not category:
        try:
            category = Category.objects.get(name=str_category)
        except:
            Category.objects.create(name=str_category)
        category = Category.objects.get(name=str_category).id

    product = Product.objects.create(
        uniq_code=uniq_code,
        name=name,
        title=title,
        price=price,
        image=image,
        image_1_url=image_1_url,
        image_2_url=image_2_url,
        image_3_url=image_3_url,
        image_4_url=image_4_url,
        category_id=category,
        str_category=str_category,
        str_categories=str_categories,
        rate=rate,
        review_count=review_count,
        discount_percent=discount_percent,
        discount_start_date=discount_start_date,
        discount_end_date=discount_end_date,
        discount_code=discount_code,
        special_discount=special_discount,
        store_link=store_link,
        product_status=product_status,
        price_status=price_status,
        description=description
    )
    return JsonResponse(data=json.dumps(product.as_json()), safe=False)


def about(request):
    return render(request, 'about.html', {})


def contact(request):
    return render(request, 'contact.html', {})
