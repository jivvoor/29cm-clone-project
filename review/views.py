from django.views.decorators.http import require_POST
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Review, ReviewImage
from .forms import ReviewForm, ReviewImageForm
from shop.models import Product

@login_required
@require_POST
def create_review(request, product_id):
    form = ReviewForm(request.POST)
    product = Product.objects.get(id=product_id)
    if form.is_valid():
        review = form.save(commit=False)
        review.user = request.user
        review.product = product
        review.save()
        # 이미지 여러 장 저장
        for file in request.FILES.getlist('images'):
            ReviewImage.objects.create(review=review, image=file)
        return JsonResponse({'success': True, 'message': '리뷰가 작성되었습니다.'})
    else:
        return JsonResponse({'success': False, 'errors': form.errors}, status=400)