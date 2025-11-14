# **Requirements Document: auto-system-contents-generator (v2.0)**

* **문서 버전**: 2.0 (아키텍처 변경: Tailwind/Alpine.js 기반 HTML 스니펫 생성)
* **작성일**: 2025년 11월 14일

## **1\. Introduction**

auto-system-contents-generator는 콘텐츠 제작의 전 과정을 자동화하는 로컬 백엔드 파이프라인 및 웹 대쉬보드입니다. 이 시스템은 Perplexity, Google(Gemini), Anthropic(Claude), DeepL 등 검증된 AI API를 활용하여 14단계의 워크플로우를 통해 자료 조사, 콘텐츠 생성, AI 검수, 번역, 그리고 최종적으로 **Tailwind/Alpine.js 기반의 깨끗한 HTML 스니펫을 생성**하는 작업을 수행합니다.

PM(사용자)은 localhost 대쉬보드를 통해 이 14단계 파이프라인을 실행, 모니터링, 검수 및 승인합니다.

## **2\. Glossary (주요 용어)**

* **대쉬보드 (Dashboard)**: localhost에서 실행되는 웹 UI. PM이 파이프라인을 실행하고 검수하는 제어판.
* **사이클 (Cycle)**: 14단계의 콘텐츠 생성 워크플로우 1회 실행 단위 (기준일 YYMMDD 기준).
* **HTML 스니펫 (HTML Snippet)**: AI가 생성하는 최종 결과물. Tailwind CSS 클래스와 Alpine.js 속성만으로 구성된 깨끗한 HTML 코드 조각입니다.
* **비동기 작업 (Async Task)**: 1분 이상 소요되는 AI 작업을 처리하기 위한 백그라운드 실행 방식 (Celery + Redis).
* **Human Checkpoint**: PM의 수동 승인이 필요한 14단계 중 5단계 (주제 선택, 구조 컨펌, 원본 검수, SNS 검수, 배포).

## **3\. Requirements (요구사항)**

### **Requirement 1: 대쉬보드 워크플로우 관리**

**User Story:** PM으로서, 나는 localhost 대쉬보드에서 콘텐츠 생성의 모든 14단계를 시각적으로 확인하고, 다음 단계를 트리거하며, 현재 상태를 모니터링하고 싶습니다.

#### **Acceptance Criteria**

1. THE Dashboard SHALL localhost에서 접근 가능해야 합니다.
2. THE Dashboard SHALL 14단계 워크플로우를 시각적으로 표시해야 합니다.
3. THE Dashboard SHALL 각 단계의 상태를 (대기, 진행중, 승인 대기, 완료, 오류)로 명확히 표시해야 합니다.
4. THE Dashboard SHALL PM의 승인이 필요한 [Human Checkpoint] 단계(2, 4, 8, 11, 14)에서 파이프라인을 자동으로 '일시 중지(Pause)'해야 합니다.
5. WHEN PM이 '실행' 버튼을 클릭하면, THE Dashboard SHALL POST /api/cycle/run/<step_id>를 호출하여 해당 AI 단계를 비동기(Async)로 트리거해야 합니다.
6. WHEN PM이 '승인' 버튼을 클릭하면, THE Dashboard SHALL POST /api/cycle/approve/<step_id>를 호출하여 다음 단계의 실행 버튼을 활성화해야 합니다.
7. THE Dashboard SHALL GET /api/cycle/status를 주기적으로(예: 5초) 폴링(polling)하여 UI 상태를 백엔드와 동기화해야 합니다.
8. THE Dashboard SHALL run_pipeline.py의 실시간 로그를 표시하는 '로그 뷰어'를 제공해야 합니다.

### **Requirement 2: 콘텐츠 생성 사이클 관리**

**User Story:** PM으로서, 나는 새로운 콘텐츠 작업을 시작(초기화)하거나, 과거의 작업 내역을 조회하고 싶습니다.

#### **Acceptance Criteria**

