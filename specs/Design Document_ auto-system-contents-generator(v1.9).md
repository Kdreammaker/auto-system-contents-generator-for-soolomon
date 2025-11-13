# **Design Document: auto-system-contents-generator**

## **1\. Overview**

이 문서는 auto-system-contents-generator의 기술 아키텍처, 데이터 모델, API 명세 및 개발 환경을 정의합니다. 본 설계의 핵심은 **'확장 마크다운(Shortcode)'** 아키텍처와, 긴 AI 작업을 처리하기 위한 **'비동기 Task Queue'**, 그리고 API 비용 폭증을 방지하기 위한 \*\*'안전장치(Safeguards)'\*\*입니다.

## **2\. Architecture (아키텍처)**

### **2.1. 기술 스택 (Technology Stack)**

* **백엔드 (Backend)**: Python 3.10+, Flask  
* **프론트엔드 (Frontend)**: Vanilla JavaScript (ES6+), HTML5, CSS3  
* **비동기 (Async)**: Celery, Redis  
* **UI/UX (Frontend Libs)**:  
  * CSS 프레임워크: **Bootstrap 5 (CDN)**  
  * 아이콘: **Remix Icon (CDN)**  
  * 폰트: **Google Fonts (CDN)**  
  * 에디터: **EasyMDE**  
* **렌더링 (Rendering)**:  
  * 파서: **markdown-it-py**  
  * 템플릿 엔진: **Jinja2**  
* **실행 환경**: **Docker Compose**

### **2.2. 핵심 설계: 확장 마크다운 (Shortcode)**

ContentDetailClient.tsx와 같은 리치 콘텐츠를 위해, AI는 단순 Markdown이 아닌 '확장 마크다운'을 생성합니다.

* **AI 생성물 (.md)**:  
  \# 스테이크와 와인  
  일반 텍스트 본문입니다.  
  \[WineCard: {"name": "카베르네 소비뇽", "price": "₩120,000"}\]  
  \[PremiumBanner\]

* **PM 정의 컴포넌트 (components/WineCard.html)**:  
  \<div class="wine-card"\>  
    \<h3\>{{ name }}\</h3\>  
    \<p\>{{ price }}\</p\>  
  \</div\>

* **Step 7 렌더링 로직 (Python)**:  
  1. markdown-it-py가 \[WineCard: {...}\] 태그를 감지합니다.  
  2. Jinja2가 components/WineCard.html 템플릿을 로드합니다.  
  3. JSON 데이터({...})를 props로 주입하여 렌더링합니다.  
  4. \[PremiumBanner\]는 components/PremiumBanner.html로 치환됩니다.

### **2.3. 비동기 아키텍처 다이어그램**

graph TD  
    A\[PM (사용자)\] \<--\> B\[\<b\>대쉬보드 (Web UI @ localhost:3000)\</b\>\];  
      
    subgraph "로컬 서버 환경 (Docker Compose)"  
        B \-- (1. API 요청)\<br/\>POST /api/cycle/run/5 \--\> C\[Web Server (Flask)\];  
        C \-- (2. 0.1초 내 즉시 응답)\<br/\>HTTP 202 Accepted \--\> B;  
        C \-- (3. 작업 전달) \--\> R\[Task Queue (Redis)\];  
        W\[Celery Worker (별도 컨테이너)\] \-- (4. 작업 수신) \--\> R;  
        W \-- (5. 파이프라인 실행) \--\> D\[Python Pipeline Core (run\_pipeline.py)\];  
    end

    subgraph "외부 API"  
        D \-- (6. AI API 호출) \--\> E\[External APIs (Google, Claude, DeepL)\];  
    end

    subgraph "로컬 파일 시스템"  
         D \-- (7. 파일 쓰기/읽기) \--\> F\[File System (content-output/, components/)\];  
    end

    B \-- (5초마다 상태 체크)\<br/\>GET /api/cycle/status \--\> C;  
    C \-- (파일/상태 읽기) \--\> F;  
    C \-- (현재 상태 응답) \--\> B;

## **3\. 프로젝트 구조 (Project Structure)**

auto-system-contents-generator/  
├── .venv/  
├── assets/                    \# PM 업로드 에셋 (이모지 등)  
│   └── emoji/  
├── components/                \# \[★\] 리치 콘텐츠 컴포넌트 (Jinja2)  
│   ├── NutritionInfo.html  
│   └── WineCard.html  
├── dashboard/                 \# 대쉬보드 UI/UX 코드  
│   ├── static/                \# CSS, JS, EasyMDE 라이브러리  
│   ├── templates/             \# 대쉬보드용 HTML 템플릿 (Flask)  
│   ├── scheduler.py  
│   └── app.py                 \# Python Flask 백엔드  
├── content-output/            \# \[★\] AI 생성 산출물 저장소 (Git 무시)  
│   └── 251112/  
├── guidelines/                \# \[PM 세팅 1\] 가이드라인  
│   ├── style\_guide\_kr.md  
│   └── component\_guide.md     \# \[★\] Shortcode 문법 정의  
├── prompts/                   \# \[PM 세팅 2\] AI 지시 프롬프트 (8개)  
│   └── ... (prompt-1-kr\&en.md 등 8개)  
├── templates/                 \# \[PM 세팅 3\] 콘텐츠 HTML 템플릿  
│   └── blog-post-default.html  
├── specs/                     \# \[★ New\] 본 문서를 포함한 Spec 문서  
│   ├── auto-system-contents-generator\_prd.md  
│   ├── auto-system-contents-generator\_requirements.md  
│   ├── auto-system-contents-generator\_design.md  
│   └── auto-system-contents-generator\_tasks.md  
├── .env                       \# \[PM 세팅 4\] API 키 (Git 무시)  
├── .env.example  
├── requirements.txt  
├── Dockerfile  
├── docker-compose.yml  
├── README.md  
└── run\_pipeline.py            \# 메인 파이프라인 실행 스크립트

