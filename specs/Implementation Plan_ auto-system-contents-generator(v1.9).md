# **Implementation Plan: auto-system-contents-generator**

## **🚨 필수 작업 규칙 🚨**

### **1\. 작업 폴더 확인**

**모든 작업은 반드시 "C:\Users\User\Downloads\auto-system-contents-generator" 폴더에서만 진행**

* 작업 시작 전 현재 폴더 확인: Get-Location 또는 pwd  
* 다른 폴더에서 작업 절대 금지

### **2. 코드 품질 원칙 필수**

**모든 코드는 다음 원칙을 준수해야 합니다**

* **상세한 한글 주석**: 모든 파일, 함수, 복잡한 로직(예: Shortcode 파서)에 한글 주석 작성  
* **작은 단위로 분리**: 파일은 150줄 이하, 함수는 50줄 이하 권장  
* **컴포넌트 분리**: 재사용 가능한 부분은 독립 컴포넌트로 분리 (Python 모듈, Jinja2 매크로 등)  
* **타입 안전성**: 모든 Python 함수 매개변수 및 반환 값에 타입 힌트 명시  
* **에러 처리**: Design Document (Chapter 7)의 모든 시나리오를 코드로 구현

### **3. GitHub 백업 및 버전 관리**

**새로운 Task를 시작하기 전에, 이전 Task의 완결을 의미하는 커밋을 반드시 GitHub에 푸시합니다.**

#### **Task 시작 전 백업 절차**

1. **현재 작업 폴더 확인 (필수\!)**  
   Get-Location  
   # 결과가 C:\Users\User\Downloads\auto-system-contents-generator 인지 확인

2. **현재 작업 상태 확인** (이전 Task의 변경사항이 남아있는지 확인)  
   git status

3. **이전 Task의 모든 변경사항 커밋**  
   git add .  
   git commit \-m "feat: Task [N-1] 완료 \- [이전 Task 요약]"

   예: git commit \-m "feat: Task 1 완료 \- Docker 환경 설정"  
4. **GitHub에 푸시**  
   git push origin main

5. **백업 확인**  
   git log \--oneline \-1  
   # 방금 올린 커밋이 최신인지 확인

#### **백업 타이밍**

* ✅ **새 Task 시작 시**: 이전 Task의 완결을 의미하는 커밋 및 푸시 (필수)  
* ✅ **작업 중단 시**: 작업을 중단하기 전 backup: 커밋으로 푸시  
* ✅ **위험한 작업 전**: 대규모 리팩토링 전 refactor: 커밋으로 푸시

#### **커밋 메시지 규칙**

feat: Task [N] 완료 \- [간단한 설명]  
fix: Task [N] 버그 수정 \- [설명]  
refactor: Task [N] 리팩토링 \- [설명]  
backup: Task [N] 작업 중 안전 백업

### **4. Spec 문서 버전 관리**

* **Task 진행 원칙**: Tasks Document의 체크리스트([ ])를 순서대로 따릅니다.  
* **Task 완료 시**: PM(개발자)은 해당 Task의 [ ]를 [x]로 **직접 체크**합니다.  
* **변경 사항 발생 시**: 작업 과정에서 requirements.md 또는 design.md의 변경이 필요하다고 판단되면, **즉시 해당 specs/ 문서를 업데이트**합니다.  
* **문서 커밋**: **업데이트된 specs/ 문서를 최우선으로 Git에 커밋**하여 항상 최신 상태의 명세서를 유지합니다.

### **5. 작업 프로세스**

1. **Task 분석**: Design Document를 참조하여 작업 범위 및 복잡도 파악  
2. **코드 작성**: 한글 주석, 모듈 분리, 타입 힌트, 디자인 시스템 준수  
3. **검증**: Linter(Flake8, Black) 검사, docker-compose up 실행, localhost:3000 UI/UX 검증  
4. **완료**: Tasks Document의 해당 항목 [x] 체크

## **🚀 Tasks**

* [x] **Task 1: 환경 설정 (Environment Setup)**  
  * [x] 1.1 Design Document의 Project Structure 섹션에 따라 전체 프로젝트 폴더 구조 생성  
  * [x] 1.2 requirements.txt 파일 생성 및 Design Document의 Technology Stack 섹션에 명시된 Python 의존성 추가  
  * [x] 1.3 Dockerfile 및 docker-compose.yml 파일 작성 (Design Document, Development Environment (Docker) 섹션 참조)  
  * [x] 1.4 .env.example 파일 작성 (모든 필요 API 키 명시)  
  * [x] 1.5 docker-compose up --build 명령어로 Flask, Redis, Celery가 오류 없이 실행되는지 확인  
