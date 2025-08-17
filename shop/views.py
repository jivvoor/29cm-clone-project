import json
from pyexpat.errors import messages
from urllib import request
from django.conf import settings
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import HttpResponse, redirect
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
import requests

from cart.models import Cart, CartItem
from users.forms import UserForm
from .models import CartProduct, ColorCategory, Like, Order, OrderPayment, Product, Category, NestedSubCategory, SizeCategory, SubCategory

from users.models import User
from . import models, forms
from .forms import SearchForm
from shop import models as shop_models
from django.views.generic import ListView, DetailView
from django.http import Http404
from django.shortcuts import get_object_or_404

from django.shortcuts import render, get_object_or_404
from .models import Product
from qna.models import Qna, QnaCategory
from shop.models import Category
from django.db.models import Count, Q
from django.db.models.functions import Coalesce
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.edit import UpdateView
from django.views.decorators.http import require_POST


from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib.auth.views import LoginView, LogoutView

from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import Product, Like

from django.urls import reverse
from review.models import Review


def checkout_selected(request):
    if request.method == "POST":
        selected_item_ids = request.POST.getlist("selected_items")
        if not selected_item_ids:
            return redirect("shop:cart")  # 선택된 항목이 없으면 장바구니로 리다이렉트
        selected_items = CartItem.objects.filter(id__in=selected_item_ids)

        session_selected_items = []
        for item in selected_items:
            session_selected_items.append({
                "product_id": item.product.id,
                "product_name": item.product.name,
                "quantity": item.quantity,
                "size_id": item.size.id if item.size else None,
                "size_name": item.size.name if item.size else None,
                "color_id": item.color.id if item.color else None,
                "color_name": item.color.name if item.color else None,
                "price": item.product.price,
            })

        request.session["selected_items"] = session_selected_items
        request.session["direct_purchase"] = False
        request.session.modified = True
        print("DEBUG: Session Selected Items:", request.session["selected_items"])

        return redirect("shop:checkout")
    
    return redirect("shop:cart") # GET 요청일 경우 장바구니로 리디렉션

