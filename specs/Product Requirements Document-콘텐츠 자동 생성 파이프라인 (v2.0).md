# **Product Requirements Document (PRD): 콘텐츠 자동 생성 파이프라인 (v2.0)**

* **문서 버전**: 2.0 (아키텍처 변경: Tailwind/Alpine.js 기반 HTML 스니펫 생성)
* **작성일**: 2025년 11월 14일
* **프로젝트명**: auto-system-contents-generator
* **GitHub**: https://github.com/Kdreammaker/auto-system-contents-generator-for-soolomon
* **핵심 철학 (v2.0)**: AI가 **Tailwind CSS**와 **Alpine.js**를 사용하여, Soolomon Admin의 **Tiptap 에디터**에 바로 붙여넣을 수 있는 **깨끗하고 인터랙티브한 HTML 스니펫**을 생성한다. 로컬 대쉬보드는 이 생성 과정을 관리하고, 최종 운영 환경과 동일한 모습으로 결과물을 미리보는 개발 도구의 역할을 수행한다.

## **1\. 개요**

### **1.1. 문제 정의**

콘텐츠 마케팅은 높은 가치를 지니지만, 고품질의 인터랙티브 콘텐츠를 다국어로 제작하고 배포하는 과정은 시간과 비용이 많이 소모된다. 또한, 생성된 콘텐츠가 최종적으로 사용될 웹사이트(Next.js, Tailwind CSS, Alpine.js 환경)의 디자인 및 기능과 호환되지 않는 문제를 해결해야 한다.

### **1.2. 제안 솔루션**

Perplexity, Google (Gemini), Anthropic (Claude), DeepL 등 검증된 AI API를 통합하여, 최종 운영 환경의 기술 스택(Tailwind CSS, Alpine.js)을 완벽하게 준수하는 **HTML 콘텐츠 스니펫**을 생성하는 엔드-투-엔드(End-to-End) 자동화 파이프라인을 구축한다.

본 시스템은 **localhost에서 실행되는 웹 기반 대쉬보드**를 통해, PM의 전략적 승인 지점을 포함한 전 과정을 그래픽 인터페이스(GUI)로 실행한다.

핵심 아키텍처로, AI는 **Tailwind CSS 클래스**로 스타일링되고 **Alpine.js 속성**으로 인터랙션을 구현한 **깨끗한 HTML 스니펫**을 직접 생성한다. 이 결과물은 별도의 변환 과정 없이 Soolomon Admin의 Tiptap 에디터에 복사-붙여넣기 하여 즉시 사용할 수 있다.

### **1.3. 핵심 목표**

*   **호환성**: 생성된 모든 HTML 스니펫은 `<style>`, `<script>` 태그 없이, 오직 **Tailwind CSS와 Alpine.js만으로** 작성되어 최종 웹사이트 환경과 완벽하게 호환되어야 한다.
*   **고품질 콘텐츠**: 단순 텍스트가 아닌, 탭, 아코디언, 갤러리 등 **인터랙티브 컴포넌트**가 포함된 리치 콘텐츠 생성을 지원한다.
*   **정확한 미리보기**: 로컬 대쉬보드는 `globals.css`와 `Alpine.js`가 적용된 **정확한 미리보기 환경**을 제공하여, AI가 생성한 HTML 스니펫이 최종 발행될 모습과 동일하게 보이도록 보장해야 한다.
*   **통합 환경**: PM은 로컬 대쉬보드 내에서 자료 조사, 구조 검토, 최종 HTML 스니펫 검수 등 모든 작업을 완수(End-to-End)할 수 있어야 한다.
*   **자동화 및 품질**: '인간의 전략적 승인' 지점을 제외한 모든 반복 작업을 비동기(Async)로 자동화하고, AI 검수 피드백을 아카이빙하여 점진적으로 품질을 개선하는 선순환 체계를 구축한다.

## **2\. 시각화 플로우**

