# 맛집가이드 (가제)
전국의 맛집을 공유하고 서로 리뷰 할 수 있는 사이트 입니다

<br/>

## 👨‍👨‍👧‍👦역할
|역할|팀원|
|--|--|
|메인페이지|[안진우](https://github.com/jinu-ahn)|  
|회원가입| [서정연](https://github.com/yeon1128)|  
|로그인|[손지아](https://github.com/JJIaa)|  
|카테고리별|[이혜민](https://github.com/hm5938)|  
|상세페이지|[김학준](https://github.com/lgkrwnsdll)|  
<br/>



## 📆프로젝트 기간
2022.08.01 ~ 2022.08.04 (총 4일)  
<br/>

  
## ⚙️주요 기능
- 메인페이지
![메인이미지]()
- 기본 기능
> 

- 회원가입/로그인/로그아웃
> 
![]()
<br/>


## 📑API
|기능|Method|url|Request|Response|
|------|---|---|---|---|
|회원가입|POST|/login/sign_in|이름, ID, 비밀번호|msg: 회원가입 완료|
|로그인했을 때 개인정보 전달|POST|/login|ID, PW|msg: 로그인 완료|
맛집 추천|POST|/post_place|URL, 카테고리, 별점, 코멘트, 추천자 ID|msg: 등록 완료|
|리뷰 작성(평점)|POST|/post_review|리뷰 , 별점, 작성자 ID|msg: 등록 완료
|리뷰 목록 조회|GET|/get_reviews| - |전체 리뷰 리스트
|맛집 검색|GET|/search_place|query = 식당 이름|검색 결과 식당 리스트|
맛집 목록 조회|GET|/<keyword>|- |전체 결과 식당 리스트|
<br/>
                                      



## 🛠️기술 스택
- View: HTML5, CSS3, Javascript 
- Framework: Flask(2.1.3)
- Database: MongoDB
- Server: AWS EC2
- etc: JWT(), jQuery, jinja2(3.1.2), pymongo(4.2.0), dnspython(2.2.1)
