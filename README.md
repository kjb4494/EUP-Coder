# EUP-Coder
#### 환경구성 설정
- 필수 라이브러리 설치
```
pip install -r requirements.txt
```

#### 초기화 절차
- 로컬 데이터베이스 구성
```
python3 manage.py makemigrations backend
python3 manage.py migrate
python3 manage.py createcachetable JsonFileChecksum
python3 manage.py loaddata modifier-type-settings-info.json
```

- 관리자 계정 생성
```
python3 manage.py createsuperuser
```

#### 실행
- 실행
```
python3 manage.py runserver 8000
```