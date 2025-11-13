# **Product Requirements Document (PRD): 콘텐츠 자동 생성 파이프라인 (v1.9)**

* **문서 버전**: 1.9 (개발 착수용 최종 기술 명세서 / UI 스택 확정)  
* **작성일**: 2025년 11월 12일  
* **프로젝트명**: auto-system-contents-generator  
* **GitHub**: https://github.com/Kdreammaker/auto-system-contents-generator-for-soolomon  
* **핵심 철학 (v1.9)**: 확정된 14단계 워크플로우를, Docker Compose 기반의 Python/Flask/Celery/Vanilla JS 기술 스택과 Bootstrap 5/Remix Icon/Google Fonts UI 킷을 사용하여 localhost:3000 웹 대쉬보드를 통해 비동기식으로 실행, 검수, 관리한다.

## **1\. 개요**

### **1.1. 문제 정의**

콘텐츠 마케팅은 높은 가치를 지니지만, 고품질의 원본 콘텐츠를 다국어로 제작하고 배포하는 과정은 시간과 비용이 많이 소모되며 확장성이 떨어진다. 단순 Markdown(.md) 콘텐츠는 리치 컴포넌트(탭, 카드, 배너) 등 복잡한 UI를 구현할 수 없다.

### **1.2. 제안 솔루션**

Perplexity, Google (Gemini), Anthropic (Claude), DeepL 등 검증된 AI API를 통합하는 엔드-투-엔드(End-to-End) 자동화 파이프라인을 구축한다.

본 시스템은 **localhost:3000에서 실행되는 웹 기반 대쉬보드**를 통해, PM의 전략적 승인(컨펌) 지점을 포함한 14단계의 전 과정을 그래픽 인터페이스(GUI)로 실행한다.

핵심 아키텍처로, AI는 일반 Markdown과 **커스텀 단축코드(Shortcode)** (예: \[WineCard: {...}\], \[PremiumBanner\])가 혼합된 \*\*'확장 마크다운'\*\*을 생성한다. Step 7: 리치 콘텐츠 렌더링 단계에서 시스템은 이 단축코드를 components/ 폴더에 미리 정의된 리치 HTML/CSS 컴포넌트로 자동 치환하여 최종 페이지를 생성한다.

### **1.3. 핵심 목표**

* **통합 환경**: PM은 localhost:3000 대쉬보드 내에서 자료 조사, 주제 선택, 구조 검토, 최종본 검수 등 모든 작업을 완수(End-to-End)할 수 있어야 한다.  
* **고품질 콘텐츠**: 단순 텍스트가 아닌, 리치 컴포넌트(탭, 카드, 배너)가 포함된 인터랙티브 콘텐츠 생성을 지원한다.  
* **자동화**: 대쉬보드의 '다음 단계 실행' 버튼 클릭을 통해, '인간의 전략적 승인' 지점을 제외한 모든 반복 작업을 백그라운드에서 비동기(Async)로 자동화한다.  
* **품질**: '교정 피드백' 및 '번역 검수 피드백'을 \*-w.feedback.md 파일로 자동 생성 및 아카이빙하여, 이를 분기별로 분석하고 prompts/ 및 guidelines/를 업데이트하는 선순환 품질 관리 체계를 구축한다.  
* **유연성**: .env 파일에서 각 단계별(Step) API 모델을 손쉽게 교체할 수 있도록 설계하여, 비용과 품질 간의 A/B 테스트 및 유연한 운영을 보장한다.

## **2\. 시각화 플로우**

### **2.1. 업무 프로세스 순서도 (PM 14단계 워크플로우)**

Step 7의 명칭이 '리치 콘텐츠 렌더링'으로 변경되어 아키텍처의 핵심을 반영합니다.

