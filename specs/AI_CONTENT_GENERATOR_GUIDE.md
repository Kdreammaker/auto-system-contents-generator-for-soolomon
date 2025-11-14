# AI 콘텐츠 자동 생성기 개발 가이드

**대상**: HTML 콘텐츠 자동 생성기 개발자  
**작성일**: 2025-01-12  
**버전**: 1.0

---

## 📋 목차

1. [개요](#개요)
2. [에디터 아키텍처](#에디터-아키텍처)
3. [HTML 생성 규칙](#html-생성-규칙)
4. [사용 가능한 컴포넌트](#사용-가능한-컴포넌트)
5. [예시 코드](#예시-코드)
6. [Admin 페이지 사용법](#admin-페이지-사용법)
7. [검증 및 테스트](#검증-및-테스트)

---

## 개요

### 프로젝트 목표

AI가 **인터랙티브 기능이 포함된 고품질 리치 콘텐츠**를 생성하여 Soolomon 웹사이트에 발행합니다.

### 핵심 요구사항

- ✅ `<style>`, `<script>` 태그 **절대 사용 금지**
- ✅ Tailwind CSS 클래스만 사용
- ✅ Alpine.js 속성으로 인터랙션 구현
- ✅ 깨끗한 HTML 스니펫만 생성

---

## 에디터 아키텍처

### 시스템 구조

```
┌─────────────────────────────────────────────────────────┐
│  Soolomon 콘텐츠 발행 시스템                             │
└─────────────────────────────────────────────────────────┘

1. AI 콘텐츠 생성기 (당신의 역할)
   ├─ 클린 HTML 스니펫 생성
   ├─ Tailwind 클래스 사용
   └─ Alpine.js 속성 추가

2. Tiptap HTML 에디터 (관리자 페이지)
   ├─ AI 생성 HTML 붙여넣기
   ├─ 수동 편집 가능
   └─ 미리보기

3. 서버 측 검증
   ├─ DOMPurify HTML Sanitization
   ├─ Alpine.js 표현식 검증
   └─ XSS 방지

4. Next.js 프론트엔드
   ├─ globals.css 전역 로드 (1회)
   ├─ Alpine.js 전역 로드 (1회)
   └─ 콘텐츠 렌더링
```


### 전역 리소스 (이미 로드됨)

**CSS (globals.css)**:
```css
/* 이미 Next.js가 전역으로 로드함 */
--primary: oklch(0.85 0.15 85);      /* Warm Amber */
--accent: oklch(0.85 0.15 85);       /* Warm Amber */
--background: oklch(1 0 0);          /* White */
--foreground: oklch(0.1 0 0);        /* Dark Gray */
--muted: oklch(0.96 0.01 85);        /* Light Gray */
--border: oklch(0.9 0.01 85);        /* Border */
```

**JavaScript (Alpine.js)**:
```html
<!-- 이미 Next.js가 전역으로 로드함 -->
<script src="https://cdn.jsdelivr.net/npm/alpinejs@3.x.x/dist/cdn.min.js"></script>
```

**당신이 할 일**: 위 리소스를 **사용**하기만 하면 됩니다. 추가로 로드하지 마세요!

---

## HTML 생성 규칙

### ✅ 허용되는 것

1. **Tailwind CSS 클래스**
   ```html
   <div class="bg-primary text-white p-4 rounded-lg">
     콘텐츠
   </div>
   ```

2. **Alpine.js 속성**
   ```html
   <div x-data="{ open: false }">
     <button x-on:click="open = !open">토글</button>
     <div x-show="open">내용</div>
   </div>
   ```

3. **시맨틱 HTML**
   ```html
   <article>
     <h1>제목</h1>
     <p>본문</p>
   </article>
   ```

### ❌ 금지되는 것

1. **`<style>` 태그**
   ```html
   <!-- ❌ 절대 금지 -->
   <style>
     .my-class { color: red; }
   </style>
   ```

2. **`<script>` 태그**
   ```html
   <!-- ❌ 절대 금지 -->
   <script>
     console.log('Hello');
   </script>
   ```

3. **인라인 스타일**
   ```html
   <!-- ❌ 금지 (예외: display:none만 허용) -->
   <div style="color: red;">콘텐츠</div>
   
   <!-- ✅ 허용 (Alpine.js 초기 상태) -->
   <div x-show="false" style="display: none;">콘텐츠</div>
   ```

4. **위험한 속성**
   ```html
   <!-- ❌ 절대 금지 -->
   <img src="x" onerror="alert('XSS')">
   <a href="javascript:alert('XSS')">링크</a>
   ```

---

## 사용 가능한 컴포넌트

### 1. 탭 (Tabs)

**용도**: 여러 콘텐츠를 탭으로 구분

**생성 코드**:
```html
<div x-data="{ activeTab: 'tab1' }" class="my-8">
  <!-- 탭 버튼 -->
  <div class="flex space-x-1 bg-muted p-1 rounded-lg">
    <button
      x-on:click="activeTab = 'tab1'"
      :class="{ 'bg-background text-primary shadow-sm': activeTab === 'tab1', 'text-muted-foreground hover:bg-background/50': activeTab !== 'tab1' }"
      class="flex-1 px-4 py-3 rounded-md transition-all duration-200"
    >
      탭 1
    </button>
    <button
      x-on:click="activeTab = 'tab2'"
      :class="{ 'bg-background text-primary shadow-sm': activeTab === 'tab2', 'text-muted-foreground hover:bg-background/50': activeTab !== 'tab2' }"
      class="flex-1 px-4 py-3 rounded-md transition-all duration-200"
    >
      탭 2
    </button>
  </div>
  
  <!-- 탭 콘텐츠 -->
  <div x-show="activeTab === 'tab1'" class="p-6 border rounded-lg mt-2">
    탭 1의 콘텐츠입니다.
  </div>
  <div x-show="activeTab === 'tab2'" class="p-6 border rounded-lg mt-2" style="display: none;">
    탭 2의 콘텐츠입니다.
  </div>
</div>
```


### 2. 아코디언 (Accordion)

**용도**: 접고 펼칠 수 있는 콘텐츠

**생성 코드**:
```html
<div class="space-y-2 my-8">
  <!-- 아코디언 아이템 1 -->
  <div x-data="{ open: false }" class="border rounded-lg">
    <button
      x-on:click="open = !open"
      class="w-full flex items-center justify-between p-4 text-left hover:bg-muted transition-colors"
    >
      <span class="font-semibold">질문 1: 맥주와 치킨이 잘 어울리는 이유는?</span>
      <svg
        :class="{ 'rotate-180': open }"
        class="w-5 h-5 transition-transform"
        fill="none"
        stroke="currentColor"
        viewBox="0 0 24 24"
      >
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
      </svg>
    </button>
    <div x-show="open" x-collapse class="p-4 border-t">
      <p>맥주의 탄산과 쓴맛이 치킨의 기름기를 중화시켜주기 때문입니다.</p>
    </div>
  </div>
  
  <!-- 아코디언 아이템 2 -->
  <div x-data="{ open: false }" class="border rounded-lg">
    <button
      x-on:click="open = !open"
      class="w-full flex items-center justify-between p-4 text-left hover:bg-muted transition-colors"
    >
      <span class="font-semibold">질문 2: 추천하는 맥주 종류는?</span>
      <svg
        :class="{ 'rotate-180': open }"
        class="w-5 h-5 transition-transform"
        fill="none"
        stroke="currentColor"
        viewBox="0 0 24 24"
      >
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
      </svg>
    </button>
    <div x-show="open" x-collapse class="p-4 border-t" style="display: none;">
      <p>라거, 페일에일, IPA 등이 치킨과 잘 어울립니다.</p>
    </div>
  </div>
</div>
```

### 3. 갤러리 (Gallery)

**용도**: 이미지 갤러리

**생성 코드**:
```html
<div x-data="{ selected: 0, images: ['/image1.jpg', '/image2.jpg', '/image3.jpg'] }" class="my-8">
  <!-- 메인 이미지 -->
  <div class="relative aspect-video bg-muted rounded-lg overflow-hidden mb-4">
    <img
      :src="images[selected]"
      alt="갤러리 이미지"
      class="w-full h-full object-cover"
    >
  </div>
  
  <!-- 썸네일 -->
  <div class="grid grid-cols-3 gap-2">
    <template x-for="(image, index) in images" :key="index">
      <button
        x-on:click="selected = index"
        :class="{ 'ring-2 ring-primary': selected === index }"
        class="aspect-video bg-muted rounded-lg overflow-hidden"
      >
        <img
          :src="image"
          alt="썸네일"
          class="w-full h-full object-cover"
        >
      </button>
    </template>
  </div>
</div>
```

### 4. 콜아웃 (Callout)

**용도**: 중요 정보 강조

**생성 코드**:
```html
<!-- 정보 콜아웃 -->
<div class="my-6 p-4 bg-blue-50 border-l-4 border-blue-500 rounded-r-lg">
  <div class="flex items-start">
    <svg class="w-5 h-5 text-blue-500 mt-0.5 mr-3" fill="currentColor" viewBox="0 0 20 20">
      <path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z" clip-rule="evenodd" />
    </svg>
    <div>
      <h4 class="font-semibold text-blue-900 mb-1">알아두세요!</h4>
      <p class="text-blue-800 text-sm">맥주는 4-6도로 차갑게 마시는 것이 가장 맛있습니다.</p>
    </div>
  </div>
</div>

<!-- 경고 콜아웃 -->
<div class="my-6 p-4 bg-amber-50 border-l-4 border-amber-500 rounded-r-lg">
  <div class="flex items-start">
    <svg class="w-5 h-5 text-amber-500 mt-0.5 mr-3" fill="currentColor" viewBox="0 0 20 20">
      <path fill-rule="evenodd" d="M8.257 3.099c.765-1.36 2.722-1.36 3.486 0l5.58 9.92c.75 1.334-.213 2.98-1.742 2.98H4.42c-1.53 0-2.493-1.646-1.743-2.98l5.58-9.92zM11 13a1 1 0 11-2 0 1 1 0 012 0zm-1-8a1 1 0 00-1 1v3a1 1 0 002 0V6a1 1 0 00-1-1z" clip-rule="evenodd" />
    </svg>
    <div>
      <h4 class="font-semibold text-amber-900 mb-1">주의하세요!</h4>
      <p class="text-amber-800 text-sm">과도한 음주는 건강에 해롭습니다.</p>
    </div>
  </div>
</div>
```


### 5. 인용구 (Quote)

**용도**: 강조된 인용구

**생성 코드**:
```html
<blockquote class="my-8 pl-6 border-l-4 border-primary italic text-lg text-muted-foreground">
  "맥주와 음식의 완벽한 조화는 미식의 정점입니다."
  <footer class="mt-2 text-sm not-italic text-foreground">
    — 맥주 소믈리에 김철수
  </footer>
</blockquote>
```

---

## 예시 코드

### 완전한 블로그 글 예시

```html
<article class="max-w-4xl mx-auto px-4 py-8">
  <!-- 제목 -->
  <h1 class="text-4xl font-bold mb-4">치킨과 맥주의 완벽한 페어링 가이드</h1>
  
  <!-- 메타 정보 -->
  <div class="flex items-center gap-4 text-sm text-muted-foreground mb-8">
    <span>2025년 1월 12일</span>
    <span>•</span>
    <span>5분 읽기</span>
  </div>
  
  <!-- 인트로 -->
  <p class="text-lg leading-relaxed mb-6">
    치킨과 맥주는 한국에서 가장 사랑받는 조합입니다. 
    하지만 어떤 맥주가 어떤 치킨과 잘 어울리는지 아시나요?
  </p>
  
  <!-- 콜아웃 -->
  <div class="my-6 p-4 bg-blue-50 border-l-4 border-blue-500 rounded-r-lg">
    <div class="flex items-start">
      <svg class="w-5 h-5 text-blue-500 mt-0.5 mr-3" fill="currentColor" viewBox="0 0 20 20">
        <path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z" clip-rule="evenodd" />
      </svg>
      <div>
        <h4 class="font-semibold text-blue-900 mb-1">이 글에서 배울 내용</h4>
        <p class="text-blue-800 text-sm">치킨 종류별 최적의 맥주 페어링을 알아봅니다.</p>
      </div>
    </div>
  </div>
  
  <!-- 탭 컴포넌트 -->
  <div x-data="{ activeTab: 'fried' }" class="my-8">
    <div class="flex space-x-1 bg-muted p-1 rounded-lg">
      <button
        x-on:click="activeTab = 'fried'"
        :class="{ 'bg-background text-primary shadow-sm': activeTab === 'fried', 'text-muted-foreground hover:bg-background/50': activeTab !== 'fried' }"
        class="flex-1 px-4 py-3 rounded-md transition-all duration-200"
      >
        후라이드
      </button>
      <button
        x-on:click="activeTab = 'yangnyeom'"
        :class="{ 'bg-background text-primary shadow-sm': activeTab === 'yangnyeom', 'text-muted-foreground hover:bg-background/50': activeTab !== 'yangnyeom' }"
        class="flex-1 px-4 py-3 rounded-md transition-all duration-200"
      >
        양념치킨
      </button>
      <button
        x-on:click="activeTab = 'garlic'"
        :class="{ 'bg-background text-primary shadow-sm': activeTab === 'garlic', 'text-muted-foreground hover:bg-background/50': activeTab !== 'garlic' }"
        class="flex-1 px-4 py-3 rounded-md transition-all duration-200"
      >
        마늘치킨
      </button>
    </div>
    
    <div x-show="activeTab === 'fried'" class="p-6 border rounded-lg mt-2">
      <h3 class="text-xl font-bold mb-3">후라이드 치킨 × 라거</h3>
      <p class="mb-4">깔끔한 후라이드 치킨에는 시원한 라거가 최고입니다.</p>
      <ul class="list-disc list-inside space-y-2 text-muted-foreground">
        <li>추천 맥주: 테라, 카스, 하이네켄</li>
        <li>온도: 4-6도</li>
        <li>특징: 탄산이 기름기를 중화</li>
      </ul>
    </div>
    
    <div x-show="activeTab === 'yangnyeom'" class="p-6 border rounded-lg mt-2" style="display: none;">
      <h3 class="text-xl font-bold mb-3">양념치킨 × 페일에일</h3>
      <p class="mb-4">달콤한 양념에는 홉향이 강한 페일에일이 잘 어울립니다.</p>
      <ul class="list-disc list-inside space-y-2 text-muted-foreground">
        <li>추천 맥주: 세븐브로이, 제주맥주 펠롱</li>
        <li>온도: 8-10도</li>
        <li>특징: 홉의 쓴맛이 단맛을 균형있게</li>
      </ul>
    </div>
    
    <div x-show="activeTab === 'garlic'" class="p-6 border rounded-lg mt-2" style="display: none;">
      <h3 class="text-xl font-bold mb-3">마늘치킨 × 밀맥주</h3>
      <p class="mb-4">강한 마늘향에는 부드러운 밀맥주가 조화롭습니다.</p>
      <ul class="list-disc list-inside space-y-2 text-muted-foreground">
        <li>추천 맥주: 호가든, 파울라너</li>
        <li>온도: 6-8도</li>
        <li>특징: 밀의 부드러움이 마늘향을 감싸줌</li>
      </ul>
    </div>
  </div>
  
  <!-- 인용구 -->
  <blockquote class="my-8 pl-6 border-l-4 border-primary italic text-lg text-muted-foreground">
    "치킨과 맥주의 조합은 단순한 음식이 아닌, 문화입니다."
    <footer class="mt-2 text-sm not-italic text-foreground">
      — 맥주 소믈리에 김철수
    </footer>
  </blockquote>
  
  <!-- 결론 -->
  <h2 class="text-2xl font-bold mb-4 mt-12">결론</h2>
  <p class="leading-relaxed mb-6">
    치킨의 종류에 따라 최적의 맥주가 다릅니다. 
    이 가이드를 참고하여 더욱 맛있는 치맥을 즐겨보세요!
  </p>
</article>
```


---

## Admin 페이지 사용법

### 1. 관리자 로그인

```
URL: https://www.soolomon.com/admin/login
권한: editor_permission = 'html_editor'
```

### 2. 콘텐츠 작성 페이지 접근

```
URL: https://www.soolomon.com/admin/contents/new
```

### 3. HTML 에디터 사용

**에디터 화면**:
```
┌─────────────────────────────────────────────────────────┐
│  [제목 입력]                                             │
├─────────────────────────────────────────────────────────┤
│  [카테고리 선택] [태그 입력]                             │
├─────────────────────────────────────────────────────────┤
│  HTML 에디터 (Tiptap)                                    │
│  ┌─────────────────────────────────────────────────┐   │
│  │ [B] [I] [U] [링크] [이미지] [코드] [HTML]       │   │
│  ├─────────────────────────────────────────────────┤   │
│  │                                                  │   │
│  │  여기에 AI 생성 HTML을 붙여넣으세요             │   │
│  │                                                  │   │
│  └─────────────────────────────────────────────────┘   │
├─────────────────────────────────────────────────────────┤
│  [미리보기] [저장] [발행]                                │
└─────────────────────────────────────────────────────────┘
```

### 4. AI 생성 HTML 붙여넣기

**단계**:
1. AI 콘텐츠 생성기에서 HTML 생성
2. 생성된 HTML 복사
3. Tiptap 에디터에 붙여넣기 (Ctrl+V)
4. 미리보기로 확인
5. 필요시 수동 편집
6. 저장 또는 발행

### 5. 서버 측 검증

**저장 버튼 클릭 시**:
```typescript
// 1. 클라이언트에서 HTML 전송
POST /api/content/validate-html
{
  "html": "<div x-data=\"{ open: false }\">...</div>",
  "userId": "admin-user-id"
}

// 2. 서버에서 검증
- DOMPurify HTML Sanitization
- Alpine.js 표현식 패턴 검증
- XSS 방지 체크

// 3. 검증 결과 반환
{
  "isValid": true,
  "sanitizedHtml": "<div x-data=\"{ open: false }\">...</div>",
  "errors": []
}

// 4. 데이터베이스 저장
INSERT INTO contents (title, html, user_id, status)
VALUES ('제목', '검증된 HTML', 'admin-user-id', 'published')

// 5. 감사 로그 기록
INSERT INTO content_edit_logs (user_id, editor_type, action, html_snippet)
VALUES ('admin-user-id', 'html', 'create', '검증된 HTML')
```

### 6. 발행 후 확인

**프론트엔드 URL**:
```
https://www.soolomon.com/content/[slug]
```

**렌더링 과정**:
```
1. Next.js가 globals.css 로드 (Tailwind 포함)
2. Next.js가 Alpine.js 로드
3. 콘텐츠 HTML 렌더링
4. Alpine.js가 x-data, x-show 등 처리
5. 인터랙티브 기능 작동
```

---

## 검증 및 테스트

### 1. 로컬 테스트

**HTML 파일 생성**:
```html
<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="UTF-8">
  <title>테스트</title>
  <script src="https://cdn.tailwindcss.com"></script>
  <script defer src="https://cdn.jsdelivr.net/npm/alpinejs@3.x.x/dist/cdn.min.js"></script>
</head>
<body class="p-8">
  <!-- 여기에 생성한 HTML 붙여넣기 -->
  <div x-data="{ activeTab: 'tab1' }" class="my-8">
    <!-- ... -->
  </div>
</body>
</html>
```

**브라우저에서 확인**:
- 스타일이 제대로 적용되는지
- 인터랙션이 작동하는지
- 콘솔 에러가 없는지

### 2. 검증 체크리스트

**HTML 구조**:
- [ ] `<style>` 태그 없음
- [ ] `<script>` 태그 없음
- [ ] 인라인 스타일 최소화 (display:none만 허용)
- [ ] 시맨틱 HTML 사용

**Tailwind CSS**:
- [ ] 모든 스타일이 Tailwind 클래스로 작성됨
- [ ] CSS Variables 사용 (var(--primary) 등)
- [ ] 반응형 클래스 사용 (sm:, md:, lg:)

**Alpine.js**:
- [ ] x-data 초기화 올바름
- [ ] x-show, x-on:click 등 올바르게 사용
- [ ] :class 동적 클래스 올바름
- [ ] 초기 숨김 요소에 style="display: none;" 추가

**보안**:
- [ ] XSS 위험 요소 없음
- [ ] 외부 스크립트 로드 없음
- [ ] 위험한 이벤트 핸들러 없음 (onerror, onload)

### 3. 일반적인 오류

**오류 1: Alpine.js 작동 안 함**
```html
<!-- ❌ 잘못된 예 -->
<div x-data="{ open: true }">
  <div x-show="open">내용</div>  <!-- 초기에 보여야 하는데 안 보임 -->
</div>

<!-- ✅ 올바른 예 -->
<div x-data="{ open: true }">
  <div x-show="open">내용</div>  <!-- 초기에 보임 -->
</div>

<div x-data="{ open: false }">
  <div x-show="open" style="display: none;">내용</div>  <!-- 초기에 숨김 -->
</div>
```

**오류 2: Tailwind 클래스 작동 안 함**
```html
<!-- ❌ 잘못된 예 -->
<div class="my-custom-class">내용</div>  <!-- 정의되지 않은 클래스 -->

<!-- ✅ 올바른 예 -->
<div class="bg-primary text-white p-4">내용</div>  <!-- Tailwind 클래스 -->
```

**오류 3: 중첩된 x-data**
```html
<!-- ❌ 잘못된 예 -->
<div x-data="{ outer: true }">
  <div x-data="{ inner: true }">  <!-- 중첩 가능하지만 복잡함 -->
    <div x-show="outer && inner">내용</div>  <!-- outer 접근 불가 -->
  </div>
</div>

<!-- ✅ 올바른 예 -->
<div x-data="{ outer: true, inner: true }">
  <div x-show="outer && inner">내용</div>
</div>
```

---

## 추가 리소스

### 참고 문서
- **Tailwind CSS**: https://tailwindcss.com/docs
- **Alpine.js**: https://alpinejs.dev/
- **Soolomon 디자인 시스템**: `soolomon-project/src/app/globals.css`

### 문의
- **기술 문의**: 프로젝트 관리자
- **보안 문의**: 보안 담당자
- **PRD 문서**: `soolomon-project/.kiro/specs/CONTENT_EDITOR_SECURITY_PRD.md`

---

**작성자**: Kiro AI  
**최종 업데이트**: 2025-01-12  
**버전**: 1.0