### **2.1. 업무 프로세스 순서도 (PM 14단계 워크플로우)**

Step 7의 명칭이 '최종 HTML 생성'으로 변경되었습니다.

graph TD
    subgraph "Phase 1: 기획 및 설계"
        A[1. 자료 조사 (AI)] --> B((<svg width="24" height="24" viewBox="0 0 24 24"><path fill="currentColor" d="M12 4a4 4 0 1 1 0 8a4 4 0 0 1 0-8m0 10c-2.67 0-8 1.34-8 4v2h16v-2c0-2.66-5.33-4-8-4"/></svg><br/><b>2. 주제/포맷 선택 (PM)</b>));
        B --> C[3. 구조 설계 (AI)];
        C --> D((<svg width="24" height="24" viewBox="0 0 24 24"><path fill="currentColor" d="M12 4a4 4 0 1 1 0 8a4 4 0 0 1 0-8m0 10c-2.67 0-8 1.34-8 4v2h16v-2c0-2.66-5.33-4-8-4"/></svg><br/><b>4. 구조 컨펌 (PM)</b>));
    end

    subgraph "Phase 2: 원본 콘텐츠 생성"
        D --> E[5. 풀 콘텐츠 작성 (AI)];
        E --> F[6. 기초 검수 (AI)];
        F --> G[7. <b>최종 HTML 생성 (AI)</b>];
        G --> H((<svg width="24" height="24" viewBox="0 0 24 24"><path fill="currentColor" d="M12 4a4 4 0 1 1 0 8a4 4 0 0 1 0-8m0 10c-2.67 0-8 1.34-8 4v2h16v-2c0-2.66-5.33-4-8-4"/></svg><br/><b>8. 원본 최종 검수 (PM)</b>));
    end

    subgraph "Phase 3: SNS 콘텐츠 생성"
        H --> I[9. SNS 변형 (AI)];
        I --> J[10. SNS 기초 검수 (AI)];
        J --> K((<svg width="24" height="24" viewBox="0 0 24 24"><path fill="currentColor" d="M12 4a4 4 0 1 1 0 8a4 4 0 0 1 0-8m0 10c-2.67 0-8 1.34-8 4v2h16v-2c0-2.66-5.33-4-8-4"/></svg><br/><b>11. SNS 최종 검수 (PM)</b>));
    end

    subgraph "Phase 4: 번역 및 배포"
        K --> L[12. 전체 번역 (AI)];
        L --> M[13. 번역 검수/교정 (AI)];
        M --> N((<svg width="24" height="24" viewBox="0 0 24 24"><path fill="currentColor" d="M12 4a4 4 0 1 1 0 8a4 4 0 0 1 0-8m0 10c-2.67 0-8 1.34-8 4v2h16v-2c0-2.66-5.33-4-8-4"/></svg><br/><b>14. 최종 배포 (PM)</b>));
    end

### **2.2. 프로그램 작동 프로세스 순서도 (기술 아키텍처)**

비동기(Async) 아키텍처를 반영한 최종 기술 순서도입니다.

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
         D -- (7. 파일 쓰기/읽기) --> F[File System (content-output/, prompts/)];
    end

    B -- (5초마다 상태 체크)<br/>GET /api/cycle/status --> C;
    C -- (파일/상태 읽기) --> F;
    C -- (현재 상태 응답) --> B;

## **3\. 전체 프로젝트 구조 (Full Project Structure)**

`components`와 `templates` 폴더가 제거되고, `guidelines`의 역할이 AI 지침으로 명확해졌습니다.

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
│   └── ... (prompt-1-kr&en.md 등 8개)
├── specs/                     # [★] 본 문서를 포함한 Spec 문서
│   ├── ...
├── .env                       # [PM 세팅 3] API 키 (Git 무시)
├── .env.example
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
├── README.md
└── run_pipeline.py            # 메인 파이프라인 실행 스크립트