* [x] **Task 2: 백엔드 API 및 비동기 뼈대 (Backend Skeleton)**  
  * [x] 2.1 dashboard/app.py에 Flask 앱 초기화 및 Celery/Redis 연동 설정  
  * [x] 2.2 Design Document의 API Endpoints 섹션에 명시된 모든 엔드포인트를 '가짜(Mock)' 데이터로 구현  
  * [x] 2.3 POST /api/cycle/run/<step_id>가 Celery 작업을 트리거하고 HTTP 202를 반환하는지 테스트  
  * [x] 2.4 GET /api/cycle/status가 manifest.json 파일의 status 객체를 읽어 JSON으로 반환하는지 테스트  
  * [x] 2.5 manifest.json 스키마(Design Document, Data Models 섹션)에 맞춘 파일 읽기/쓰기 유틸리티 함수 구현  
  * [x] 2.6 Design Document의 '멱등성(S-1)' 로직 구현 (중복 작업 실행 방지)  
* [x] **Task 3: 대쉬보드 UI 뼈대 (Frontend Skeleton)**  
  * [x] 3.1 dashboard/templates/에 기본 layout.html 생성  
  * [x] 3.2 layout.html에 CDN을 통해 Bootstrap 5, Remix Icon, Google Fonts 로드  
  * [x] 3.3 View 1: 메인 페이지 (/) UI 뼈대 구현 (버튼, 목록)  
  * [x] 3.4 View 2: 사이클 대쉬보드 (/cycle/<YYMMDD>) UI 뼈대 구현 (14단계 리스트, 로그 뷰어)  
  * [x] 3.5 Modal 1, 2, 3, 4의 기본 HTML/CSS 뼈대 구현 (Bootstrap Modals)  
  * [x] 3.6 dashboard/static/에 EasyMDE 라이브러리 파일(.js, .css) 추가  
* [ ] **Task 4: 프론트-백엔드 연동 (UI Wiring)**  
  * [ ] 4.1 View 1의 [새 사이클 시작] 버튼(Modal 1)이 POST /api/cycle/start를 호출하고, manifest.json 생성 후 View 2로 리디렉션되는 흐름 완성  
  * [ ] 4.2 View 2가 5초마다 GET /api/cycle/status를 폴링(polling)하여 14단계의 status.text를 UI에 업데이트하는 로직 구현 (Vanilla JS)  
  * [ ] 4.3 View 2의 [Step N 실행] 버튼이 POST /api/cycle/run/<step_id>를 호출하고 UI를 '진행중' 상태로 즉시 변경하는 로직 구현 (버튼 disabled 처리 포함)  
* [ ] **Task 5: Step 1~2 (기획) 파이프라인 연동**  
  * [ ] 5.1 run_pipeline.py에 Step 1 (자료 조사) 로직 구현 (Perplexity API 호출, step1-research.md 저장)  
  * [ ] 5.2 Step 1 완료 시 manifest.json의 status를 STEP_2_PENDING_APPROVAL로 업데이트하는 로직 구현  
  * [ ] 5.3 [Human 1] (Step 2): View 2에서 [검토하기] 버튼 클릭 시 '간이 폼(Modal 1 변형)'을 열어 selection.json을 저장하고 '승인'(POST /api/cycle/approve/2)하는 기능 구현  
* [ ] **Task 6: Step 3~4 (설계) 파이프라인 연동**  
  * [ ] 6.1 run_pipeline.py에 Step 3 (구조 설계) 로직 구현 (Prompt 2 호출, step2-outline.md 저장)  
  * [ ] 6.2 Step 3 완료 시 manifest.json의 status를 STEP_4_PENDING_APPROVAL로 업데이트  
  * [ ] 6.3 [Human 2] (Step 4): View 2에서 [검토하기] 버튼 클릭 시 Modal 2를 열어 GET /api/cycle/content?file=step2-outline.md로 콘텐츠 로드  
  * [ ] 6.4 Modal 2의 EasyMDE 에디터 및 [저장], [승인] 버튼 기능 구현 (POST /api/cycle/content, POST /api/cycle/approve/4)  
* [ ] **Task 7: Step 5~6 (콘텐츠 작성/검수) 파이프라인 연동**  
  * [ ] 7.1 run_pipeline.py에 Step 5 (풀 콘텐츠 작성) 로직 구현 (Prompt 3 + component_guide.md 참조, step3-content-raw.md 저장)  
  * [ ] 7.2 run_pipeline.py에 Step 6 (기초 검수) 로직 구현 (Claude API 호출, step3-revised-final.md 및 *-w.feedback.md 저장)  
  * [ ] 7.3 Step 6 완료 시 manifest.json status를 STEP_7_PENDING (다음 단계 자동 실행 대기)으로 업데이트  