graph TD  
    subgraph "Phase 1: 기획 및 설계"  
        A\[1. 자료 조사 (AI)\] \--\> B((\<svg width="24" height="24" viewBox="0 0 24 24"\>\<path fill="currentColor" d="M12 4a4 4 0 1 1 0 8a4 4 0 0 1 0-8m0 10c-2.67 0-8 1.34-8 4v2h16v-2c0-2.66-5.33-4-8-4"/\>\</svg\>\<br/\>\<b\>2. 주제/포맷 선택 (PM)\</b\>));  
        B \--\> C\[3. 구조 설계 (AI)\];  
        C \--\> D((\<svg width="24" height="24" viewBox="0 0 24 24"\>\<path fill="currentColor" d="M12 4a4 4 0 1 1 0 8a4 4 0 0 1 0-8m0 10c-2.67 0-8 1.34-8 4v2h16v-2c0-2.66-5.33-4-8-4"/\>\</svg\>\<br/\>\<b\>4. 구조 컨펌 (PM)\</b\>));  
    end

    subgraph "Phase 2: 원본 콘텐츠 생성"  
        D \--\> E\[5. 풀 콘텐츠 작성 (AI)\];  
        E \--\> F\[6. 기초 검수 (AI)\];  
        F \--\> G\[7. \<b\>리치 콘텐츠 렌더링 (AI)\</b\>\];  
        G \--\> H((\<svg width="24" height="24" viewBox="0 0 24 24"\>\<path fill="currentColor" d="M12 4a4 4 0 1 1 0 8a4 4 0 0 1 0-8m0 10c-2.67 0-8 1.34-8 4v2h16v-2c0-2.66-5.33-4-8-4"/\>\</svg\>\<br/\>\<b\>8. 원본 최종 검수 (PM)\</b\>));  
    end

    subgraph "Phase 3: SNS 콘텐츠 생성"  
        H \--\> I\[9. SNS 변형 (AI)\];  
        I \--\> J\[10. SNS 기초 검수 (AI)\];  
        J \--\> K((\<svg width="24" height="24" viewBox="0 0 24 24"\>\<path fill="currentColor" d="M12 4a4 4 0 1 1 0 8a4 4 0 0 1 0-8m0 10c-2.67 0-8 1.34-8 4v2h16v-2c0-2.66-5.33-4-8-4"/\>\</svg\>\<br/\>\<b\>11. SNS 최종 검수 (PM)\</b\>));  
    end

    subgraph "Phase 4: 번역 및 배포"  
        K \--\> L\[12. 전체 번역 (AI)\];  
        L \--\> M\[13. 번역 검수/교정 (AI)\];  
        M \--\> N((\<svg width="24" height="24" viewBox="0 0 24 24"\>\<path fill="currentColor" d="M12 4a4 4 0 1 1 0 8a4 4 0 0 1 0-8m0 10c-2.67 0-8 1.34-8 4v2h16v-2c0-2.66-5.33-4-8-4"/\>\</svg\>\<br/\>\<b\>14. 최종 배포 (PM)\</b\>));  
    end

### **2.2. 프로그램 작동 프로세스 순서도 (기술 아키텍처)**

비동기(Async) 아키텍처를 반영한 최종 기술 순서도입니다.

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

## **3\. 전체 프로젝트 구조 (Full Project Structure)**

components/ 및 specs/ 폴더가 신설되었습니다.

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
│   ├── auto-system-contents-generator\_prd.md (본 파일)  
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

### **3.1. 산출물 폴더 구조 (content-output/YYMMDD/)**

manifest.json이 이 사이클의 모든 상태와 파일 경로를 관리합니다.