### **3.1. 산출물 폴더 구조 (content-output/YYMMDD/)**

`final-content.html`이 최종 산출물이 됩니다.

content-output/
└── 251114/                    # [기준일] 폴더
    ├── manifest.json          # [★] 이 사이클의 두뇌 (상태, 설정, 파일 경로)
    ├── pipeline.log           # 이 사이클의 상세 로그 파일
    ├── selection.json         # [Human 1] PM이 선택한 주제/포맷 정의
    ├── step1-research/
    │   └── step1-research-jp.md
    ├── step2-outline/
    │   └── step2-outline.md   # [Human 2] PM이 컨펌/수정한 아웃라인
    ├── step3-content/
    │   ├── step3-content-raw.md
    │   ├── step3-revised-w.feedback.md
    │   └── step3-revised-final.md     # [★] AI가 생성/검수한 최종 마크다운 원본
    ├── step4-html/
    │   └── final-content.html       # [★] 최종 산출물: Tailwind/Alpine.js가 적용된 HTML 스니펫
    ├── step5-social/
    │   └── ...
    └── ...

## **4\. 14-Step Workflow (확정)**

*
  1. 자료 조사 (AI)
*
  2. **[Human 1] 주제 및 포맷 선택**
*
  3. 콘텐츠 구조 설계 (AI)
*
  4. **[Human 2] 구조 컨펌**
*
  5. **풀 콘텐츠 작성 (AI)**: Prompt 3를 참조하여, 표준 마크다운으로 `step3-content-raw.md`를 생성합니다.
*
  6. **기초 검수 (AI)**: (예: Claude API) AI가 `step3-content-raw.md`의 표현, 문법을 1차 검수하여 `step3-revised-final.md`를 생성합니다.
*
  7. **최종 HTML 생성 (AI)**: (New Logic)
  * 강력한 AI(예: Claude 3 Opus)가 `step3-revised-final.md`와 `AI_CONTENT_GENERATOR_GUIDE.md`를 함께 입력받습니다.
  * AI는 가이드라인의 규칙(Tailwind, Alpine.js, 컴포넌트 구조 등)을 완벽하게 준수하여 최종 `final-content.html` 스니펫을 생성합니다.
*
  8. **[Human 3] 원본 최종 검수**: PM이 대쉬보드의 **"HTML 프리뷰" 탭**에서 최종 렌더링된 `final-content.html`을 검토 후 승인합니다.
*
  9. SNS 형태로 변형 (AI)
*
  10. SNS 기초 검수 (AI)
*
  11. **[Human 4] SNS 최종 검수**
*
  12. 전체 번역 (AI) (DeepL API)
*
  13. 번역 검수 및 교정 (AI) (예: Claude API)
*
  14. **[Human 5] 배포**: PM이 최종 산출물(HTML 스니펫, SNS본, 번역본)을 각 플랫폼에 배포.

## **5\. 대쉬보드 UI/UX 상세 기획 (localhost)**

### **5.1. 핵심 화면 (Views)**

* **View 1: 메인 페이지 (/) \- 사이클 런처 및 스케줄러**
  * **기능**: 새 콘텐츠 생성 사이클을 시작, 예약, 또는 과거 사이클을 조회합니다.
  * **컴포넌트**: "새 사이클 즉시 시작" 버튼 (Modal 1 호출), "과거 사이클 목록" (View 2로 이동), "예약 작업 관리" (Modal 3 호출)
* **View 2: 사이클 대쉬보드 (/cycle/<YYMMDD>) \- 메인 워크스페이스**
  * **기능**: 14단계 워크플로우를 실행하고, 승인하고, 모니터링합니다.
  * **컴포넌트**: 워크플로우 영역 (14단계 상태 시각화), 로그 뷰어.
  * **UI 가이드**: 대쉬보드 자체의 UI는 빠른 개발을 위해 **Bootstrap 5**와 **Remix Icon**을 사용합니다. (이는 최종 결과물과 무관합니다)

