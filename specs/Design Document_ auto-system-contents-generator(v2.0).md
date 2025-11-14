# **Design Document: auto-system-contents-generator (v2.0)**

* **문서 버전**: 2.0 (아키텍처 변경: Tailwind/Alpine.js 기반 HTML 스니펫 생성)
* **작성일**: 2025년 11월 14일

## **1\. Overview**

이 문서는 auto-system-contents-generator의 기술 아키텍처, 데이터 모델, API 명세 및 개발 환경을 정의합니다. 본 설계의 핵심은 **'AI 직접 HTML 생성'** 아키텍처와, 긴 AI 작업을 처리하기 위한 **'비동기 Task Queue'**, 그리고 API 비용 폭증을 방지하기 위한 **'안전장치(Safeguards)'** 입니다.

## **2\. Architecture (아키텍처)**

### **2.1. 기술 스택 (Technology Stack)**

*   **백엔드 (Backend)**: Python 3.10+, Flask
*   **프론트엔드 (Frontend)**: Vanilla JavaScript (ES6+), HTML5, CSS3
*   **비동기 (Async)**: Celery, Redis
*   **대쉬보드 UI (Dashboard UI)**:
    *   CSS 프레임워크: **Bootstrap 5** (CDN)
    *   아이콘: **Remix Icon** (CDN)
    *   폰트: **Google Fonts** (CDN)
    *   에디터: **EasyMDE**
*   **콘텐츠 결과물 (Content Output)**:
    *   CSS: **Tailwind CSS** (제공된 `globals.css` 사용)
    *   JS: **Alpine.js** (CDN)
*   **실행 환경**: **Docker Compose**

### **2.2. 핵심 설계: AI 직접 HTML 생성**

Soolomon Admin의 Tiptap 에디터와 호환되는 리치 콘텐츠를 위해, AI는 최종 HTML 스니펫을 직접 생성합니다.

*   **Step 6: AI 생성물 (Markdown)**:
    *   `step3-revised-final.md`
    *   표준 마크다운 문법으로 작성된 순수 텍스트 콘텐츠

*   **Step 7: AI 입력 (Markdown + 가이드라인)**:
    1.  `step3-revised-final.md` (콘텐츠)
    2.  `specs/AI_CONTENT_GENERATOR_GUIDE.md` (규칙)

*   **Step 7: AI 최종 생성물 (HTML Snippet)**:
    *   `final-content.html`
    *   `AI_CONTENT_GENERATOR_GUIDE.md`의 규칙을 완벽하게 준수하는, Tailwind와 Alpine.js로 구성된 깨끗한 HTML 코드

    ```html
    <!-- 예시: AI 최종 생성물 -->
    <div x-data="{ open: false }" class="border rounded-lg">
      <button x-on:click="open = !open" class="w-full flex ...">
        <span class="font-semibold">질문 1: 맥주와 치킨이 잘 어울리는 이유는?</span>
        <svg :class="{ 'rotate-180': open }" ...></svg>
      </button>
      <div x-show="open" x-collapse class="p-4 border-t">
        <p>맥주의 탄산과 쓴맛이 치킨의 기름기를 중화시켜주기 때문입니다.</p>
      </div>
    </div>
    ```

### **2.3. 비동기 아키텍처 다이어그램**

graph TD
    A[PM (사용자)] <-- (상호작용) --> B[<b>대쉬보드 (Web UI @ localhost)</b>];
      
    subgraph "로컬 서버 환경 (Docker Compose)"
        B -- (1. API 요청)<br/>POST /api/cycle/run/5 --> C[Web Server (Flask)];
        C -- (2. 0.1초 내 즉시 응답)<br/>HTTP 202 Accepted --> B;
        C -- (3. 작업 전달) --> R[Task Queue (Redis)];
        W[Celery Worker (별도 컨테이너)] -- (4. 작업 수신) --> R;
        W -- (5. 파이프라인 실행) --> D[Python Pipeline Core (run_pipeline.py)];
    end

    subgraph "외부 API"
        D -- (6. AI API 호출) --> E[External APIs (Google, Claude, DeepL)];
    end

    subgraph "로컬 파일 시스템"
         D -- (7. 파일 쓰기/읽기) --> F[File System (content-output/, prompts/, specs/)];
    end

    B -- (5초마다 상태 체크)<br/>GET /api/cycle/status --> C;
    C -- (파일/상태 읽기) --> F;
    C -- (현재 상태 응답) --> B;

## **3\. 프로젝트 구조 (Project Structure)**