content-output/  
└── 251112/                    \# \[기준일\] 폴더  
    ├── manifest.json          \# \[★\] 이 사이클의 두뇌 (상태, 설정, 파일 경로)  
    ├── pipeline.log           \# 이 사이클의 상세 로그 파일  
    ├── selection.json         \# \[Human 1\] PM이 선택한 주제/포맷 정의  
    ├── step1-research/  
    │   └── step1-research-jp.md  
    ├── step2-outline/  
    │   └── step2-outline.md   \# \[Human 2\] PM이 컨펌/수정한 아웃라인  
    ├── step3-content/  
    │   ├── step3-content-raw.md  
    │   ├── step3-revised-w.feedback.md  
    │   ├── step3-revised-final.md     \# \[★\] AI가 생성한 '확장 마크다운' (Shortcode 포함)  
    │   └── step3-revised-final.html   \# \[★\] '확장 마크다운'이 렌더링된 최종 HTML  
    ├── step4-social/  
    │   ├── step4-social-raw.md  
    │   ├── step4-social-w.feedback.md  
    │   └── step4-social-final.md      \# \[Human 4\] PM이 최종 승인한 SNS 원본  
    ├── step5-translation/  
    │   ├── step3-revised-final-en.md  
    │   └── step4-social-final-en.md  
    └── step6-qc/  
        ├── step3-translated-revised-w.feedback-en.md  
        └── step3-translated-revised-final-en.md \# \[Human 5\] 배포 대기 최종본

## **4\. 14-Step Workflow (확정)**

*   
  1. 자료 조사 (AI)  
*   
  2. **\[Human 1\] 주제 및 포맷 선택**  
*   
  3. 콘텐츠 구조 설계 (AI)  
*   
  4. **\[Human 2\] 구조 컨펌**  
*   
  5. 풀 콘텐츠 작성 (AI): Prompt 3와 guidelines/component\_guide.md를 참조하여, \*\*'확장 마크다운(Shortcode)'\*\*이 포함된 step3-content-raw.md를 생성합니다.  
*   
  6. 기초 검수 (AI): (예: Claude API) AI가 step3-content-raw.md의 표현, 문법, *Shortcode 문법 오류*를 1차 검수하여 step3-revised-final.md를 생성합니다.  
*   
  7. **리치 콘텐츠 렌더링 (AI)**: (New Logic)  
  * run\_pipeline.py의 고급 파서(예: markdown-it-py)가 step3-revised-final.md를 읽습니다.  
  * 일반 Markdown은 HTML(예: \<p\>)로 변환합니다.  
  * Shortcode(예: \[WineCard: {...}\])를 만나면, components/WineCard.html을 로드하고 {...} JSON 데이터를 주입(Props)하여 렌더링합니다.  
  * 이 모든 것을 templates/blog-post-default.html에 삽입하여 최종 step3-revised-final.html 파일을 생성합니다.  
*   
  8. **\[Human 3\] 원본 최종 검수**: PM이 대쉬보드에서 **"Markdown (수정)" 탭** (step3-revised-final.md)과 **"HTML 프리뷰" 탭** (step3-revised-final.html)을 모두 검토 후 승인합니다.  
*   
  9. SNS 형태로 변형 (AI)  
*   
  10. SNS 기초 검수 (AI)  
*   
  11. **\[Human 4\] SNS 최종 검수**  
*   
  12. 전체 번역 (AI) (DeepL API)  
*   
  13. 번역 검수 및 교정 (AI) (예: Claude API)  
*   
  14. **\[Human 5\] 배포**: PM이 최종 산출물(HTML본, SNS본, 번역본)을 각 플랫폼에 배포.

## **5\. 대쉬보드 UI/UX 상세 기획 (localhost:3000)**

### **5.1. 핵심 화면 (Views)**

* **View 1: 메인 페이지 (/) \- 사이클 런처 및 스케줄러**  
  * **기능**: 새 콘텐츠 생성 사이클을 시작, 예약, 또는 과거 사이클을 조회합니다.  
  * **컴포넌트**: "새 사이클 즉시 시작" 버튼 (Modal 1 호출), "과거 사이클 목록" (View 2로 이동), "예약 작업 관리" (Modal 3 호출)  
