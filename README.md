# Taskie
- 태스키는 투두, 루틴, 습관 서비스 모두를 한번에 관리할 수 있는 일정 관리 앱입니다.
- 투두/루틴/습관에서 완료한 할 일들을 '태스크' 라는 개념으로 묶어 보여줌으로써 간편하고 효율적으로 일정 관리를 할 수 있습니다.

## link
[Go to clinet repo](https://github.com/upa-r-upa/taskie-client)

## 서비스 소개
### Task (태스크)
- 투두부터, 루틴 내부의 할 일, 습관 모두를 '태스크'라는 개념으로 묶어서 확인할 수 있습니다.
- 오늘의 태스크, 이번주 태스크 등으로 손쉽게 일정을 확인할 수 있습니다.
### Todo (투두) 서비스
- 가장 기본적인 할 일 관리인 투두 서비스입니다.
- **(개발 예정)** 단기 목표부터, 장기 목표까지 모두 관리할 수 있습니다.
- **(개발 예정)** 캘린더와 연동하여 할 일들을 통합해 확인할 수 있습니다. 
### Routine (루틴) 서비스
- 여러 투두를 하나의 루틴으로 묶어 순서대로, 각 필요한 시간에 맞추어 실행할 수 있습니다.
- 예를 들어 월-금 아침 7시마다 '미라클 모닝' 루틴(1. 물 마시기 (5분), 2. 명상하기 (10분), ...)을 만들어 순서대로 할 일을 진행할 수 있습니다. 
### Habit (습관) 서비스
- 특정 주기별로 반복되는 투두를 만들 수 있습니다.
- 예를 들어 '물 마시기' 습관을 매일 2시간마다 진행해 건강한 생활 습관을 만들 수 있습니다.
- 예를 들어 '이불 빨래하기' 습관을 2주 마다 반복되게 하여 자주 하지 않는 일을 까먹지 않고 관리할 수 있습니다.

## 프로젝트 실행 방법 (도커 사용 시)
### 1. 사전 준비
- Docker
- Docker Compose

### 2. 레포지터리 설치
```bash
git clone https://github.com/upa-r-upa/taskie_backend.git
cd taskie_backend
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
git clone https://github.com/upa-r-upa/taskie_backend.git
cd taskie_backend
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
