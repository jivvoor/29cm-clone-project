# shopsite-backend

How about 30cm?

https://29cm.co.kr/

---

## 📁 프로젝트 개요

- **프로젝트명**: 29cm 클론 코딩 프로젝트(How about 30cm?)
- **개발 기간**: [2024.05 ~ 2024.06] → 2025.08 유지보수 예정
- **담당 범위**: [ 전체 앱 개발 / 백엔드 연동 ]
- **Github** : https://github.com/jiwoo0123/30cm_project.git

## **👨‍👦‍👦팀 멤버**

**[FE] Hye-jin-Yoon**

**[BE] Ji-woo-Choi**

## **⚒ 기술 스택**

- **Frontend:** HTML, CSS, JavaScript
- **Backend:** Python, Django
- **Database:** MySQL
- **Version Control & Collaboration:** GitHub

## **📖 핵심 기능 (백엔드)**

- **회원가입 및 로그인**
    - **카카오, 네이버, 구글 소셜 로그인 API 연동**
    - **이메일 회원가입:** 이메일, 비밀번호 입력 시 유효성 검사
    - **로그인:** Email, PW 일치 검사
    - **JWT(JSON Web Token) 기반 로그인 유지:** `Access Token`과 `Refresh Token`을 `Cookie`에 저장하고, `interceptor`를 활용해 모든 페이지에서 로그인 상태 유지.
- **상품 관리**
    - **다단계 카테고리 구조 구현:** `Category`, `SubCategory`, `NestedSubCategory` 순으로 드롭다운 필터링 기능 구현. (Django의 `ForeignKey` 관계 활용)
    - **상품 리스트:** 카드 형태로 정렬
    - **상품 검색 기능:** 상품 이름 검색 및 가격, 색상, 사이즈별 필터링 기능.
- **장바구니**
    - **장바구니에 상품 추가, 개별 삭제 기능**
    - **전체 선택/해제 및 선택 삭제 기능**
    - **장바구니 비우기 (목록 전체 삭제)**
    - **데이터베이스 설계:** `User`와 `Product`를 연결하는 `CartProduct` 중간 테이블을 활용하여 다대다(N:M) 관계를 구현.
- **주문 및 결제**
    - **바로 구매하기:** 상품 상세 페이지에서 직접 주문/결제.
    - **선택 구매:** 장바구니에 담은 상품 중 원하는 상품만 선택하여 구매.
    - **주문 내역 확인:** 주문 시점의 상품명, 가격, 수량을 `OrderedProduct` 테이블에 저장하여 데이터 불변성 유지.
- **Q&A, 리뷰 및 좋아요**
    - **Q&A 작성**: 상품마다 QnA 카테고리별로 작성 가능.
    - **리뷰 작성:** 구매 확정 상태인 상품에만 리뷰 작성 가능.
    - **좋아요(Like) 기능:** 사용자가 상품에 좋아요를 누를 수 있는 기능 구현.
    

## 🔧 **트러블 슈팅**

### 카테고리 필터링 기능 구현 과정

### **1. 문제점**

프로젝트 초기에 데이터베이스 정규화를 위해 상품 모델(`Product`)에서 `category` 필드를 제거하고, `Category`, `SubCategory`, `NestedSubCategory`로 이어지는 3단계 계층 구조를 구현했습니다. 이로 인해 기존 뷰 함수가 상품을 필터링할 때 `product.category`와 같은 직접적인 접근 방식을 사용하면서 `FieldError`가 발생했습니다.

### **2. 해결 과정**

오류의 원인은 `Product` 모델이 더 이상 `category` 필드를 직접 가지지 않고, `nested_subcategory` 필드를 통해 상위 카테고리에 간접적으로 연결되기 때문임을 파악했습니다.

문제 해결을 위해 모든 카테고리 필터링 로직을 다음과 같이 수정했습니다.

- **수정 전** : `Product.objects.filter(category__slug=...)`
- **수정 후** : `Product.objects.filter(nested_subcategory__parent_subcategory__category__slug=...)`

`nested_subcategory`를 시작점으로 삼아, `__` (더블 언더스코어) 문법으로 관계를 따라가며 상위 카테고리 필드에 접근하도록 쿼리셋을 변경했습니다.

### **3. 결과 및 배운 점**

이러한 수정으로 사용자가 카테고리를 선택했을 때 올바른 상품 목록이 표시되도록 기능을 개선했습니다. 이 경험을 통해 **데이터베이스 정규화가 코드에 미치는 영향**과 **Django ORM의 관계형 쿼리**에 대한 이해를 깊게 할 수 있었습니다. 또한, 오류 메시지를 정확히 분석하고 모델 관계를 파악하는 것이 문제를 해결하는 가장 빠른 방법임을 배웠습니다.

---

## 🗄️ERD

![30cm (3).png](attachment:b745d602-d65d-4ef8-a29d-6c53b8712b30:30cm_(3).png)

---

## 📷 스크린샷

### 로그인 & 메인 화면

![image.png](attachment:43c3b0f0-e103-4bc2-b788-2b69b3c25909:image.png)

![image.png](attachment:010ea661-c03d-4b35-a13d-93b863445bfa:image.png)

---

### 상품 디테일 화면 - 사이즈, 색상, 수량 선택 로직 구현

![image.png](attachment:846b6cf9-1b5b-4c58-afe3-e56b0054cd20:image.png)

### 장바구니 - 장바구니에 상품 추가, 개별/선택/전체 삭제 기능

![image.png](attachment:0b4a9c51-1495-4aa0-b887-edf891aad28f:image.png)

### 결제 전 주문 정보 확인

![image.png](attachment:5d558287-8705-4252-b091-404da18908f9:image.png)

### iamport API를 사용해 결제 기능 구현

![image.png](attachment:00141da0-976e-48ca-b6e9-39c1c742553a:image.png)

### 주문 내역 확인 - 주문 시점의 상품명, 가격, 수량 정보 저장 및 확인

![스크린샷 2025-08-17 215539.png](attachment:352897ac-d6e0-4ece-916c-6016c4278f5c:스크린샷_2025-08-17_215539.png)

---

### 리뷰 작성 - 구매 확정 상태인 상품에만 리뷰 작성 가

![스크린샷 2025-08-17 215549.png](attachment:d62c7d58-ddb5-4d7d-bf8c-e4f19812c16e:스크린샷_2025-08-17_215549.png)

![스크린샷 2025-08-17 215637.png](attachment:30e3e6d5-b229-4171-8c22-6b43fd905069:스크린샷_2025-08-17_215637.png)

---

### Q&A 작성 - 상품별 Q&A 카테고리별로 작성 가능

![스크린샷 2025-08-17 215253.png](attachment:7716f633-cce6-43cf-962e-d405e7fa5cf9:스크린샷_2025-08-17_215253.png)

![스크린샷 2025-08-17 215319.png](attachment:d6ae80e6-ee45-4c94-82b8-eea197233337:8ed9f3bf-fede-4640-bf41-0390ef1983bf.png)