* **View 2: 사이클 대쉬보드 (/cycle/\<YYMMDD\>) \- 메인 워크스페이스**  
  * **기능**: 14단계 워크플로우를 실행하고, 승인하고, 모니터링합니다.  
  * **컴포넌트**: 워크플로우 영역 (14단계 상태 시각화), 로그 뷰어.  
  * **UI 가이드**: 모든 버튼과 상태 표시에 **Remix Icon**을 사용하여 시각적 일관성을 유지합니다. (예: 실행 \<i class="ri-play-line"\>\</i\>, 승인 대기 \<i class="ri-user-search-line"\>\</i\>, 완료 \<i class="ri-check-line"\>\</i\>)

### **5.2. 핵심 모달 (Modals / Pop-ups)**

* **Modal 1: 새 사이클 생성 (View 1에서 호출)**  
  * **기능**: Prompt 1 (자료 조사) 실행을 위한 파라미터를 설정합니다.  
  * **컴포넌트**: "전략 모드 선택" (Standard/Specialized), "HTML 템플릿 선택" (templates/ 폴더 스캔), "실행" 버튼  
* **Modal 2: 산출물 뷰어 & 검수 (View 2에서 호출)**  
  * **기능**: '확장 마크다운'을 확인, 수정, 승인합니다.  
  * **컴포넌트**:  
    * **뷰어 탭**: "Markdown (수정)" (EasyMDE 에디터), "HTML 프리뷰" (iframe 렌더링)  
    * **Markdown 에디터 툴바**:  
      * "이모지/에셋 삽입" 버튼 (Modal 4 호출)  
      * **"컴포넌트 삽입" 버튼**: guidelines/component\_guide.md를 파싱하여 \[NutritionInfo: {...}\], \[PremiumBanner\] 등 사용 가능한 Shortcode 목록(스니펫)을 보여주고 클릭 시 에디터에 삽입합니다.  
    * "저장" 버튼, "승인 (Approve)" 버튼  
* **Modal 3: 새 예약 추가 (View 1에서 호출)**  
  * **기능**: Step 1 작업의 예약 및 반복을 설정합니다.  
  * **컴포넌트**: "실행 시간 설정" (Cron UI), "전략 모드 선택", "HTML 템플릿 선택", "저장" 버튼  
* **Modal 4: 에셋 삽입 (Modal 2에서 호출)**  
  * **기능**: assets/emoji/ 폴더의 스티커를 에디터에 삽입합니다.  
  * **컴포넌트**: 이미지/GIF 목록 (파일명 표시). 클릭 시 에디터에 \!\[file-name\](/assets/emoji/file-name.png) 텍스트 삽입.

## **6\. 핵심 기능 요구사항 (Functional Requirements)**

* **EPIC 0: 대쉬보드 (Dashboard)**  
  * **USR-0.1 (워크플로우 실행)**: PM은 대쉬보드의 버튼 클릭으로 14단계 파이프라인을 단계별로 트리거해야 한다. (백엔드 POST /api/cycle/run/\<step\_id\> 호출)  
  * **USR-0.2 (워크플로우 상태)**: 대쉬보드는 14단계의 (대기, 진행중, 승인 대기, 완료, 오류) 상태를 GET /api/cycle/status 폴링(polling)을 통해 실시간으로 시각화해야 한다.  
  * **USR-0.3 (산출물 조회/수정)**: PM은 대쉬보드 내에서 모든 stepN 폴더의 .md 산출물을 EasyMDE 에디터로 조회, 수정, 저장(POST /api/cycle/content)할 수 있어야 한다.  
  * **USR-0.4 (워크플로우 승인)**: PM은 **\[Human 2, 4, 8, 11\]** 단계에서 "승인" 버튼을 눌러야만(POST /api/cycle/approve/\<step\_id\>) 다음 단계가 활성화된다.  
  * **USR-0.5 (사이클 생성)**: PM은 대쉬보드에서 '전략 모드'와 'HTML 템플릿'을 선택하여 새 콘텐츠 생성 사이클(POST /api/cycle/start)을 시작할 수 있어야 한다.  
  * **USR-0.6 (예약 실행)**: PM은 대쉬보드에서 Step 1 작업의 반복 실행을 예약할 수 있어야 한다. (백엔드 scheduler.py와 연동)  
  * **USR-0.7 (에셋 삽입)**: PM은 Markdown 에디터에서 assets/emoji/ 폴더의 이미지/GIF를 클릭 한 번으로 본문에 삽입할 수 있어야 한다.  
  * **USR-0.8 (HTML 프리뷰)**: PM은 Step 8 (원본 검수) 단계에서, templates/와 components/가 모두 적용된 **최종 리치 HTML 프리뷰**를 확인할 수 있어야 한다.  
  * **USR-0.9 (컴포넌트 삽입)**: PM은 Markdown 에디터에서 guidelines/component\_guide.md에 정의된 Shortcode 스니펫을 클릭 한 번으로 삽입할 수 있어야 한다.  
  * **USR-0.10 (UI 일관성)**: 대쉬보드의 모든 아이콘은 **Remix Icon**을 사용해야 하며, 커스텀 폰트가 필요할 경우 **Google Fonts**를 CDN으로 로드해야 한다.  
