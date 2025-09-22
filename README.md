# Django 기반 29cm 클론 코딩 프로젝트 - BACKEND

## 📝 프로젝트 개요

- **프로젝트명**: Django 기반 29cm 클론 코딩 프로젝트
- **개발 기간**: 2024.05 ~ 2024.06
- **참고 사이트**: [29cm](https://29cm.co.kr/)
- **GitHub**: [https://github.com/jiwoo0123/30cm_project.git](https://github.com/jiwoo0123/30cm_project.git)

---

## 👨‍💻 팀 멤버

| 역할 | 이름 |
| --- | --- |
| **Frontend** | Hye-jin-Yoon |
| **Backend** | Ji-woo-Choi |

---

## 🛠 기술 스택

| 구분 | 기술 |
| --- | --- |
| **Frontend** | HTML, CSS, JavaScript |
| **Backend** | Python, Django |
| **Database** | MySQL |
| **Version Control** | Git, GitHub |

---

## 📖 핵심 기능 (Backend)

### **👤 회원 관리**
- **소셜 로그인**: 카카오, 네이버, 구글 소셜 로그인 API 연동
- **이메일 회원가입**: 이메일, 비밀번호 유효성 검사
- **로그인**: JWT (Access Token, Refresh Token) 기반 로그인 유지

### **📦 상품 관리**
- **다단계 카테고리**: 3단계 카테고리 (`Category` > `SubCategory` > `NestedSubCategory`) 구조
- **상품 필터링**: 이름, 가격, 색상, 사이즈별 필터링 및 검색

### **🛒 장바구니**
- **CRUD**: 장바구니 상품 추가, 개별/선택/전체 삭제
- **데이터베이스**: `User`와 `Product`를 연결하는 `CartProduct` 중간 테이블 (N:M 관계)

### **💳 주문 및 결제**
- **다양한 주문**: 바로 구매, 선택 구매 기능
- **주문 내역**: 주문 시점의 데이터 불변성 유지를 위해 `OrderedProduct` 테이블에 정보 저장

### **💬 커뮤니티**
- **Q&A**: 상품별, 카테고리별 Q&A 작성
- **리뷰**: 구매 확정 상품에만 리뷰 작성 가능
- **좋아요**: 상품별 '좋아요' 기능

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

