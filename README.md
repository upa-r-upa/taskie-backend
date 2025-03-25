# Taskie
- 태스키는 투두, 루틴, 습관 서비스 모두를 한번에 관리할 수 있는 일정 관리 앱입니다.
- 투두/루틴/습관에서 완료한 할 일들을 '태스크' 라는 개념으로 묶어 보여줌으로써 간편하고 효율적으로 일정 관리를 할 수 있습니다.

- 더욱 상세한 서비스 설명은 client 레포를 참고해주세요.
- [Go to clinet repo](https://github.com/upa-r-upa/taskie-client)

## 프로젝트 실행 방법 (도커 사용 시)
### 1. 사전 준비
- Docker
- Docker Compose

### 2. 레포지터리 설치
```bash
git clone https://github.com/upa-r-upa/taskie-backend.git
cd taskie-backend
```

### 3. 최초 실행 혹은 코드 변경 시
 ```bash
 docker-compose build
 ```

### 4. 컨테이너 실행
   ```bash
   docker-compose up -d
 ```
### 5. 서버 확인
http://localhost:8000 에서 로컬 서버를 확인할 수 있습니다. (docs: http://localhost:8000/docs)

## 프로젝트 실행 방법 (도커 미사용 시)

### 1. 사전 준비
- Python >= 3.11
- poetry 

### 1. 레포지터리 설치
```bash
git clone https://github.com/upa-r-upa/taskie-backend.git
cd taskie-backend
```
### 2. 환경 변수 설정
```bash
cp .env.example .env
```
개발을 위해선 아무 값이나 넣어도 괜찮습니다.
docker-compose는 고정된 값이 따로 넣어져 있습니다.

### 3. 의존성 설치
```bash
poetry install
```
### 4. 데이터베이스 마이그레이션 진행

```bash
poetry run alembic upgrade head
```

### 5. 서버 실행

```bash
poetry run uvicorn app.main:app --reload
```

### 6. 서버 확인
http://localhost:8000 에서 로컬 서버를 확인할 수 있습니다. (docs: http://localhost:8000/docs)
