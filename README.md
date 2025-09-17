# 30cm 클론 코딩 프로젝트

## 📝 프로젝트 개요

- **프로젝트명**: 30cm - 29cm 클론 코딩 프로젝트
- **개발 기간**: 2024.05 ~ 2024.06 (현재 유지보수 중)
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

---

## 📷 스크린샷

### **로그인 & 메인 화면**
![로그인 화면](mediafiles/readme-images/login.png)
![메인 화면](mediafiles/readme-images/main_screen.png)

### **상품 디테일**
*사이즈, 색상, 수량 선택*
![상품 디테일](mediafiles/readme-images/product_detail.png)

### **장바구니**
*상품 추가, 개별/선택/전체 삭제*
![장바구니](mediafiles/readme-images/cart.png)

### **주문 및 결제**
*결제 전 주문 정보 확인*
![결제 전 주문 정보](mediafiles/readme-images/before_payment.png)

*iamport API를 활용한 결제*
![결제](mediafiles/readme-images/payment.png)

### **주문 내역**
*주문 시점의 상품 정보 확인*
![주문 내역](mediafiles/readme-images/order_history.png)

### **리뷰**
*구매 확정 상품에만 리뷰 작성 가능*
![리뷰 작성](mediafiles/readme-images/review1.png)
![리뷰 목록](mediafiles/readme-images/review2.png)

### **Q&A**
*상품별, 카테고리별 Q&A 작성*
*(Q&A 관련 이미지가 없어 비워두었습니다.)*