* **EPIC 1: 백엔드 로직 (Backend Logic)**  
  * **USR-1.1 (모델 유연성)**: .env 파일로 모델명 교체.  
  * **USR-1.2 (인간 승인 대기)**: 백엔드 파이프라인은 인간 승인 지점에서 명확히 '일시 중지(Pause)'되어야 한다.  
  * **USR-1.3 (워크플로우 분기)**: 'Standard' 또는 'Specialized' 모드에 따라 올바른 프롬프트 세트 로드.  
  * **USR-1.4 (리치 렌더링)**: Step 7은 markdown-it-py와 같은 고급 파서를 사용하여 '확장 마크다운(.md)'을 components/ 폴더의 컴포넌트와 조합, 최종 HTML로 렌더링해야 한다.  
  * **USR-1.5 (피드백 파일 생성)**: 모든 AI 검수 단계(6, 10, 13)는 \*-w.feedback.md 파일을 반드시 생성.  
* **EPIC 2: 에러 핸들링 및 안정성 (Reliability & Safety)**  
  * **USR-2.1 (멱등성)**: \[Step N 실행\] 버튼 중복 클릭 시, 이미 '진행중'이거나 '대기중'인 작업의 중복 실행을 **방지**하고 HTTP 409 Conflict를 반환해야 합니다.  
  * **USR-2.2 (싱글톤 예약)**: Step 1 예약 작업 실행 시, Redis Lock을 사용하여 이전 작업이 아직 실행 중이라면 이번 스케줄은 건너뛰어야 합니다.  
  * **USR-2.3 (재시도 제한)**: 429/503 API 오류 발생 시, **최대 3회** Exponential Backoff 재시도 후 실패 처리합니다.  
  * **USR-2.4 (외부 예산)**: PM(개발자) SHALL 모든 외부 API(Google, Claude, DeepL 등)의 관리자 콘솔에서 \*\*월간/일간 API 사용량 하드 리밋(Hard Limit)\*\*을 설정해야 합니다.  
  * **USR-2.5 (에러 로깅)**: 401/400 API 오류, 렌더링 오류, 비동기 오류 등 모든 실패는 로그 뷰어에 명확한 한글 에러 메시지를 표시해야 합니다.  
  * **USR-2.6 (데이터 무결성)**: 에디터 '저장' 실패 시, 수정본 유실 방지를 위한 \[클립보드에 복사\] 버튼이 포함된 Toast 알림을 제공해야 합니다.

## **7\. 기술 사양 (Technical Specifications)**

### **7.1. 프로그래밍 언어 및 프레임워크**