### **5.2. 핵심 모달 (Modals / Pop-ups)**

* **Modal 1: 새 사이클 생성 (View 1에서 호출)**
  * **기능**: Prompt 1 (자료 조사) 실행을 위한 파라미터를 설정합니다.
  * **컴포넌트**: "전략 모드 선택" (Standard/Specialized), "실행" 버튼
* **Modal 2: 산출물 뷰어 & 검수 (View 2에서 호출)**
  * **기능**: 단계별 마크다운 초안을 확인하거나, 최종 생성된 HTML 스니펫을 검수합니다.
  * **컴포넌트**:
    * **뷰어 탭**: "Markdown" (EasyMDE 에디터, Step 2, 4, 6 검수용), **"HTML 최종 프리뷰"** (iframe, Step 8 검수용)
    * **HTML 최종 프리뷰**: `globals.css`와 `Alpine.js`가 적용되어 최종 운영 환경과 100% 동일한 모습으로 `final-content.html`을 렌더링합니다.
    * "저장" 버튼, "승인 (Approve)" 버튼
* **Modal 3: 새 예약 추가 (View 1에서 호출)**
  * **기능**: Step 1 작업의 예약 및 반복을 설정합니다.
  * **컴포넌트**: "실행 시간 설정" (Cron UI), "전략 모드 선택", "저장" 버튼
* **Modal 4: 에셋 삽입 (Modal 2에서 호출)**
  * **기능**: assets/emoji/ 폴더의 스티커를 마크다운 에디터에 삽입합니다.
  * **컴포넌트**: 이미지/GIF 목록. 클릭 시 에디터에 `![file-name](/assets/emoji/file-name.png)` 텍스트 삽입.

## **6\. 핵심 기능 요구사항 (Functional Requirements)**

* **EPIC 0: 대쉬보드 (Dashboard)**
  * **USR-0.1 (워크플로우 실행)**: PM은 대쉬보드의 버튼 클릭으로 14단계 파이프라인을 단계별로 트리거해야 한다.
  * **USR-0.2 (워크플로우 상태)**: 대쉬보드는 14단계의 상태를 실시간으로 시각화해야 한다.
  * **USR-0.3 (산출물 조회/수정)**: PM은 대쉬보드 내에서 단계별 .md 산출물을 EasyMDE 에디터로 조회, 수정, 저장할 수 있어야 한다.
  * **USR-0.4 (워크플로우 승인)**: PM은 **[Human 2, 4, 8, 11]** 단계에서 "승인" 버튼을 눌러야만 다음 단계가 활성화된다.
  * **USR-0.5 (사이클 생성)**: PM은 대쉬보드에서 '전략 모드'를 선택하여 새 콘텐츠 생성 사이클을 시작할 수 있어야 한다.
  * **USR-0.6 (예약 실행)**: PM은 대쉬보드에서 Step 1 작업의 반복 실행을 예약할 수 있어야 한다.
  * **USR-0.7 (에셋 삽입)**: PM은 Markdown 에디터에서 assets/emoji/ 폴더의 이미지/GIF를 클릭 한 번으로 본문에 삽입할 수 있어야 한다.
  * **USR-0.8 (HTML 프리뷰)**: PM은 Step 8 (원본 검수) 단계에서, **`globals.css`와 `Alpine.js`가 완벽하게 적용된 최종 HTML 프리뷰**를 확인할 수 있어야 한다.
  * **USR-0.9 (UI 일관성)**: 대쉬보드 자체의 UI는 **Bootstrap 5**와 **Remix Icon**을 사용한다. 이는 최종 생성물과 무관하다.
