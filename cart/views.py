from django.shortcuts import render, redirect
from shop.models import ColorCategory, Product, SizeCategory
from .models import Cart, CartItem
from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings
import requests
import json
from django.shortcuts import HttpResponse
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, JsonResponse

def _cart_id(request):
    cart_id = request.session.session_key
    if not cart_id:
        request.session.create()  # 새 세션 생성
        cart_id = request.session.session_key  # 새로 생성된 세션 키를 다시 가져옴
    return cart_id

def add_cart(request, product_id):
    # 해당 product_id로 제품을 가져옴
    product = get_object_or_404(Product, id=product_id)
    
    # 로그인한 사용자와 비로그인 사용자 모두 처리
    if request.user.is_authenticated:
        # 로그인한 사용자의 경우 user 기반으로 Cart 생성
        cart, created = Cart.objects.get_or_create(user=request.user)
    else:
        # 비로그인 사용자의 경우 세션 기반으로 Cart 생성
        cart, created = Cart.objects.get_or_create(cart_id=_cart_id(request))

    if request.method == "POST":
        # POST 데이터 처리
        quantity = int(request.POST.get("quantity", 1))
        size_id = request.POST.get("sizecategory")
        color_id = request.POST.get("colorcategory")
        # 사이즈와 색상 가져오기
        size = get_object_or_404(SizeCategory, id=size_id)
        color = get_object_or_404(ColorCategory, id=color_id)

        # CartItem 가져오기 또는 생성
        cart_item, created = CartItem.objects.get_or_create(
            cart=cart,
            product=product,
            size=size,
            color=color,
            defaults={"quantity": 0},
        )
        cart_item.quantity += 1
        cart_item.save()
        
        if not created:
            # 이미 존재하는 경우 수량 업데이트
            cart_item.quantity += 1
            cart_item.save()

        if request.POST.get("action") == "direct_purchase":
            # 바로 구매 세션 설정
            request.session["direct_purchase"] = True
            request.session["direct_product_id"] = product_id
            request.session["direct_quantity"] = quantity
            request.session["direct_size_id"] = size_id
            request.session["direct_color_id"] = color_id
            return redirect("shop:checkout")

    return redirect("cart:cart_detail")

def minus_cart(request, product_id):
    # 해당 product_id로 제품을 가져옴
    product = get_object_or_404(Product, id=product_id)
    
    try:
        # 로그인한 사용자와 비로그인 사용자 모두 처리
        if request.user.is_authenticated:
            # 로그인한 사용자의 경우 user 기반으로 Cart 가져오기
            cart = Cart.objects.get(user=request.user)
        else:
            # 비로그인 사용자의 경우 세션 기반으로 Cart 가져오기
            cart = Cart.objects.get(cart_id=_cart_id(request))
        
        # CartItem을 업데이트하거나 새로 생성
        cart_item, created = CartItem.objects.get_or_create(
            product=product,
            cart=cart,
            defaults={'quantity': 1}
        )
        if not created:
            # 이미 존재하는 경우 수량을 감소시킴
            if cart_item.quantity > 1:
                cart_item.quantity -= 1
                cart_item.save()
            else:
                cart_item.delete()
    except Cart.DoesNotExist:
        pass  # Cart가 존재하지 않으면 아무것도 하지 않음

    return redirect('cart:cart_detail')

def cart_detail(request):
    cart_items = []
    total = 0
    counter = 0

    try:
        # 로그인 사용자 처리
        if request.user.is_authenticated:
            cart = Cart.objects.get(user=request.user)
        else:
            # 비로그인 사용자는 세션 기반 장바구니 처리
            cart = Cart.objects.get(cart_id=_cart_id(request))

        # 장바구니 항목 가져오기
        cart_items = CartItem.objects.filter(cart=cart, active=True)

        # 총 가격 및 수량 계산
        for item in cart_items:
            total += (item.product.price * item.quantity)
            counter += item.quantity

    except Cart.DoesNotExist:
        cart_items = []

    return render(request, 'cart/cart.html', {
        'cart_items': cart_items,
        'total': total,
        'counter': counter
    })

def delete_selected_items(request):
    if request.method == "POST":
        selected_ids = request.POST.getlist("selected_items")
        
        # 사용자가 접근할 수 있는 CartItem만 필터링
        if request.user.is_authenticated:
            # 로그인한 사용자의 경우 user 기반으로 필터링
            CartItem.objects.filter(
                id__in=selected_ids,
                cart__user=request.user
            ).delete()
        else:
            # 비로그인 사용자의 경우 세션 기반으로 필터링
            CartItem.objects.filter(
                id__in=selected_ids,
                cart__cart_id=_cart_id(request)
            ).delete()
        
        return redirect("cart:cart_detail")
    
def update_quantity(request):
    if request.method == "POST":
        cart_item_id = request.POST.get("cart_item_id")
        quantity = int(request.POST.get("quantity"))

        try:
            # CartItem 조회
            cart_item = get_object_or_404(CartItem, id=cart_item_id)
            
            # 사용자가 해당 CartItem에 접근 권한이 있는지 확인
            if request.user.is_authenticated:
                # 로그인한 사용자의 경우 user 기반으로 확인
                if cart_item.cart.user != request.user:
                    return JsonResponse({"status": "error", "message": "Access denied."}, status=403)
            else:
                # 비로그인 사용자의 경우 세션 기반으로 확인
                if cart_item.cart.cart_id != _cart_id(request):
                    return JsonResponse({"status": "error", "message": "Access denied."}, status=403)

            if quantity > 0:
                cart_item.quantity = quantity
                cart_item.save()
                return JsonResponse({"status": "success", "quantity": cart_item.quantity})
            else:
                return JsonResponse({"status": "error", "message": "Invalid quantity."}, status=400)
        except Exception as e:
            return JsonResponse({"status": "error", "message": "An error occurred."}, status=500)

def delete_item(request):
    if request.method == "POST":
        cart_item_id = request.POST.get("cart_item_id")
        
        try:
            # CartItem 조회
            cart_item = get_object_or_404(CartItem, id=cart_item_id)
            
            # 사용자가 해당 CartItem에 접근 권한이 있는지 확인
            if request.user.is_authenticated:
                # 로그인한 사용자의 경우 user 기반으로 확인
                if cart_item.cart.user != request.user:
                    return JsonResponse({"status": "error", "message": "Access denied."}, status=403)
            else:
                # 비로그인 사용자의 경우 세션 기반으로 확인
                if cart_item.cart.cart_id != _cart_id(request):
                    return JsonResponse({"status": "error", "message": "Access denied."}, status=403)
            
            # CartItem 삭제
            cart_item.delete()
            return JsonResponse({"status": "success", "message": "Item deleted successfully."})
            
        except Exception as e:
            return JsonResponse({"status": "error", "message": "An error occurred."}, status=500)
    
    return JsonResponse({"status": "error", "message": "Invalid request method."}, status=405)