auto-system-contents-generator/
├── .venv/
├── assets/                    # PM 업로드 에셋 (이모지 등)
│   └── emoji/
├── dashboard/                 # 대쉬보드 UI/UX 코드
│   ├── static/                # CSS, JS 라이브러리
│   ├── templates/             # 대쉬보드용 HTML 템플릿 (Flask)
│   ├── scheduler.py
│   └── app.py                 # Python Flask 백엔드
├── content-output/            # [★] AI 생성 산출물 저장소 (Git 무시)
│   └── 251114/
├── guidelines/                # [PM 세팅 1] AI 콘텐츠 생성 가이드라인
│   └── style_guide_kr.md
├── prompts/                   # [PM 세팅 2] AI 지시 프롬프트 (8개)
│   └── ...
├── specs/                     # [★] 본 문서를 포함한 Spec 문서
│   └── ...
├── .env                       # [PM 세팅 3] API 키 (Git 무시)
├── .env.example
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
├── README.md
└── run_pipeline.py            # 메인 파이프라인 실행 스크립트

## **4\. 데이터 모델 (Data Models)**

### **4.1. manifest.json 스키마**

`final_html_path`가 추가됩니다.

{
  "cycle_id": "251114",
  "createdAt": "2025-11-14T10:30:01Z",
  "status": {
    "step": 7,
    "code": "STEP_7_PENDING",
    "text": "Step 7: 최종 HTML 생성 대기중"
  },
  "config": {
    "mode": "specialized"
  },
  "selection": {
    "selected_topic": "한국 편의점 꿀조합",
    "selected_format": "B",
    "source_file": "content-output/251114/step1-research/step1-research-jp.md"
  },
  "files": {
    "step_1_research": "content-output/251114/step1-research/step1-research-jp.md",
    "step_2_outline": "content-output/251114/step2-outline/step2-outline.md",
    "step_3_master_md": "content-output/251114/step3-content/step3-revised-final.md",
    "final_html_path": "content-output/251114/step4-html/final-content.html",
    "step_5_social_md": null
  },
  "logs": "content-output/251114/pipeline.log"
}

## **5\. API 엔드포인트 명세 (API Endpoints)**

| Method | Endpoint | 설명 |
| :---- | :---- | :---- |
| GET | /api/cycles | **과거 사이클 목록 조회**. (View 1) |
| POST | /api/cycle/start | **새 사이클 시작 (Step 1 실행)**. (Modal 1) |
| GET | /api/cycle/<cycle_id>/status | **사이클 상태/로그 조회**. (View 2) |
| POST | /api/cycle/<cycle_id>/run/<step_id> | **비동기 AI 작업 실행**. (예: /run/7) |
| POST | /api/cycle/<cycle_id>/approve/<step_id> | **PM 승인**. (예: /approve/8) |
| GET | /api/cycle/<cycle_id>/content | **에디터용 콘텐츠 조회**. (Modal 2) |
| POST | /api/cycle/<cycle_id>/content | **에디터에서 콘텐츠 저장**. (Modal 2) |
| GET | /api/schedules | 예약된 작업 목록 조회. (View 1) |
| POST | /api/schedules/add | 새 예약 작업 추가. (Modal 3) |

## **6\. 개발 환경 (Docker)**

* **필수 설치**: **Docker Desktop**.
* **핵심 파일**: Dockerfile (Python 앱 빌드), docker-compose.yml (Flask+Redis+Celery 서비스 통합 실행).
* **실행**: `docker-compose up --build`.
* **종료**: `docker-compose down`.

## **7\. 에러 핸들링 및 비용 방지 설계**

* **(S-1) 멱등성**: POST /api/cycle/run/<step_id> 호출 시, manifest.json의 status를 확인. RUNNING 또는 PENDING 상태일 경우, HTTP 409 Conflict (이미 작업 중)를 반환하여 중복 작업을 방지합니다.
* **(S-2) 싱글톤 예약**: Step 1 스케줄 작업 실행 시, Redis Lock을 사용하여 이전 작업이 실행 중이면 스킵합니다.
* **(S-3) 재시도 제한**: 429/503 API 오류 발생 시, **최대 3회** Exponential Backoff 재시도 후 실패 처리합니다.
* **(S-4) 외부 예산**: 모든 외부 API 대시보드에서 **월간/일간 API 사용량 하드 리밋(Hard Limit)**을 설정하는 것을 의무화합니다.
* **(E-1) 환경 오류**: .env / prompts/ 누락 시, 로그 뷰어에 명확한 한글 메시지 출력.
* **(E-2) 비동기 오류**: Redis 연결 실패 시 즉시 Toast 알림. 작업 타임아웃(30분) 시 상태를 '시간 초과'로 변경.
* **(E-3) 데이터 무결성**: 에디터 '저장' 실패 시, 수정본 유실 방지를 위한 [클립보드에 복사] 버튼이 포함된 Toast 알림 제공.
* **(E-4) HTML 생성 오류**: AI가 Step 7에서 가이드라인을 위반하는 HTML(예: `<script>` 태그)을 생성하면, 로그 뷰어에 `[WARNING] AI가 생성한 HTML에 잠재적 규칙 위반이 감지되었습니다.`라고 표시할 수 있습니다. (선택 사항)