* **백엔드 (Backend)**: **Python 3.10+**, **Flask**  
* **프론트엔드 (Frontend)**: **Vanilla JavaScript (ES6+)**, **HTML5**, **CSS3**  
* **선정 이유**: React/Vue의 복잡성 없이, Flask(백엔드)가 렌더링한 HTML을 Vanilla JS(프론트엔드)가 보조하는 방식이 로컬 대쉬보드 목적에 가장 빠르고 효율적입니다.

### **7.2. 주요 Python 의존성 (Backend)**

requirements.txt에 포함되어야 할 핵심 라이브러리 목록입니다.

* **웹 서버/비동기**: flask, celery, redis  
* **AI API 클라이언트**: google-generativeai, anthropic, deepl, perplexity-api  
* **유틸리티**: python-dotenv, PyYAML, APScheduler  
* **렌더링**: markdown-it-py (Shortcode 파싱용), Jinja2 (components/ 템플릿 렌더링용)

### **7.3. 프론트엔드 스타일링 & 에셋 (Frontend Styling & Assets)**

* **CSS 프레임워크**: **Bootstrap 5** (CDN 버전)  
  * **선정 이유**: 신속한 개발. PRD 5장에서 요구하는 Modal, Button 등 모든 UI 컴포넌트를 즉시 구현할 수 있습니다.  
* **아이콘 라이브러리**: **Remix Icon** (CDN 버전)  
  * **선정 이유**: PM님께서 요청. 가볍고 디자인이 일관되며, 제공된 템플릿 예시(ContentDetailClient.tsx 등)에서 이미 ri- 접두사로 광범위하게 사용 중임.  
* **폰트 라이브러리**: **Google Fonts** (CDN 버전)  
  * **선정 이유**: PM님께서 요청. CSS 기본 폰트 외의 커스텀 브랜딩 폰트가 필요할 경우, CDN을 통해 간편하게 로드.

### **7.4. 콘텐츠 에디터 (Markdown Editor)**

* **라이브러리**: **EasyMDE**  
* **선정 이유**: 오픈소스. Markdown 에디터 \+ 실시간 프리뷰 기능을 제공하며, Vanilla JS 환경에 통합하기 쉽고 툴바 커스터마이징(에셋/컴포넌트 삽입 버튼)이 용이합니다.

### **7.5. 콘텐츠 렌더링 엔진**

* **라이브러리**: **markdown-it-py** (Python) \+ **Jinja2** (Python)  
* **선정 이유**: Step 7에서 '확장 마크다운'을 파싱해야 합니다.  
  1. markdown-it-py가 플러그인을 통해 \[MyComponent: {...}\] 같은 커스텀 태그를 감지합니다.  
  2. 감지된 태그에 대해, Jinja2 템플릿 엔진이 components/MyComponent.html 파일을 로드하고 {...} JSON 데이터를 props로 주입하여 렌더링합니다. (단순 markdown2 라이브러리로는 이 기능 구현이 불가능합니다.)

## **8\. 데이터 스키마 (Data Schemas)**

### **8.1. manifest.json 스키마**

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

## **9\. API 엔드포인트 명세 (API Endpoint Specifications)**

프론트엔드(Vanilla JS)와 백엔드(Flask)가 통신하기 위한 API 명세입니다.

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

## **10\. 비동기 작업 아키텍처 (Async Task Architecture)**

긴 AI 작업을 처리하기 위해 Task Queue 아키텍처를 도입합니다.

1. **구성 요소**: **Flask (웹 서버)**, **Redis (메시지 브로커)**, **Celery (Task Worker)**.  
2. **작동 방식 (2.2 순서도 참조)**:  
   * PM이 \[Step 5 실행\] 버튼을 클릭합니다.  
   * Flask는 HTTP 202 (Accepted)를 0.1초 만에 즉시 응답하고, Celery에게 "Step 5 작업해줘"라는 메시지를 Redis를 통해 전달합니다.  
   * 별도 프로세스(컨테이너)인 Celery Worker가 이 메시지를 받아, 백그라운드에서 1분 동안 run\_pipeline.py의 Step 5 로직을 실행합니다.  
   * PM의 대쉬보드는 5초마다 GET /api/cycle/status를 호출하여 "Step 5: 진행중..." \-\> "Step 6: 완료"로 바뀌는 상태를 표시합니다.

