# shopsite-backend

장고(Django) 기반 이커머스 백엔드 프로젝트입니다. 실무에서 요구되는 구조와 보안, API, 환경설정, 확장성을 모두 반영했습니다.

## 주요 특징
- **앱 분리**: shop, cart, lists, qna, review, users 등 도메인별 Django 앱 구조
- **보안**: SECRET_KEY, DB, 결제키 등 모든 민감 정보는 .env로 분리, .gitignore로 안전하게 관리
- **RESTful API**: Django REST Framework 기반 API 제공, drf-yasg(Swagger)로 문서 자동화(`/swagger/`, `/redoc/`)
- **소셜 로그인/결제**: allauth(구글/네이버/카카오), iamport(포트원) 연동
- **미디어/정적 파일 관리**: mediafiles/, uploads/ 구조화
- **테스트/마이그레이션/스크립트**: Django 표준 워크플로우 지원

## 실행 방법
1. 의존성 설치
	```bash
	pip install -r requirements.txt
	```
2. .env 파일 생성 (예시)
	```env
	SECRET_KEY=your-secret-key
	DEBUG=False
	DB_URL=sqlite:///db.sqlite3
	PORTONE_API_KEY=your-portone-key
	...
	```
3. DB 마이그레이션 및 슈퍼유저 생성
	```bash
	python manage.py makemigrations
	python manage.py migrate
	python manage.py createsuperuser
	```
4. 서버 실행
	```bash
	python manage.py runserver
	```

## 폴더 구조 예시
```
shop/        # 상품/카테고리 등 도메인 모델
cart/        # 장바구니
lists/       # 찜/리스트
qna/         # QnA
review/      # 리뷰
users/       # 사용자/인증
config/      # 프로젝트 설정
mediafiles/  # 업로드 이미지
uploads/     # 미디어 파일
```

## 보완/확장 포인트
- API 인증/권한(JWT 등), 서비스 계층 분리, 비동기 작업(Celery), 테스트 커버리지 확대, CI/CD 등 실무 확장성 고려

## 기타
- 프론트엔드는 별도 구현되어 있거나 외부에서 연동
- 커스텀 스크립트: import_products.py 등

---
실무 백엔드 개발에 필요한 구조와 보안, API, 확장성을 모두 반영한 포트폴리오용 프로젝트입니다.