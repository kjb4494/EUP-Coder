# EUP-Coder
- 필수 라이브러리 설치
```
pip install -r requirements.txt
```

- 로컬 데이터베이스 구성
```
python3 manage.py makemigrations backend
python3 manage.py migrate
python3 manage.py createcachetable JsonFileChecksum
```

- 관리자 계정 생성
```
python3 manage.py createsuperuser
```

- 실행
```
python3 manage.py runserver 8000
```