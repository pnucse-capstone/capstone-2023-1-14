# 지하철 내 주의가 필요한 인물 및 분실물 탐지

## 1. 프로젝트 소개
- 프로젝트 명 : 라즈베리 파이를 이용한 스마트폰 부품 판별 시스템
- 프로젝트 배경 : 현대 사회에서 공공장소에서의 범죄와 안전 문제 등이 지속적으로 발생하고 있으며, 대부분의 CCTV는 단순히 촬영 및 녹화의 기능만 하고 있다.
또한 사람들이 많이 몰리는 장소에서는 눈에 띄지 않는 분실물이나 주의가 필요한 인물을 놓치기 쉬워 신속한 대응이 어렵다.
이러한 문제들을 해결하기 위해 인공지능과 빅데이터를 활용한 CCTV 분석이 필요하다. 
- 프로젝트목표: 본 연구의 목표는 공공장소의 안전과 편의성 향상을 위해 주의가 필요한     인물과 분실물을 탐지할 수 있는 학습 모델을 개발하고,
웹페이지를 통해 해당 영상을 분석하고 탐지 결과를 표시하며, 목표물을 탐지하였을 때 알림을 발생시켜 탐지 효과를 늘리는 것이다. 
## 2. 팀 소개
### Team 컴퓨터좋아
|이름|이메일|역활|
|:-:|:-:|:-:|
|윤영채|youngchae66@gmail.com|데이터 어노테이션 및 분실물 탐지|
|노현수|heredell42@gmail.com|웹 인터페이스 및 데이터 베이스|
|디미트로바 딜랴나 베셀리노바|dimitrova55@pusan.ac.kr|학습 모델 생성|


## 3. 구성도
![img](https://github.com/pnucse-capstone/capstone-2023-1-14/assets/101184475/3e87161b-1607-4687-8044-f8166a9a8cdb)
![img](https://github.com/pnucse-capstone/capstone-2023-1-14/assets/101184475/82295c1c-afdc-4197-8834-8f221bc5489e)



## 4. 소개 및 시연 영상
11/1일 업로드 예정

## 5. 사용법
### Python Requirements
```
pip install -r requirements.txt
```

__개발 환경 버전__
|이름|버전|
|:-:|:-:|
|Python|v3.10.13|
|flask|v2.2.2|
|opencv-python|v4.8.0.76|
|werkzeug|v2.2.3| 
|ultralytics|v8.0.162| 
|supervision|v0.13.0|
|numpy|v1.24.3|
|matplotlib|v3.7.1|
|Pillow|v9.4.0|
|waitress|---|

### waitress 서버 실행

```
python app.py
```

### 웹 접속

웹 브라우저에서 localhost로 접속
```
http://localhost:8080
```