## **11\. 개발 환경 구축 가이드 (Docker)**

PM님(개발자)께서 이 시스템을 실행하기 위한 Docker 환경 설정 가이드입니다.

### **11.1. 1단계: Docker Desktop 설치**

* docker.com/products/docker-desktop/에서 본인의 OS(Windows/Mac)에 맞는 **Docker Desktop**을 다운로드하여 설치합니다.

### **11.2. 2단계: 프로젝트 루트 폴더에 파일 2개 생성**

프로젝트 루트(auto-system-contents-generator/)에 다음 Dockerfile과 docker-compose.yml 파일을 생성합니다.

**Dockerfile** (Python/Flask/Celery 앱 빌드 설계도)

\# 1\. Python 3.10을 기본 이미지로 사용  
FROM python:3.10-slim

\# 2\. 작업 디렉토리 설정  
WORKDIR /app

\# 3\. 의존성 파일 복사 및 설치  
COPY requirements.txt requirements.txt  
RUN pip install \--no-cache-dir \-r requirements.txt

\# 4\. 전체 프로젝트 소스 코드 복사  
COPY . .

\# 5\. Flask 앱 실행 포트 노출 (3000번)  
EXPOSE 3000

\# 6\. 기본 실행 명령어 (Flask 서버)  
CMD \["flask", "run", "--host=0.0.0.0", "--port=3000"\]

**docker-compose.yml** (전체 서비스(Flask+Redis+Celery) 실행기)

version: '3.8'

services:  
  \# 1\. Redis (메시지 브로커)  
  redis:  
    image: "redis:alpine"  
    ports:  
      \- "6379:6379"

  \# 2\. Web (Flask 백엔드 및 대쉬보드)  
  web:  
    build: .  
    command: flask run \--host=0.0.0.0 \--port=3000  
    volumes:  
      \- .:/app  \# \[★\] 로컬 폴더와 컨테이너 내부를 동기화  
    ports:  
      \- "3000:3000"  
    env\_file:  
      \- .env    \# .env 파일의 API 키를 컨테이너로 전달  
    depends\_on:  
      \- redis

  \# 3\. Worker (Celery 비동기 작업자)  
  worker:  
    build: .  
    command: celery \-A dashboard.app.celery worker \--loglevel=info  
    volumes:  
      \- .:/app  \# \[★\] 로컬 폴더와 컨테이너 내부를 동기화  
    env\_file:  
      \- .env  
    depends\_on:  
      \- redis

### **11.3. 3단계: 시스템 실행 및 종료**

* **시스템 실행 (빌드 포함)**:  
  * (터미널에서 auto-system-contents-generator/ 폴더로 이동)  
  * docker-compose up \--build  
  * (최초 1회 빌드 후, 다음부터는 docker-compose up만 입력)  
* **시스템 종료**:  
  * (터미널에서 Ctrl+C를 누른 후)  
  * docker-compose down

## **12\. 실패 및 오류 케이스 (Error Handling & Scenarios)**

Shortcode 렌더링 오류를 포함한 최종 에러 핸들링 시나리오입니다.

* **1\. 환경 및 설정 오류 (Environment & Config)**  
  * **케이스**: .env 파일 누락, 필수 API 키 누락, prompts/ 파일 누락, CDN 연결 실패 (인터넷 끊김).  
  * **대응**: run\_pipeline.py 실행 시 즉시 실패. **로그 뷰어**에 \[ERROR\] 필수 API 키 'CLAUDE\_API\_KEY'가 .env 파일에 설정되지 않았습니다.와 같이 명확한 한글 메시지 출력.  
