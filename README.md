# 🛍️ ShopSite - Django 기반 이커머스 플랫폼

[![Django](https://img.shields.io/badge/Django-5.0.6-green.svg)](https://www.djangoproject.com/)
[![Python](https://img.shields.io/badge/Python-3.12+-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![API Documentation](https://img.shields.io/badge/API-Swagger-red.svg)](#api-문서)

> **실제 이커머스 서비스의 핵심 기능을 구현한 Django 기반 웹 애플리케이션**

## 📝 프로젝트 개요

- **프로젝트명**: ShopSite - Django 이커머스 플랫폼
- **개발 기간**: 2024.05 ~ 2024.06
- **참고 사이트**: [29cm](https://29cm.co.kr/)
- **GitHub**: [https://github.com/jivvoor/29cm-clone-project.git](https://github.com/jivvoor/29cm-clone-project.git)

### 🎯 프로젝트 목표
- Django의 핵심 기능을 활용한 실무 수준의 이커머스 플랫폼 구현
- RESTful API 설계 및 문서화
- 확장 가능한 아키텍처 설계
- 실제 서비스에서 사용되는 다양한 기술 스택 통합

---

## 🚀 주요 기능

### 👤 **사용자 관리**
- ✅ **소셜 로그인**: Google, Naver, Kakao OAuth 2.0 연동
- ✅ **이메일 회원가입**: Django Auth 시스템 기반
- ✅ **프로필 관리**: 사용자 정보 수정 및 관리
- ✅ **세션 관리**: 로그인/비로그인 사용자 모두 지원

### 📦 **상품 관리**
- ✅ **3단계 카테고리**: Category → SubCategory → NestedSubCategory
- ✅ **상품 검색**: 이름, 설명 기반 실시간 검색
- ✅ **필터링**: 카테고리, 가격, 색상, 사이즈별 필터링
- ✅ **상품 상세**: 이미지, 설명, 옵션 정보 제공

### 🛒 **장바구니 & 주문**
- ✅ **장바구니 CRUD**: 추가, 수정, 삭제, 수량 변경
- ✅ **선택 구매**: 장바구니에서 선택 상품만 주문
- ✅ **바로 구매**: 상품 상세에서 바로 주문
- ✅ **주문 내역**: 주문 시점 데이터 보존

### 💳 **결제 시스템**
- ✅ **포트원(Portone) PG**: 실제 결제 시스템 연동
- ✅ **다양한 결제 수단**: 카드, 계좌이체, 간편결제
- ✅ **결제 검증**: 서버 사이드 결제 검증

### 💬 **커뮤니티**
- ✅ **Q&A**: 상품별 문의사항 관리
- ✅ **리뷰 시스템**: 구매 확정 상품 리뷰 작성
- ✅ **좋아요**: 상품 찜하기 기능
- ✅ **공개/비공개**: Q&A 공개 여부 설정

### 📱 **API & 모바일 지원**
- ✅ **RESTful API**: Django REST Framework
- ✅ **API 문서화**: Swagger/OpenAPI 자동 생성
- ✅ **모바일 최적화**: 반응형 웹 디자인

---

## 🛠 기술 스택

### **Backend**
| 기술 | 버전 | 용도 |
|------|------|------|
| **Python** | 3.12+ | 메인 프로그래밍 언어 |
| **Django** | 5.0.6 | 웹 프레임워크 |
| **Django REST Framework** | Latest | API 개발 |
| **MySQL** | 8.0+ | 데이터베이스 |
| **Redis** | 7.0+ | 캐싱 (계획) |

### **Frontend**
| 기술 | 용도 |
|------|------|
| **HTML5** | 마크업 |
| **CSS3** | 스타일링 |
| **JavaScript (ES6+)** | 동적 기능 |
| **Bootstrap** | UI 프레임워크 |

### **외부 서비스**
| 서비스 | 용도 |
|--------|------|
| **Google OAuth** | 소셜 로그인 |
| **Naver OAuth** | 소셜 로그인 |
| **Kakao OAuth** | 소셜 로그인 |
| **포트원(Portone)** | 결제 시스템 |

### **개발 도구**
| 도구 | 용도 |
|------|------|
| **Git** | 버전 관리 |
| **GitHub** | 코드 저장소 |
| **Swagger** | API 문서화 |
| **Django Debug Toolbar** | 개발 디버깅 |

---

## 📊 프로젝트 구조

```
shopsite/
├── 📁 config/                 # 프로젝트 설정
│   ├── settings.py            # Django 설정
│   ├── urls.py               # 메인 URL 설정
│   └── wsgi.py               # WSGI 설정
├── 📁 shop/                  # 상품 관리 앱
│   ├── models.py             # 상품, 카테고리 모델
│   ├── views.py              # 상품 관련 뷰
│   ├── api.py                # 상품 API
│   └── serializers.py        # API 시리얼라이저
├── 📁 cart/                  # 장바구니 앱
│   ├── models.py             # 장바구니 모델
│   ├── views.py              # 장바구니 뷰
│   └── api.py                # 장바구니 API
├── 📁 users/                 # 사용자 관리 앱
│   ├── models.py             # 사용자 모델
│   ├── views.py              # 인증 뷰
│   └── forms.py              # 폼 정의
├── 📁 review/                # 리뷰 앱
├── 📁 qna/                   # Q&A 앱
├── 📁 lists/                 # 찜하기 앱
├── 📁 mediafiles/            # 업로드된 파일
└── 📁 uploads/               # 미디어 파일
```

---

## 🚀 시작하기

### 1. 저장소 클론
```bash
git clone https://github.com/jivvoor/shopsite-backend.git
cd shopsite-backend
```

### 2. 가상환경 설정
```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

### 3. 의존성 설치
```bash
pip install -r requirements.txt
```

### 4. 환경 변수 설정
`.env` 파일을 생성하고 다음 내용을 추가하세요:

```env
# Django 설정
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# 데이터베이스 설정
DB_ENGINE=django.db.backends.mysql
DB_NAME=shopsite_db
DB_USER=your_db_user
DB_PASSWORD=your_db_password
DB_HOST=localhost
DB_PORT=3306

# 포트원 결제 설정
PORTONE_API_KEY=your-portone-api-key
PORTONE_API_SECRET=your-portone-api-secret
PORTONE_SHOP_ID=your-shop-id

# 소셜 로그인 설정
GOOGLE_OAUTH2_CLIENT_ID=your-google-client-id
GOOGLE_OAUTH2_CLIENT_SECRET=your-google-client-secret
NAVER_OAUTH2_CLIENT_ID=your-naver-client-id
NAVER_OAUTH2_CLIENT_SECRET=your-naver-client-secret
KAKAO_OAUTH2_CLIENT_ID=your-kakao-client-id
```

### 5. 데이터베이스 설정
```bash
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
```

### 6. 서버 실행
```bash
python manage.py runserver
```

---

## 📚 API 문서

### 🔗 API 엔드포인트

#### **상품 API**
- `GET /shop/api/products/` - 상품 목록 조회
- `GET /shop/api/products/{id}/` - 상품 상세 조회
- `GET /shop/api/products/featured/` - 추천 상품 조회
- `GET /shop/api/products/search/?q={query}` - 상품 검색

#### **카테고리 API**
- `GET /shop/api/categories/` - 카테고리 목록 조회
- `GET /shop/api/categories/{id}/products/` - 카테고리별 상품 조회
- `GET /shop/api/subcategories/` - 서브카테고리 목록 조회

#### **장바구니 API**
- `GET /cart/api/cart/` - 장바구니 조회
- `POST /cart/api/cart/add_item/` - 장바구니에 상품 추가
- `POST /cart/api/cart/remove_item/` - 장바구니에서 상품 제거
- `POST /cart/api/cart/update_quantity/` - 상품 수량 업데이트
- `POST /cart/api/cart/clear/` - 장바구니 비우기

### 📖 API 문서 보기
- **Swagger UI**: http://localhost:8000/swagger/
- **ReDoc**: http://localhost:8000/redoc/

---

## 🧪 테스트

### 테스트 실행
```bash
# 전체 테스트 실행
python manage.py test

# 특정 앱 테스트
python manage.py test cart
python manage.py test shop
python manage.py test users

# 커버리지 리포트 생성
coverage run --source='.' manage.py test
coverage report
coverage html
```

### 테스트 커버리지
- ✅ **모델 테스트**: 모든 모델의 기본 기능 테스트
- ✅ **뷰 테스트**: HTTP 요청/응답 테스트
- ✅ **API 테스트**: REST API 엔드포인트 테스트
- ✅ **인증 테스트**: 로그인/로그아웃 테스트
- ✅ **권한 테스트**: 접근 권한 검증 테스트

---

## 🔒 보안 고려사항

### ✅ 구현된 보안 기능
- **환경 변수**: 민감한 정보 `.env` 파일로 분리
- **CSRF 보호**: Django CSRF 미들웨어 활용
- **SQL Injection 방지**: Django ORM 사용
- **XSS 방지**: 템플릿 자동 이스케이핑
- **접근 권한**: 사용자별 데이터 접근 제어
- **세션 보안**: 안전한 세션 관리

### 🔄 향후 보안 강화 계획
- **Rate Limiting**: API 호출 제한
- **JWT 토큰**: API 인증 강화
- **HTTPS**: SSL/TLS 인증서 적용
- **로그 모니터링**: 보안 로그 추적

---

## 📈 성능 최적화

### ✅ 구현된 최적화
- **데이터베이스 인덱싱**: 자주 조회되는 필드 인덱스 설정
- **쿼리 최적화**: select_related, prefetch_related 활용
- **API 페이지네이션**: 대용량 데이터 처리
- **이미지 최적화**: Pillow를 활용한 이미지 리사이징

### 🚀 향후 최적화 계획
- **Redis 캐싱**: 자주 조회되는 데이터 캐싱
- **CDN**: 정적 파일 전송 최적화
- **데이터베이스 최적화**: 쿼리 성능 튜닝
- **비동기 처리**: Celery를 활용한 백그라운드 작업

---

## 🐳 배포 (Docker)

### Dockerfile 생성 예시
```dockerfile
FROM python:3.12-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
```

### Docker Compose 예시
```yaml
version: '3.8'
services:
  web:
    build: .
    ports:
      - "8000:8000"
    environment:
      - DEBUG=False
    depends_on:
      - db
  
  db:
    image: mysql:8.0
    environment:
      MYSQL_DATABASE: shopsite_db
      MYSQL_ROOT_PASSWORD: rootpassword
    volumes:
      - mysql_data:/var/lib/mysql

volumes:
  mysql_data:
```

---


## 📄 라이선스

이 프로젝트는 MIT 라이선스 하에 배포됩니다. 자세한 내용은 `LICENSE` 파일을 참조하세요.

---

## 👨‍💻 개발자

| 역할 | 이름 | GitHub |
|------|------|--------|
| **Frontend** | Hye-jin-Yoon | [@hyjin-yoon](https://github.com/hyjin-yoon) |
| **Backend** | Ji-woo-Choi | [@jivvoor](https://github.com/jivvoor) |

---

## 🎯 향후 계획

### 📋 단기 목표 (1-2개월)
- [ ] **테스트 커버리지 90% 이상 달성**
- [ ] **API 문서화 완성**
- [ ] **Docker 컨테이너화**
- [ ] **CI/CD 파이프라인 구축**

### 🚀 중기 목표 (3-6개월)
- [ ] **모바일 앱 API 개발**
- [ ] **실시간 알림 시스템**
- [ ] **관리자 대시보드**
- [ ] **분석 및 통계 기능**

### 🌟 장기 목표 (6개월+)
- [ ] **마이크로서비스 아키텍처 전환**
- [ ] **AI 추천 시스템**
- [ ] **다국어 지원**
- [ ] **클라우드 배포**

---


<div align="center">

**⭐ 이 프로젝트가 도움이 되었다면 스타를 눌러주세요! ⭐**

Made with ❤️ wisdom Team

</div>