* **EPIC 1: 백엔드 로직 (Backend Logic)**
  * **USR-1.1 (모델 유연성)**: .env 파일로 모델명 교체.
  * **USR-1.2 (인간 승인 대기)**: 백엔드 파이프라인은 인간 승인 지점에서 명확히 '일시 중지(Pause)'되어야 한다.
  * **USR-1.3 (워크플로우 분기)**: 'Standard' 또는 'Specialized' 모드에 따라 올바른 프롬프트 세트 로드.
  * **USR-1.4 (HTML 생성)**: Step 7은 AI를 통해, `step3-revised-final.md` 마크다운 원본과 `AI_CONTENT_GENERATOR_GUIDE.md` 규칙을 참조하여, **Tailwind와 Alpine.js를 사용한 최종 HTML 스니펫**을 생성해야 한다.
  * **USR-1.5 (피드백 파일 생성)**: 모든 AI 검수 단계(6, 10, 13)는 `*-w.feedback.md` 파일을 반드시 생성.
* **EPIC 2: 에러 핸들링 및 안정성 (Reliability & Safety)**
  * **USR-2.1 (멱등성)**: 작업 중복 실행을 방지해야 한다.
  * **USR-2.2 (싱글톤 예약)**: 예약 작업 중복 실행을 방지해야 한다.
  * **USR-2.3 (재시도 제한)**: API 오류 시 최대 3회 재시도 후 실패 처리해야 한다.
  * **USR-2.4 (외부 예산)**: PM(개발자)은 모든 외부 API에 예산 하드 리밋을 설정해야 한다.
  * **USR-2.5 (에러 로깅)**: 모든 실패는 로그 뷰어에 명확한 한글 에러 메시지를 표시해야 한다.
  * **USR-2.6 (데이터 무결성)**: 에디터 저장 실패 시, 수정본 유실을 방지해야 한다.

## **7\. 기술 사양 (Technical Specifications)**

### **7.1. 프로그래밍 언어 및 프레임워크**

* **백엔드 (Backend)**: **Python 3.10+**, **Flask**
* **프론트엔드 (Frontend)**: **Vanilla JavaScript (ES6+)**, **HTML5**, **CSS3**
* **선정 이유**: React/Vue의 복잡성 없이, Flask(백엔드)가 렌더링한 HTML을 Vanilla JS(프론트엔드)가 보조하는 방식이 로컬 대쉬보드 목적에 가장 빠르고 효율적입니다.

### **7.2. 주요 Python 의존성 (Backend)**

* **웹 서버/비동기**: flask, celery, redis
* **AI API 클라이언트**: google-generativeai, anthropic, deepl, perplexity-api
* **유틸리티**: python-dotenv, PyYAML, APScheduler

### **7.3. 프론트엔드 기술 스택 구분**

*   **대쉬보드 UI용**:
    *   **CSS 프레임워크**: **Bootstrap 5** (CDN)
    *   **아이콘**: **Remix Icon** (CDN)
    *   **폰트**: **Google Fonts** (CDN)
    *   **선정 이유**: 대쉬보드 자체의 UI를 신속하게 개발하기 위함.
*   **콘텐츠 결과물용**:
    *   **CSS**: **Tailwind CSS** (제공된 `globals.css` 파일)
    *   **JS**: **Alpine.js** (CDN)
    *   **선정 이유**: 최종 운영 환경과의 100% 호환성 보장.

### **7.4. 콘텐츠 에디터 (Markdown Editor)**

* **라이브러리**: **EasyMDE**
* **선정 이유**: 마크다운 초안(Step 2, 4, 6)을 편집하는 데 사용. 가볍고 툴바 커스터마이징이 용이.

## **8\. 데이터 스키마 (Data Schemas)**

### **8.1. manifest.json 스키마**

content-output/YYMMDD/ 폴더에 생성되어, 해당 사이클의 모든 상태와 파일 경로를 관리하는 '두뇌' 파일입니다.