* [ ] **Task 8: Step 7 (리치 콘텐츠 렌더링) 엔진 구현**  
  * [ ] 8.1 components/ 폴더에 예시 컴포넌트 2개(예: PremiumBanner.html, WineCard.html) (Jinja2) 작성  
  * [ ] 8.2 guidelines/component_guide.md 파일에 [PremiumBanner] 및 [WineCard: {...}] 사용법 명세 작성  
  * [ ] 8.3 run_pipeline.py에 Step 7 (리치 렌더링) 로직 구현  
  * [ ] 8.4 markdown-it-py 플러그인을 사용하여 Shortcode([... ])를 감지하는 로직 구현  
  * [ ] 8.5 Jinja2를 사용하여 감지된 Shortcode를 components/의 HTML 파일로 치환하고 JSON 데이터를 주입하는 로직 구현  
  * [ ] 8.6 최종 렌더링 결과를 templates/blog-post-default.html에 삽입하여 step3-revised-final.html 파일 생성  
  * [ ] 8.7 Step 7 완료 시 manifest.json status를 STEP_8_PENDING_APPROVAL로 업데이트  
* [ ] **Task 9: Step 8 (원본 검수) UI/UX 구현**  
  * [ ] 9.1 [Human 3] (Step 8): [검토하기] 버튼 클릭 시 Modal 2 로드  
  * [ ] 9.2 Modal 2의 "Markdown" 탭에 step3-revised-final.md를 로드  
  * [ ] 9.3 Modal 2의 "HTML 프리뷰" 탭에 step3-revised-final.html을 <iframe>으로 로드  
  * [ ] 9.4 [승인] 버튼(POST /api/cycle/approve/8) 기능 구현  
* [ ] **Task 10: Step 9~11 (SNS) 파이프라인 연동**  
  * [ ] 10.1 run_pipeline.py에 Step 9 (SNS 변형) 로직 구현 (Prompt 4 호출, step4-social-raw.md 저장)  
  * [ ] 10.2 run_pipeline.py에 Step 10 (SNS 검수) 로직 구현 (Claude API 호출, step4-social-final.md 저장)  
  * [ ] 10.3 Step 10 완료 시 manifest.json status를 STEP_11_PENDING_APPROVAL로 업데이트  
  * [ ] 10.4 [Human 4] (Step 11): [검토하기] 버튼으로 Modal 2에서 step4-social-final.md 검수 및 승인 기능 구현  
* [ ] **Task 11: Step 12~13 (번역) 파이프라인 연동**  
  * [ ] 11.1 run_pipeline.py에 Step 12 (전체 번역) 로직 구현  
    * (1) 승인된 step3-revised-final.md 번역 (DeepL API)  
    * (2) 승인된 step4-social-final.md 번역 (DeepL API)  
    * (3) step5-translation/ 폴더에 결과 저장  
  * [ ] 11.2 run_pipeline.py에 Step 13 (번역 검수) 로직 구현 (Claude API 호출, step6-qc/ 폴더에 최종본 및 피드백 저장)  
  * [ ] 11.3 Step 13 완료 시 manifest.json status를 STEP_14_PENDING_APPROVAL (배포 대기)로 업데이트  
* [ ] **Task 12: 대쉬보드 편의기능 구현**  
  * [ ] 12.1 Step 1 예약 기능 (Modal 3) 및 APScheduler 연동  
  * [ ] 12.2 Modal 2 에디터 툴바에 [이모지/에셋 삽입] 버튼 (Modal 4) 기능 구현  
  * [ ] 12.3 Modal 2 에디터 툴바에 [컴포넌트 삽입] 버튼 (GET /api/components) 기능 구현  
  * [ ] 12.4 View 1의 '과거 사이클 목록' (GET /api/cycles) 기능 구현  
  * [ ] 12.5 Design Document의 '싱글톤 예약(S-2)' (Redis Lock) 로직 구현  
* [ ] **Task 13: 에러 핸들링 및 안정화**  
  * [ ] 13.1 Design Document (Chapter 7)의 '환경/설정 오류' 시나리오 구현 (로그 뷰어에 명확한 한글 메시지 출력)  
  * [ ] 13.2 Design Document (Chapter 7)의 '외부 API 오류' 시나리오 구현 (최대 3회 자동 재시도, 401/400 즉시 실패 및 로그 출력)  
  * [ ] 13.3 Design Document (Chapter 7)의 '비동기 오류' 시나리오 구현 (Redis 연결 실패 Toast 알림, 작업 타임아웃 상태 변경)  
  * [ ] 13.4 Design Document (Chapter 7)의 'UX/무결성 오류' 시나리오 구현 (에디터 저장 실패 시 '클립보드 복사' Toast 알림)  
  * [ ] 13.5 Design Document (Chapter 7)의 '렌더링 오류' 시나리오 구현 (Shortcode 문법 오류/컴포넌트 누락 시 로그 출력 및 프리뷰에 에러 메시지 표시)