## **4\. 데이터 모델 (Data Models)**

### **4.1. manifest.json 스키마**

content-output/YYMMDD/ 폴더에 생성되어, 해당 사이클의 모든 상태와 파일 경로를 관리하는 '두뇌' 파일입니다.

{  
  "cycle\_id": "251112",  
  "createdAt": "2025-11-12T10:30:01Z",  
  "status": {  
    "step": 4,  
    "code": "STEP\_4\_PENDING\_APPROVAL",  
    "text": "Step 4: PM 구조 컨펌 대기중"  
  },  
  "config": {  
    "mode": "specialized",  
    "template": "blog-post-default.html"  
  },  
  "selection": {  
    "selected\_topic": "한국 편의점 꿀조합",  
    "selected\_format": "B",  
    "source\_file": "content-output/251112/step1-research/step1-research-jp.md"  
  },  
  "files": {  
    "step\_1\_research": "content-output/251112/step1-research/step1-research-jp.md",  
    "step\_2\_outline": "content-output/251112/step2-outline/step2-outline.md",  
    "step\_3\_master\_md": null,  
    "step\_3\_master\_html": null,  
    "step\_4\_social\_md": null  
  },  
  "logs": "content-output/251112/pipeline.log"  
}

## **5\. API 엔드포인트 명세 (API Endpoints)**

| Method | Endpoint | 설명 |
| :---- | :---- | :---- |
| GET | /api/cycles | **과거 사이클 목록 조회**. (View 1\) |
| POST | /api/cycle/start | **새 사이클 시작 (Step 1 실행)**. (Modal 1\) |
| GET | /api/cycle/\<cycle\_id\>/status | **사이클 상태/로그 조회**. (View 2\) |
| POST | /api/cycle/\<cycle\_id\>/run/\<step\_id\> | **비동기 AI 작업 실행**. (예: /run/5) |
| POST | /api/cycle/\<cycle\_id\>/approve/\<step\_id\> | **PM 승인**. (예: /approve/4) |
| GET | /api/cycle/\<cycle\_id\>/content | **에디터용 콘텐츠 조회**. (Modal 2\) |
| POST | /api/cycle/\<cycle\_id\>/content | **에디터에서 콘텐츠 저장**. (Modal 2\) |
| GET | /api/schedules | 예약된 작업 목록 조회. (View 1\) |
| POST | /api/schedules/add | 새 예약 작업 추가. (Modal 3\) |
| GET | /api/components | **(New)** Shortcode 컴포넌트 스니펫 목록 조회. |

## **6\. 개발 환경 (Docker)**

* **필수 설치**: **Docker Desktop**.  
* **핵심 파일**: Dockerfile (Python 앱 빌드), docker-compose.yml (Flask+Redis+Celery 서비스 통합 실행).  
* **실행**: docker-compose up \--build.  
* **종료**: docker-compose down.

## **7\. 에러 핸들링 및 비용 방지 설계**

* **(S-1) 멱등성**: POST /api/cycle/run/\<step\_id\> 호출 시, manifest.json의 status를 확인. RUNNING 또는 PENDING 상태일 경우, HTTP 409 Conflict (이미 작업 중)를 반환하여 중복 작업을 방지합니다.  
* **(S-2) 싱글톤 예약**: Step 1 스케줄 작업 실행 시, Redis Lock (예: SET step1\_lock true NX EX 3600)을 시도합니다. 실패 시 (이미 Lock 존재 시), "이전 작업 실행 중, 스킵" 로그를 남기고 종료합니다.  
* **(S-3) 재시도 제한**: 429/503 API 오류 발생 시, **최대 3회** Exponential Backoff 재시도 후 실패 처리합니다.  
* **(S-4) 외부 예산**: Google Cloud, Anthropic 등 모든 API 대시보드에서 \*\*월간/일간 API 사용량 하드 리밋(Hard Limit)\*\*을 설정하는 것을 의무화합니다.  
* **(E-1) 환경 오류**: .env / prompts/ 누락 시, 로그 뷰어에 명확한 한글 메시지 출력.  
* **(E-2) 비동기 오류**: Redis 연결 실패 시 즉시 Toast 알림(🔴 작업 큐 연결 실패). 작업 타임아웃(30분) 시 상태를 '시간 초과'로 변경.  
* **(E-3) 데이터 무결성**: 에디터 '저장' 실패 시, 수정본 유실 방지를 위한 \[클립보드에 복사\] 버튼이 포함된 Toast 알림 제공.  
* **(E-4) 렌더링 오류**: Shortcode JSON 문법 오류 또는 컴포넌트 누락 시, 로그 뷰어에 \[ERROR\] 렌더링 실패: 'WineCard' JSON 파싱 실패 메시지 출력.