{
  "cycle_id": "251112",
  "createdAt": "2025-11-12T10:30:01Z",
  "status": {
    "step": 4,
    "code": "STEP_4_PENDING_APPROVAL",
    "text": "Step 4: PM 구조 컨펌 대기중"
  },
  "config": {
    "mode": "specialized",
    "template": "blog-post-default.html"
  },
  "selection": {
    "selected_topic": "한국 편의점 꿀조합",
    "selected_format": "B",
    "source_file": "content-output/251112/step1-research/step1-research-jp.md"
  },
  "files": {
    "step_1_research": "content-output/251112/step1-research/step1-research-jp.md",
    "step_2_outline": "content-output/251112/step2-outline/step2-outline.md",
    "step_3_master_md": null,
    "step_3_master_html": null,
    "step_4_social_md": null
  },
  "logs": "content-output/251112/pipeline.log"
}

## **9\. API 엔드포인트 명세 (API Endpoint Specifications)**

프론트엔드(Vanilla JS)와 백엔드(Flask)가 통신하기 위한 API 명세입니다.

| Method | Endpoint | 설명 |
| :---- | :---- | :---- |
| GET | /api/cycles | **과거 사이클 목록 조회**. (View 1) |
| POST | /api/cycle/start | **새 사이클 시작 (Step 1 실행)**. (Modal 1) |
| GET | /api/cycle/<cycle_id>/status | **사이클 상태/로그 조회**. (View 2) |
| POST | /api/cycle/<cycle_id>/run/<step_id> | **비동기 AI 작업 실행**. (예: /run/5) |
| POST | /api/cycle/<cycle_id>/approve/<step_id> | **PM 승인**. (예: /approve/4) |
| GET | /api/cycle/<cycle_id>/content | **에디터용 콘텐츠 조회**. (Modal 2) |
| POST | /api/cycle/<cycle_id>/content | **에디터에서 콘텐츠 저장**. (Modal 2) |
| GET | /api/schedules | 예약된 작업 목록 조회. (View 1) |
| POST | /api/schedules/add | 새 예약 작업 추가. (Modal 3) |
| GET | /api/components | **(제거됨)** |

## **10\. 비동기 작업 아키텍처 (Async Task Architecture)**

긴 AI 작업을 처리하기 위해 Task Queue 아키텍처를 도입합니다.

1. **구성 요소**: **Flask (웹 서버)**, **Redis (메시지 브로커)**, **Celery (Task Worker)**.
2. **작동 방식 (2.2 순서도 참조)**:
   * PM이 [Step 5 실행] 버튼을 클릭합니다.
   * Flask는 HTTP 202 (Accepted)를 0.1초 만에 즉시 응답하고, Celery에게 "Step 5 작업해줘"라는 메시지를 Redis를 통해 전달합니다.
   * 별도 프로세스(컨테이너)인 Celery Worker가 이 메시지를 받아, 백그라운드에서 1분 동안 run_pipeline.py의 Step 5 로직을 실행합니다.
   * PM의 대쉬보드는 5초마다 GET /api/cycle/status를 호출하여 "Step 5: 진행중..." -> "Step 6: 완료"로 바뀌는 상태를 표시합니다.

## **11\. 개발 환경 구축 가이드 (Docker)**

PM님(개발자)께서 이 시스템을 실행하기 위한 Docker 환경 설정 가이드입니다.

### **11.1. 1단계: Docker Desktop 설치**

* docker.com/products/docker-desktop/에서 본인의 OS(Windows/Mac)에 맞는 **Docker Desktop**을 다운로드하여 설치합니다.

### **11.2. 2단계: 프로젝트 루트 폴더에 파일 2개 생성**

프로젝트 루트(auto-system-contents-generator/)에 다음 Dockerfile과 docker-compose.yml 파일을 생성합니다.

**Dockerfile** (Python/Flask/Celery 앱 빌드 설계도)

# 1. Python 3.10을 기본 이미지로 사용
FROM python:3.10-slim

# 2. 작업 디렉토리 설정
WORKDIR /app