* **2\. 외부 API 오류 (External Dependencies)**  
  * **케이스**: 401/403 (인증 오류), 429 (Rate Limit), 500/503 (서버 다운), 400 (유해성 응답 거부).  
  * **대응**:  
    * (429/503): 백엔드에서 **Exponential Backoff 자동 재시도 (최대 3회)** 구현. 로그 뷰어에 \[INFO\] API Rate Limit 감지. 10초 후 자동으로 재시도합니다... 표시.  
    * (401/400): 즉시 실패. **로그 뷰어**에 \[ERROR \- Claude\] API 키가 유효하지 않습니다. 또는 \[ERROR\] AI가 유해 콘텐츠 필터에 의해 응답을 거부했습니다. 표시. 대쉬보드에 \[재시도\] 버튼 활성화.  
* **3\. 파이프라인 및 데이터 오류 (Internal Logic & Data)**  
  * **케이스**: 입력 파일 누락 (예: step2-outline.md 삭제), 파일 쓰기 권한 오류, 인코딩 오류, AI의 빈 응답(Null Response).  
  * **대응**: 즉시 실패. **로그 뷰어**에 \[CRITICAL\] AI 작업은 성공했으나, 'content-output/' 폴더에 파일 쓰기 권한이 없습니다. 또는 \[ERROR\] AI가 빈 응답을 반환했습니다. 표시.  
* **4\. 비동기 작업 및 스케줄러 오류 (Async & Scheduler)**  
  * **케이스**: Task Queue(Redis) 연결 실패, 비동기 작업(Task) 타임아웃 (30분 이상 소요).  
  * **대응**:  
    * (연결 실패): \[Step 5 실행\] 클릭 즉시 \[Toast 알림\] 🔴 오류: 백그라운드 작업 큐(Redis)에 연결할 수 없습니다. 표시.  
    * (타임아웃): GET /api/cycle/status가 30분 이상 '진행중'이면, **대쉬보드 상태**를 '시간 초과(Timeout)'로 변경.  
* **5\. 사용자 경험(UX) 및 데이터 무결성 오류 (UI/UX & Integrity)**  
  * **케이스**: PM이 Modal 2 (EasyMDE)에서 \[저장\] 버튼을 눌렀으나 파일 쓰기 실패.  
  * **대응**: \[Toast 알림\] 🔴 저장 실패: (오류 메시지). \[클립보드에 복사\] 버튼을 즉시 제공하여, **PM님의 수정본이 유실되는 것을 반드시 방지**해야 함.  
* **6\. 리치 콘텐츠 렌더링 오류 (Rendering Errors)**  
  * **케이스 (1) \- 문법 오류**: AI가 Step 5에서 \[WineCard: {"name": "Test" (JSON 문법 오류)처럼 깨진 JSON Shortcode를 생성함.  
  * **대응 (1)**: Step 7의 markdown-it-py 파서가 이 오류를 감지. **로그 뷰어**에 \[ERROR\] 렌더링 실패: 'WineCard' 컴포넌트의 JSON 데이터 파싱에 실패했습니다. 표시. Modal 2의 **HTML 프리뷰 탭**에 "렌더링 오류 발생" 메시지 표시.  
  * **케이스 (2) \- 컴포넌트 누락**: AI가 \[NonExistentComponent\]처럼 components/ 폴더에 존재하지 않는 컴포넌트를 호출함.  
  * **대응 (2)**: **로그 뷰어**에 \[ERROR\] 렌더링 실패: 'NonExistentComponent'를 찾을 수 없습니다. 표시.

## **13\. 향후 로드맵 (v2.0)**

* **v1.9 (현재)**: 안정성 우선. \[Human 2, 4, 8, 11\] 단계에서 명시적 승인.  
* **v2.0 (미래)**: v1.9 운영을 통해 Prompt 4(SNS)의 AI 검수 품질이 안정적이라고 판단되면, 대쉬보드(View 2)에 "SNS 자동 승인" 체크박스를 추가하여 \[Human 4\] 단계를 건너뛸 수 있는 '자동화 최적화' 플로우를 구현한다.