1. WHEN PM이 '새 사이클 시작' 버튼을 클릭하면, THE Dashboard SHALL 'Modal 1'을 표시해야 합니다.
2. THE Modal 1 SHALL '전략 모드 (Standard/Specialized)' 선택 옵션을 제공해야 합니다.
3. WHEN PM이 '실행' 버튼을 클릭하면, THE System SHALL POST /api/cycle/start를 호출하고, content-output/YYMMDD/ 폴더와 manifest.json 파일을 생성하며 Step 1을 즉시 실행해야 합니다.
4. THE Dashboard SHALL content-output/ 폴더를 스캔하여 '과거 사이클 목록'을 View 1에 표시해야 합니다.

### **Requirement 3: 예약 실행**

**User Story:** PM으로서, 나는 Step 1: 자료 조사 작업이 매주 월요일 새벽에 자동으로 실행되도록 예약하고 싶습니다.

#### **Acceptance Criteria**

1. THE Dashboard SHALL '예약 작업 관리' UI를 View 1에 제공해야 합니다.
2. WHEN PM이 '새 예약 추가' 버튼을 클릭하면, THE Dashboard SHALL 'Modal 3'을 표시해야 합니다.
3. THE Modal 3 SHALL 실행 시간(Cron), 전략 모드를 설정하는 UI를 제공해야 합니다.
4. THE System SHALL APScheduler (또는 유사 스케줄러)를 사용하여 예약된 작업을 백그라운드에서 자동 실행해야 합니다.

### **Requirement 4: 콘텐츠 검수 및 수정**

**User Story:** PM으로서, 나는 AI가 생성한 .md 초안을 검토하고, 최종 생성된 HTML 스니펫이 운영 환경과 동일한 모습으로 보이는지 확인한 뒤 승인하고 싶습니다.

#### **Acceptance Criteria**

1. WHEN PM이 [Human Checkpoint] (예: Step 8)에서 '검토하기' 버튼을 클릭하면, THE Dashboard SHALL 'Modal 2' (산출물 뷰어)를 표시해야 합니다.
2. THE Modal 2 SHALL "Markdown" 탭과 **"HTML 최종 프리뷰"** 탭을 제공해야 합니다.
3. THE "Markdown" 탭 SHALL EasyMDE (또는 유사 에디터)를 사용하여 .md 파일(step2-outline.md 등)의 내용을 표시하고, PM이 이를 직접 수정 및 저장(POST /api/cycle/content)할 수 있도록 허용해야 합니다.
4. THE "HTML 최종 프리뷰" 탭 SHALL **`globals.css`와 `Alpine.js`가 적용된 iframe**을 통해 `final-content.html` 파일의 내용을 최종 운영 환경과 동일하게 렌더링해야 합니다.

### **Requirement 5: 에셋 관리**

**User Story:** PM으로서, 나는 .md 콘텐츠를 수정할 때, 미리 준비된 이모지(스티커)를 에디터에서 쉽게 삽입하고 싶습니다.

#### **Acceptance Criteria**

1. THE Markdown 에디터 SHALL "이모지/에셋 삽입" 버튼을 제공해야 합니다.
2. WHEN PM이 이 버튼을 클릭하면, THE Dashboard SHALL Modal 4를 표시하고 assets/emoji/ 폴더의 이미지/GIF 목록을 표시해야 합니다.
3. WHEN PM이 스티커를 클릭하면, THE 에디터 SHALL 커서 위치에 `![emotion-happy](/assets/emoji/emotion-happy.png)`와 같은 Markdown 이미지 태그를 삽입해야 합니다.

### **Requirement 6: 최종 HTML 생성**

**User Story:** 개발자(PM)로서, 나는 AI가 마크다운 초안을 `AI_CONTENT_GENERATOR_GUIDE.md` 규칙에 따라 완벽한 HTML 스니펫으로 자동 변환하기를 원합니다.

#### **Acceptance Criteria**