# 3. 의존성 파일 복사 및 설치
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# 4. 전체 프로젝트 소스 코드 복사
COPY . .

# 5. Flask 앱 실행 포트 노출 (3001번)
EXPOSE 3001

# 6. 기본 실행 명령어 (Flask 서버)
CMD ["flask", "--app", "dashboard.app", "run", "--host=0.0.0.0", "--port=3001"]

**docker-compose.yml** (전체 서비스(Flask+Redis+Celery) 실행기)

version: '3.8'

services:
  # 1. Redis (메시지 브로커)
  redis:
    image: "redis:alpine"
    ports:
      - "6379:6379"

  # 2. Web (Flask 백엔드 및 대쉬보드)
  web:
    build: .
    command: flask --app dashboard.app run --host=0.0.0.0 --port=3001
    volumes:
      - .:/app  # [★] 로컬 폴더와 컨테이너 내부를 동기화
    ports:
      - "3001:3001"
    env_file:
      - .env    # .env 파일의 API 키를 컨테이너로 전달
    depends_on:
      - redis

  # 3. Worker (Celery 비동기 작업자)
  worker:
    build: .
    command: celery -A dashboard.app.celery worker --loglevel=info
    volumes:
      - .:/app  # [★] 로컬 폴더와 컨테이너 내부를 동기화
    env_file:
      - .env
    depends_on:
      - redis

### **11.3. 3단계: 시스템 실행 및 종료**

* **시스템 실행 (빌드 포함)**:
  * (터미널에서 auto-system-contents-generator/ 폴더로 이동)
  * docker-compose up --build
  * (최초 1회 빌드 후, 다음부터는 docker-compose up만 입력)
* **시스템 종료**:
  * (터미널에서 Ctrl+C를 누른 후)
  * docker-compose down

## **12\. 실패 및 오류 케이스 (Error Handling & Scenarios)**

* **1\. 환경 및 설정 오류**: .env, prompts/ 파일 누락 등.
* **2\. 외부 API 오류**: 4xx/5xx API 에러, 자동 재시도.
* **3\. 파이프라인 및 데이터 오류**: 파일 I/O 오류, AI의 빈 응답.
* **4\. 비동기 작업 및 스케줄러 오류**: Redis 연결 실패, 작업 타임아웃.
* **5\. 사용자 경험(UX) 및 데이터 무결성 오류**: 에디터 저장 실패.
* **6\. HTML 생성 오류 (HTML Generation Errors)**
  * **케이스 (1) \- 규칙 위반**: AI가 Step 7에서 `AI_CONTENT_GENERATOR_GUIDE.md`의 규칙을 위반한 HTML을 생성 (예: `<style>` 태그 사용, 금지된 속성 사용).
  * **대응 (1)**: Step 8의 PM 검수 단계에서 시각적으로 오류가 확인됨. 필요시, 백엔드에서 간단한 정규식으로 명백한 위반(예: `<script>` 태그)을 감지하고 로그에 \[WARNING\]을 남길 수 있음.
  * **케이스 (2) \- 스타일 깨짐**: AI가 존재하지 않는 Tailwind 클래스를 사용하거나, Alpine.js 문법 오류를 포함하여 HTML 프리뷰가 깨져 보임.
  * **대응 (2)**: Step 8의 PM이 "HTML 최종 프리뷰" 탭에서 시각적으로 문제를 인지하고 해당 단계를 '재실행'하거나, 이전 단계의 마크다운을 수정하여 재시도.

## **13\. 향후 로드맵 (v2.0)**

* **v2.0 (현재)**: 안정성 우선. PM이 모든 Human Checkpoint에서 명시적 승인.
* **v2.1 (미래)**: v2.0 운영을 통해 AI의 HTML 생성 품질이 안정적이라고 판단되면, 특정 컴포넌트(예: Callout) 생성 규칙 위반을 자동으로 감지하고 수정하는 '자동 교정' 단계를 추가하는 것을 검토.
