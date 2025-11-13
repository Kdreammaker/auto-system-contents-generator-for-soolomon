# 1. Python 3.10을 기본 이미지로 사용
FROM python:3.10-slim

# 2. 작업 디렉토리 설정
WORKDIR /app

# 3. 의존성 파일 복사 및 설치
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# 4. 전체 프로젝트 소스 코드 복사
COPY . .

# 5. Flask 앱 실행 포트 노출 (3000번)
EXPOSE 3000

# 6. 기본 실행 명령어 (Flask 서버)
CMD ["flask", "run", "--host=0.0.0.0", "--port=3000"]