1. THE System SHALL Step 7: 최종 HTML 생성 단계를 포함해야 합니다.
2. THE Step 7 SHALL AI를 통해, `step3-revised-final.md`와 `AI_CONTENT_GENERATOR_GUIDE.md`를 입력받아 처리해야 합니다.
3. THE AI SHALL `AI_CONTENT_GENERATOR_GUIDE.md`에 명시된 규칙(Tailwind CSS 클래스, Alpine.js 속성, 금지된 태그 등)을 반드시 준수하여 최종 HTML 스니펫을 생성해야 합니다.
4. THE Step 7 SHALL 최종 결과물을 `final-content.html` 파일로 저장해야 합니다.

### **Requirement 7: 에러 핸들링 및 안정성 (비용 폭증 방지)**

**User Story:** PM으로서, 나는 AI 작업이 실패했을 때, 브라우저가 멈추지 않아야 하며, 왜 실패했는지 명확한 한글 에러 메시지를 로그 뷰어에서 확인하고 싶습니다. 또한, 버그로 인해 API 비용이 폭증하지 않도록 시스템이 설계되어야 합니다.

#### **Acceptance Criteria**

1. THE System SHALL 긴 AI 작업(1분 이상)을 비동기(Async)로 처리해야 합니다 (Celery + Redis).
2. WHEN PM이 비동기 작업을 실행하면, THE 대쉬보드 SHALL 0.1초 이내에 (202 Accepted) 응답을 받고 '진행중' 상태로 전환되어야 합니다.
3. **(비용 방지 1: 멱등성)** WHEN PM이 [Step 5 실행] 버튼을 중복 클릭해도, THE System SHALL manifest.json의 status를 확인하여, 이미 '진행중'이거나 '대기중'인 작업의 중복 실행을 **방지**하고 HTTP 409 Conflict를 반환해야 합니다.
4. **(비용 방지 2: 싱글톤 예약)** WHEN Step 1 예약 작업이 실행될 때, THE System SHALL Redis Lock을 사용하여, 이전 Step 1 작업이 아직 실행 중이라면 이번 스케줄은 건너뛰어야 합니다.
5. **(비용 방지 3: 재시도 제한)** WHEN API가 429(Rate Limit) 또는 503(서버 오류)을 반환하면, THE System SHALL Exponential Backoff을 통해 **최대 3회**까지만 자동 재시도하고, 3회 모두 실패 시 작업을 '오류' 상태로 전환해야 합니다.
6. **(비용 방지 4: 외부 예산)** PM(개발자) SHALL 모든 외부 API(Google, Claude, DeepL 등)의 관리자 콘솔에서 **월간/일간 API 사용량 하드 리밋(Hard Limit)**을 설정해야 합니다.
7. WHEN API가 401(인증 오류) 또는 400(유해성 거부)을 반환하면, THE System SHALL 즉시 실패 처리하고, 로그 뷰어에 `[ERROR - Claude] API 키가 유효하지 않습니다.`와 같은 명확한 한글 에러 메시지를 표시해야 합니다.
8. WHEN AI가 Step 7에서 가이드라인을 위반하는 HTML(예: `<script>` 태그)을 생성하면, THE System SHALL 로그 뷰어에 `[WARNING] AI가 생성한 HTML에 잠재적 규칙 위반이 감지되었습니다.`라고 표시할 수 있습니다. (선택 사항)
9. WHEN PM이 에디터에서 '저장'을 눌렀으나 파일 쓰기에 실패하면, THE 대쉬보드 SHALL [Toast 알림] 🔴 저장 실패와 함께, **PM의 수정본 유실을 방지하기 위한 '클립보드에 복사' 버튼**을 제공해야 합니다.
10. WHEN docker-compose.yml의 Redis/Celery 서비스에 연결할 수 없으면, THE 대쉬보드 SHALL 작업 실행 시 [Toast 알림] 🔴 오류: 백그라운드 작업 큐(Redis)에 연결할 수 없습니다.를 표시해야 합니다.