def direct_purchase(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    if request.method == "POST":
        quantity = int(request.POST.get("quantity", 1))
        size_id = request.POST.get("sizecategory")
        color_id = request.POST.get("colorcategory")

        size = get_object_or_404(SizeCategory, id=size_id) if size_id else None
        color = get_object_or_404(ColorCategory, id=color_id) if color_id else None

        # 바로 구매 아이템 데이터 생성
        direct_item = {
            "product_name": product.name,
            "quantity": quantity,
            "size_id": size.id if size else None,
            "size_name": size.name if size else None,
            "color_id": color.id if color else None,
            "color_name": color.name if color else None,
            "price": product.price * quantity,
        }

        # 세션에 저장
        request.session["direct_product_items"] = direct_item
        request.session["direct_purchase"] = True
        request.session.modified = True  # 세션 변경 사항 저장

        # checkout 페이지로 리다이렉트
        return redirect("shop:checkout")

    return redirect("cart:cart")

def checkout(request):
    items = []
    total = 0

    if request.method == "POST":
        # 사용자의 배송 정보 업데이트 처리
        form = UserForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect("shop:payment")  # 결제 페이지로 리디렉션

    else:
        form = UserForm(instance=request.user)

    if request.session.get("direct_purchase"):
        direct_item = request.session.get("direct_product_items", {})  # 딕셔너리로 가져옴
        if direct_item:  # 데이터가 있을 경우
            items = {  # 리스트 형태로 변환                
                    "product_name": direct_item["product_name"],
                    "quantity": direct_item["quantity"],
                    "size_name": direct_item["size_name"],
                    "color_name": direct_item["color_name"],
                    "price": direct_item["price"],
                    "form": form,

                
            }
            total = direct_item["price"] * direct_item["quantity"]
            direct_item_json = json.dumps(direct_item, ensure_ascii=False)
            return render(request, "shop/checkout.html", {
                "direct_items": items,
                "selected_items": None,
                "total": total,
                "direct_item_json": direct_item_json,
            })
        
        return render(request,"shop/checkout.html")
    
    selected_items = request.session.get("selected_items", [])
    
    if not isinstance(selected_items, list):
        selected_items = []
    for item in selected_items:
        product = Product.objects.get(id=item["product_id"])
        size = SizeCategory.objects.get(id=item["size_id"]).name if item["size_id"] else None  # SizeCategory를 문자열로 변환
        color = ColorCategory.objects.get(id=item["color_id"]).name if item["color_id"] else None  # ColorCategory를 문자열로 변환

        items.append({
            "product": product.name,
            "quantity": item["quantity"],
            "size_name": size,
            "color_name": color,
            "price": product.price * item["quantity"],
        })
        total = sum(item["price"] for item in selected_items)

        selected_items_json = json.dumps(selected_items, ensure_ascii=False)
        return render(request, "shop/checkout.html", {
            "selected_items": items, 
            "selected_items_json": selected_items_json,
            "total": total, 
            "direct_items" : None,
            "form": form,

        })
    return render(request,"shop/checkout.html")

@csrf_exempt
@login_required
def toggle_like(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    user = request.user

    # 좋아요 상태 토글
    if Like.objects.filter(user=user, product=product).exists():
        # 이미 좋아요한 경우, 좋아요 취소
        Like.objects.filter(user=user, product=product).delete()
        liked = False
    else:
        # 좋아요 추가
        Like.objects.create(user=user, product=product)
        liked = True

    # 좋아요 수를 포함하여 JSON 응답 반환
    return JsonResponse({'liked': liked, 'like_count': product.like_count()})

def search(request):
    # GET 요청으로부터 검색 파라미터 수집
    name = request.GET.get("name", "")
    category = int(request.GET.get("category", 0))
    color_id = int(request.GET.get("ColorCategory", 0))
    price = int(request.GET.get("price", 0))
    s_hosts = request.GET.getlist("hosts", [])

    # 필터 조건
    filter_args = {}

    if name:
        filter_args["name__icontains"] = name  # 대소문자 구분 없이 이름 검색

    if category != 0:
        filter_args["category__pk"] = category  # 카테고리 필터링

    if color_id != 0:
        filter_args["color__pk"] = color_id  # 색상 필터링

    if price != 0:
        filter_args["price__lte"] = price  # 가격 필터링

    if s_hosts:
        filter_args["host__id__in"] = s_hosts  # 호스트 필터링

    # 필터링된 상품 검색
    products = Product.objects.filter(**filter_args)

    # 페이징 처리 추가
    page = request.GET.get("page", 1)
    paginator = Paginator(products, 10)  # 한 페이지에 10개씩 표시

    try:
        products_page = paginator.page(page)
    except PageNotAnInteger:
        products_page = paginator.page(1)
    except EmptyPage:
        products_page = paginator.page(paginator.num_pages)

    # 카테고리와 호스트 선택지
    categories = models.Category.objects.all()
    color_categories = models.ColorCategory.objects.all()
    hosts = User.objects.all()

    # 템플릿에 넘길 컨텍스트
    context = {
        "name": name,
        "s_category": category,
        "s_ColorCategories": [color_id],
        "price": price,
        "s_hosts": s_hosts,
        "categories": categories,
        "ColorCategories": color_categories,
        "hosts": hosts,
        "products": products_page,  # 페이징된 상품 목록
        "page_obj": products_page,  # 페이지 정보 객체
    }

    return render(request, "shop/search.html", context)

def all_products(request):
    page = request.GET.get("page", 1)
    products = Product.objects.all().order_by('name')
    paginator = Paginator(products, 10)
    try:
        products_page = paginator.page(page)
    except PageNotAnInteger: 
        products_page = paginator.page(1)
    except EmptyPage: 
        products_page = paginator.page(paginator.num_pages)

    context = {
        "products": products_page,  # 현재 페이지에 해당하는 제품 리스트
        "page_obj": products_page,  # 페이지 정보 객체 (템플릿에서 사용 가능)
    }
    return render(request, 'shop/product_list.html', context)

class ProductDetail(DetailView):
    model = models.Product
    template_name = "shop/product_detail.html"
    context_object_name = "product"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category_id = self.request.GET.get('category_id')
        if category_id:
            context['qnas'] = Qna.objects.filter(product=self.object, category_id=category_id)  # 선택된 카테고리의 Q&A만 필터링
            context['selected_category_id'] = int(category_id)  # 선택된 카테고리 ID 저장
        else:
            context['qnas'] = Qna.objects.filter(product=self.object)  # 모든 Q&A 가져옴
            context['selected_category_id'] = None
        context['qna_categories'] = QnaCategory.objects.annotate(
            qna_count=Coalesce(Count('qna', filter=Q(qna__product=self.object)), 0)).order_by('id')
        context['total_qna_count'] = context['qnas'].count()

        context['sizes'] = SizeCategory.objects.all()
        context['colors'] = ColorCategory.objects.all()

        user = self.request.user
        product = self.object  # 현재 조회 중인 Product 객체
       

        if user.is_authenticated:
            # 사용자와 제품 간의 좋아요 여부를 확인하고 변수에 저장
            context['user_has_liked'] = Like.objects.filter(user=user, product=product).exists()
        else:
            context['user_has_liked'] = False  # 로그인하지 않은 경우 기본적으로 False

        # 리뷰 리스트 추가
        context['reviews'] = Review.objects.filter(product=product).order_by('-created_at')

        # 좋아요 수 추가
        context['like_count'] = Like.objects.filter(product=product).count()

        return context
    


class ProductListByCategory(ListView):
    model = models.Product
    template_name = 'shop/product_list.html'
    context_object_name = 'products'

    def get_queryset(self):
        return models.Product.objects.filter(nested_subcategory__parent_subcategory__category__slug=self.kwargs['slug'])
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = models.Category.objects.all()
        return context

class ProductListBySubCategory(ListView):
    model = models.Product
    template_name = 'shop/product_list.html'
    context_object_name = 'products'

    def get_queryset(self):
        return models.Product.objects.filter(
            nested_subcategory__parent_subcategory__category__slug=self.kwargs['category_slug'],
            nested_subcategory__parent_subcategory__slug=self.kwargs['subcategory_slug']
        )
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        subcategory = get_object_or_404(models.SubCategory, slug=self.kwargs['subcategory_slug'])
        context['nested_subcategories'] = subcategory.nested_subcategories.all()
        return context

class ProductListByNestedSubCategory(ListView):
    model = models.Product
    template_name = "shop/product_list.html"
    context_object_name = "products"

    def get_queryset(self):
        category_slug = self.kwargs['category_slug']
        subcategory_slug = self.kwargs['subcategory_slug']
        nested_subcategory_slug = self.kwargs['nested_subcategory_slug']
        
        return models.Product.objects.filter(
            nested_subcategory__parent_subcategory__category__slug=category_slug,
            nested_subcategory__parent_subcategory__slug=subcategory_slug,
            nested_subcategory__slug=nested_subcategory_slug
        )
    

class HomeView(ListView):
    """HomeView Definition"""
    model = models.Product
    paginate_by = 10  # 👈 한 페이지에 제한할 Object 수
    paginate_orphans = 5  # 👈 짜투리 처리
    page_kwarg = "page" # 👈 페이징할 argument
    context_object_name = "products"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        # 좋아요 상태 확인 및 추가
        if user.is_authenticated:
            liked_product_ids = Like.objects.filter(user=user).values_list('product_id', flat=True)
            for product in context['products']:
                product.user_has_liked = product.id in liked_product_ids
        else:
            for product in context['products']:
                product.user_has_liked = False

        return context


def product_list(request):
    products = Product.objects.all()

    # 각 상품에 대해 현재 사용자가 좋아요를 눌렀는지 확인
    for product in products:
        product.user_has_liked = product.likes.filter(user=request.user).exists()

    return render(request, 'shop/product_list.html', {
        'products': products,
    })

#주문관련 뷰

@login_required
def order_list(request):
    order_qs = Order.objects.all().filter(user=request.user)
    return render(
        request,
        "mall/order_list.html",
        {
            "order_list": order_qs,
        },
    )
    pass


@csrf_exempt
@login_required
def order_new(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            
            # 결제 정보 처리
            imp_uid = data.get('imp_uid')
            merchant_uid = data.get('merchant_uid')
            paid_amount = data.get('paid_amount')
            status = data.get('status')
            
            print(f"결제 정보 수신: imp_uid={imp_uid}, merchant_uid={merchant_uid}, amount={paid_amount}")
            
            # 세션에서 주문 정보 가져오기
            direct_purchase = request.session.get('direct_purchase', False)
            
            if direct_purchase:
                # 직접 구매인 경우
                direct_item = request.session.get('direct_product_items', {})
                if direct_item:
                    # Order 생성
                    order = Order.objects.create(
                        user=request.user,
                        total_amount=paid_amount
                    )
                    
                    # OrderedProduct 생성
                    from .models import OrderedProduct
                    product = Product.objects.get(name=direct_item['product_name'])
                    OrderedProduct.objects.create(
                        order=order,
                        product=product,
                        name=product.name,
                        price=product.price,
                        quantity=direct_item['quantity']
                    )
                    
                    # 세션 정리
                    del request.session['direct_purchase']
                    del request.session['direct_product_items']
                    
            else:
                # 장바구니에서 구매인 경우
                selected_items = request.session.get('selected_items', [])
                if selected_items:
                    # Order 생성
                    order = Order.objects.create(
                        user=request.user,
                        total_amount=paid_amount
                    )
                    
                    # OrderedProduct 생성
                    from .models import OrderedProduct
                    for item in selected_items:
                        product = Product.objects.get(id=item['product_id'])
                        OrderedProduct.objects.create(
                            order=order,
                            product=product,
                            name=product.name,
                            price=product.price,
                            quantity=item['quantity']
                        )
                    
                    # 세션 정리
                    del request.session['selected_items']
            
            # OrderPayment 생성
            payment = OrderPayment.create_by_order(order)
            payment.meta = {
                'imp_uid': imp_uid,
                'merchant_uid': merchant_uid,
                'paid_amount': paid_amount,
                'status': status
            }
            payment.pay_status = 'paid'
            payment.is_paid_ok = True
            payment.save()
            
            # 주문 상태 업데이트
            order.status = Order.Status.PAID
            order.save()
            
            return JsonResponse({
                'status': 'success',
                'message': '주문이 성공적으로 생성되었습니다.',
                'order_id': str(order.uid)
            })
            
        except json.JSONDecodeError as e:
            return JsonResponse({
                'status': 'error',
                'message': '잘못된 JSON 형식입니다.'
            }, status=400)
        except Exception as e:
            print(f"주문 생성 오류: {str(e)}")
            return JsonResponse({
                'status': 'error',
                'message': str(e)
            }, status=400)
    
    # GET 요청의 경우 기존 로직 유지
    cart_product_qs = CartProduct.objects.filter(user=request.user)

    order = Order.create_from_cart(request.user, cart_product_qs)
    cart_product_qs.delete()

    return redirect("order_pay", order.pk)


@login_required
def order_pay(request, pk):
    order = get_object_or_404(Order, pk=pk, user=request.user)

    order.refresh_from_db()

    if order.total_amount == 0:
        messages.error(request, "장바구니에 상품이 없습니다.")
        return redirect("cart_detail")

    if not order.product_set.exists():
        messages.error(request, "장바구니에 상품이 없습니다.")
        return redirect("cart_detail")

    if not order.can_pay():
        messages.error(request, "현재 결제를 할 수 없는 주문입니다.")
        return redirect(order)

    payment = OrderPayment.create_by_order(order)

    payment_props = {
        "pg": settings.PORTONE_PG,
        "merchant_uid": payment.merchant_uid,
        "name": payment.name,
        "amount": payment.desired_amount,
        "buyer_name": payment.buyer_name or request.user.username,
        "buyer_email": payment.buyer_email,
    }

    return render(
        request,
        "mall/order_pay.html",
        {
            "portone_shop_id": settings.PORTONE_SHOP_ID,
            "payment_props": payment_props,
            "next_url": reverse("order_check", args=[order.pk, payment.pk]),
        },
    )


@login_required
def order_check(request, order_pk, payment_pk):
    payment = get_object_or_404(OrderPayment, pk=payment_pk, order__pk=order_pk)
    payment.update()
    # return redirect(payment.order)
    return redirect("order_detail", order_pk)


@login_required
def order_detail(request, pk):
    order = get_object_or_404(Order, pk=pk, user=request.user)
    return render(
        request,
        "mall/order_detail.html",
        {
            "order": order,
        },
    )

@require_POST
@login_required
def order_confirm(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    if order.status == Order.Status.DELIVERED or order.status == Order.Status.PAID:
        order.status = Order.Status.CONFIRMED
        order.save()
    return redirect('shopping_info')