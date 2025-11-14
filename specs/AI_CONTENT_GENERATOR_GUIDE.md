# AI 콘텐츠 자동 생성기 개발 가이드

**대상**: HTML 콘텐츠 자동 생성기 개발자  
**작성일**: 2025-11-14  
**버전**: 1.1 (컴포넌트 Blueprint 업데이트)

---

## 📋 목차

1. [개요](#개요)
2. [에디터 아키텍처](#에디터-아키텍처)
3. [HTML 생성 규칙](#html-생성-규칙)
4. [사용 가능한 컴포넌트](#사용-가능한-컴포넌트)
5. [Admin 페이지 사용법](#admin-페이지-사용법)
6. [검증 및 테스트](#검증-및-테스트)
7. [추가 리소스](#추가-리소스)

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

AI는 아래 정의된 컴포넌트들의 HTML 구조와 규칙을 완벽하게 준수하여 최종 HTML 스니펫을 생성해야 합니다. 각 컴포넌트의 주석을 통해 상세한 사용법과 AI가 채워야 할 데이터 필드를 확인하세요.

<!--
  Component: CalloutBlock (개정판 Blueprint)
  Description: 4가지 타입(info, success, warning, error, quote)의 텍스트 강조 박스입니다.
  AI는 아래 4가지 예시 중 맥락에 맞는 HTML 스니펫을 생성해야 합니다.
  SVG 아이콘 경로는 remixicon.com 또는 유사 아이콘 라이브러리(Phosphor 등)를 참조합니다.
-->

<!-- 
  [AI 생성 예시 1: type="info" (정보)]
  - globals.css의 'info' 상태 색상 (bg-info-bg, border-info, text-info-text) [cite: globals.css]를 사용합니다.
-->
<div 
  class="soolomon-component my-6 p-4 border-l-4 rounded-r-lg bg-info-bg border-info animate-fadeIn" 
  data-component="CalloutBlock" 
  data-type="info"
>
  <div class="flex items-start">
    <svg class="w-5 h-5 text-info mt-0.5 mr-3 flex-shrink-0" fill="currentColor" viewBox="0 0 20 20">
      <path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z" clip-rule="evenodd" />
    </svg>
    <div class="prose prose-sm max-w-none text-info-text">
      <!-- AI가 여기에 'title'과 'content'를 채웁니다 -->
      <h4 class_comment="!text-inherit" 
          class="font-semibold mb-1 !mt-0 !text-inherit">알아두세요!</h4>
      <p class="!text-inherit">맥주는 4-6도로 마시는 것이 가장 맛있습니다.</p>
    </div>
  </div>
</div>

<!-- 
  [AI 생성 예시 2: type="success" (성공/팁)]
  - globals.css의 'success' 상태 색상 (bg-success-bg, border-success, text-success-text) [cite: globals.css]를 사용합니다.
-->
<div 
  class="soolomon-component my-6 p-4 border-l-4 rounded-r-lg bg-success-bg border-success animate-fadeIn" 
  data-component="CalloutBlock" 
  data-type="success"
>
  <div class="flex items-start">
    <svg class="w-5 h-5 text-success mt-0.5 mr-3 flex-shrink-0" fill="currentColor" viewBox="0 0 20 20">
      <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd" />
    </svg>
    <div class="prose prose-sm max-w-none text-success-text">
      <h4 class="font-semibold mb-1 !mt-0 !text-inherit">K-언니의 비밀 팁</h4>
      <p class="!text-inherit">불닭볶음면에 마요네즈를 섞으면 완벽한 '불닭 마요'가 됩니다.</p>
    </div>
  </div>
</div>

<!-- 
  [AI 생성 예시 3: type="warning" (경고)]
  - globals.css의 'warning' 상태 색상 (bg-warning-bg, border-warning, text-warning-text) [cite: globals.css]를 사용합니다.
-->
<div 
  class="soolomon-component my-6 p-4 border-l-4 rounded-r-lg bg-warning-bg border-warning animate-fadeIn" 
  data-component="CalloutBlock" 
  data-type="warning"
>
  <div class="flex items-start">
    <svg class="w-5 h-5 text-warning mt-0.5 mr-3 flex-shrink-0" fill="currentColor" viewBox="0 0 20 20">
      <path fill-rule="evenodd" d="M8.257 3.099c.765-1.36 2.722-1.36 3.486 0l5.58 9.92c.75 1.334-.213 2.98-1.742 2.98H4.42c-1.53 0-2.493-1.646-1.743-2.98l5.58-9.92zM11 13a1 1 0 11-2 0 1 1 0 012 0zm-1-8a1 1 0 00-1 1v3a1 1 0 002 0V6a1 1 0 00-1-1z" clip-rule="evenodd" />
    </svg>
    <div class="prose prose-sm max-w-none text-warning-text">
      <h4 class="font-semibold mb-1 !mt-0 !text-inherit">주의하세요!</h4>
      <p class="!text-inherit">과도한 음주는 건강에 해롭습니다.</p>
    </div>
  </div>
</div>

<!-- 
  [AI 생성 예시 4: type="quote" (인용)]
  - globals.css의 'primary' [cite: globals.css] 색상을 border-color로 사용합니다.
-->
<blockquote 
  class="soolomon-component my-8 pl-6 border-l-4 border-primary italic text-lg text-muted-foreground animate-fadeIn"
  data-component="CalloutBlock" 
  data-type="quote"
>
  <!-- AI가 여기에 인용구와 footer를 채웁니다 -->
  <p>"맥주와 음식의 완벽한 조화는 미식의 정점입니다."</p>
  <footer class="mt-2 text-sm not-italic text-foreground">
    — 맥주 소믈리에 김철수
  </footer>
</blockquote>

<!--
  Component: ComparisonTable (개정판 Blueprint)
  Description: 데이터 비교표를 생성합니다.
  AI는 이 HTML 구조를 생성하고, 'headers'와 'rows' 데이터를 채워넣어야 합니다.
  (AI must generate this HTML structure and populate the 'headers' and 'rows' data)
-->

<!-- 
  [AI 생성 예시]
  - AI가 'table' 객체(headers, rows)를 기반으로 아래와 같은 순수 HTML을 생성합니다.
-->
<div 
  class="soolomon-component my-8 animate-fadeIn" 
  data-component="ComparisonTable"
>
  <div class="rounded-lg border border-border overflow-hidden">
    <!-- 모바일 반응형을 위한 가로 스크롤 컨테이너 -->
    <div class="overflow-x-auto">
      <table class="w-full min-w-[600px] text-left border-collapse">
        <!-- 테이블 헤더 -->
        <thead class="bg-muted">
          <tr>
            <th class="p-4 text-sm font-semibold text-foreground tracking-wider">
              구분
            </th>
            <th class="p-4 text-sm font-semibold text-foreground tracking-wider">
              라거 (Lager)
            </th>
            <th class="p-4 text-sm font-semibold text-foreground tracking-wider">
              에일 (Ale)
            </th>
          </tr>
        </thead>
        <!-- 테이블 바디 -->
        <tbody class="bg-background">
          <tr class="border-b border-border last:border-b-0">
            <td class="p-4 text-muted-foreground font-medium">
              특징
            </td>
            <td class="p-4 text-foreground">
              깔끔하고 청량함
            </td>
            <td class="p-4 text-foreground">
              풍부한 향과 묵직함
            </td>
          </tr>
          <tr class="border-b border-border last:border-b-0">
            <td class="p-4 text-muted-foreground font-medium">
              발효 방식
            </td>
            <td class="p-4 text-foreground">
              하면 발효 (저온)
            </td>
            <td class="p-4 text-foreground">
              상면 발효 (고온)
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</div>

<!--
  Component: CrewComparison (개정판 Blueprint)
  Description: 전문가 2인(아마라, 홍설화)을 비교하는 2단 그리드입니다.
  AI는 이 HTML 구조를 생성하고, <div class="prose..."> 내부에 각 크루의 코멘트를 채워넣어야 합니다.
-->
<div 
  class="soolomon-component my-10 animate-fadeIn" 
  data-component="CrewComparison"
>
  <h3 class="text-2xl font-bold text-foreground mb-6 text-center">
    The Crew's Choice
  </h3>
  
  <div class="grid md:grid-cols-2 gap-6">
    <!-- 왼쪽: 아마라 (Data Pick) -->
    <div 
      class_comment="bg-secondary/10 border-secondary/20 [globals.css], hover-lift [animations.css]"
      class="relative bg-secondary/10 border border-secondary/20 rounded-xl p-6 hover-lift animate-slideUp"
    >
      <div class_comment="bg-secondary text-secondary-foreground [globals.css]"
           class="absolute -top-4 left-6 bg-secondary text-secondary-foreground px-3 py-1 rounded-full text-xs font-bold uppercase tracking-wide shadow-md">
        Amara's Data Pick
      </div>
      <div class="mt-2">
        <div class="flex items-center mb-4">
          <div class="w-10 h-10 bg-secondary/20 rounded-full flex items-center justify-center mr-3">
            <i class="ri-bar-chart-box-line text-secondary text-xl"></i>
          </div>
          <div>
            <h4 class_comment="text-secondary [globals.css]"
                class="font-bold text-secondary">대중적인 선택</h4>
            <p class="text-xs text-muted-foreground">실패 확률 0% 검증된 데이터</p>
          </div>
        </div>
        <div class="prose prose-sm text-foreground/80 leading-relaxed">
          <!-- AI가 여기에 아마라의 코멘트를 채웁니다 -->
          <p>"제 분석 결과, 이 조합의 만족도는 92.4%입니다. 실패 없는 선택을 원한다면 이것이 정답입니다."</p>
        </div>
      </div>
    </div>

    <!-- 오른쪽: 홍설화 (Artist's Pick) -->
    <div 
      class_comment="bg-primary/10 border-primary/20 [globals.css], hover-lift [animations.css]"
      class="relative bg-primary/10 border border-primary/20 rounded-xl p-6 hover-lift animate-slideUp" 
      style="animation-delay: 0.1s;"
    >
      <div class_comment="bg-primary text-primary-foreground [globals.css]"
           class="absolute -top-4 right-6 bg-primary text-primary-foreground px-3 py-1 rounded-full text-xs font-bold uppercase tracking-wide shadow-md">
        Seolhwa's Art Pick
      </div>
      <div class="mt-2">
        <div class="flex items-center mb-4 justify-end">
          <div class="text-right mr-3">
            <h4 class_comment="text-primary-hover [globals.css]"
                class="font-bold text-amber-600">특별한 영감</h4>
            <p class="text-xs text-muted-foreground">영혼을 울리는 페어링</p>
          </div>
          <div class="w-10 h-10 bg-primary/20 rounded-full flex items-center justify-center">
            <i class="ri-brush-line text-amber-600 text-xl"></i>
          </div>
        </div>
        <div class="prose prose-sm text-foreground/80 leading-relaxed text-right">
          <!-- AI가 여기에 홍설화의 코멘트를 채웁니다 -->
          <p>"재미없게. 틀을 깨 보세요. 이 와인의 영혼이 당신의 미각과 만나는 순간, 완전히 새로운 차원의 경험이 열릴 겁니다."</p>
        </div>
      </div>
    </div>
  </div>
</div>

<!--
  Component: ImageGallery (개정판 Blueprint)
  Description: 이미지 슬라이더 또는 비디오 플레이어를 생성합니다.
  AI는 아래 두 가지 타입(image, video) 중 하나의 HTML 스니펫을 생성해야 합니다.
-->

<!-- 
  [AI 생성 예시 1: type="image"] (Alpine.js 기반)
  - AI_CONTENT_GENERATOR_GUIDE.md [cite: AI_CONTENT_GENERATOR_GUIDE.md]의 "3. 갤러리" 로직을 100% 준수합니다.
  - AI가 'images' 배열에 이미지 URL을 채워넣어야 합니다.
-->
<div 
  class="soolomon-component my-8 animate-fadeIn" 
  data-component="ImageGallery" 
  data-type="image"
  x-data="{ 
    selected: 0, 
    images: [
      'https://placehold.co/600x400/FFBF00/191970?text=Image+1', 
      'https://placehold.co/600x400/191970/FFBF00?text=Image+2', 
      'https://placehold.co/600x400/f3f4f6/333?text=Image+3'
    ] 
  }"
>
  <!-- 메인 이미지 -->
  <div class="relative aspect-video bg-muted rounded-xl overflow-hidden mb-2 shadow-lg">
    <!-- 루프 대신 x-show를 사용한 동적 이미지 표시 -->
    <template x-for="(image, index) in images" :key="index">
      <img
        x-show="selected === index"
        :src="image"
        alt="갤러리 메인 이미지"
        class="absolute inset-0 w-full h-full object-cover transition-opacity duration-300"
        x-transition:enter="transition ease-out duration-300"
        x-transition:enter-start="opacity-0"
        x-transition:enter-end="opacity-100"
        x-transition:leave="transition ease-in duration-300"
        x-transition:leave-start="opacity-100"
        x-transition:leave-end="opacity-0"
        style="display: none;"
      >
    </template>
    <!-- 이전/다음 버튼 -->
    <button 
      x-on:click="selected = (selected - 1 + images.length) % images.length"
      class="absolute left-3 top-1/2 -translate-y-1/2 bg-background/50 text-foreground hover:bg-background/80 p-2 rounded-full transition-all"
    >
      <i class="ri-arrow-left-s-line h-5 w-5"></i>
    </button>
    <button 
      x-on:click="selected = (selected + 1) % images.length"
      class="absolute right-3 top-1/2 -translate-y-1/2 bg-background/50 text-foreground hover:bg-background/80 p-2 rounded-full transition-all"
    >
      <i class="ri-arrow-right-s-line h-5 w-5"></i>
    </button>
  </div>
  
  <!-- 썸네일 -->
  <div class="grid grid-cols-5 gap-2">
    <template x-for="(image, index) in images" :key="index">
      <button
        x-on:click="selected = index"
        :class="{ 'ring-2 ring-primary ring-offset-2': selected === index, 'opacity-60 hover:opacity-100': selected !== index }"
        class="aspect-video bg-muted rounded-lg overflow-hidden transition-all duration-200"
      >
        <img
          :src="image"
          alt="갤러리 썸네일"
          class="w-full h-full object-cover"
        >
      </button>
    </template>
  </div>
</div>

<!-- 
  [AI 생성 예시 2: type="video"]
  - 반응형 16:9 비율(aspect-video)을 유지하는 <iframe> 래퍼입니다.
  - AI가 'videoUrl'을 채워넣어야 합니다. (예: YouTube embed URL)
-->
<div 
  class="soolomon-component my-8 animate-fadeIn" 
  data-component="ImageGallery" 
  data-type="video"
>
  <div class="aspect-video w-full relative">
    <iframe 
      class="absolute inset-0 w-full h-full rounded-xl shadow-lg" 
      src="https://www.youtube.com/embed/dQw4w9WgXcQ" 
      title="YouTube video player" 
      frameborder="0" 
      allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" 
      allowfullscreen
    >
    </iframe>
  </div>
</div>

<!--
  Component: InteractiveTabs (개정판 Blueprint)
  Description: Alpine.js를 사용하는 탭 컴포넌트입니다.
  AI는 'activeTab'의 초기값('tab1')을 설정하고,
  버튼과 패널의 ID('tab1', 'tab2'...)를 일치시켜
  아래와 같은 순수 HTML 스니펫을 생성해야 합니다.
  (AI must generate this exact HTML snippet structure)
-->
<div 
  class="soolomon-component my-8" 
  data-component="InteractiveTabs"
  x-data="{ activeTab: 'tab1' }"
>
  <!-- 탭 헤더 (네비게이션) -->
  <div class_comment="bg-muted p-1 rounded-lg [globals.css]">
    <div class="flex space-x-1 bg-muted p-1 rounded-lg mb-6 overflow-x-auto">
      <!-- 탭 1 버튼 -->
      <button
        x-on:click="activeTab = 'tab1'"
        :class="{ 
          'bg-background text-primary shadow-sm': activeTab === 'tab1', 
          'text-muted-foreground hover:bg-background/50': activeTab !== 'tab1' 
        }"
        class_comment="bg-background text-primary [globals.css]"
        class="flex-1 flex items-center justify-center space-x-2 px-4 py-3 rounded-md transition-all duration-200 text-sm font-medium whitespace-nowrap"
      >
        <span>재료</span>
      </button>
      
      <!-- 탭 2 버튼 -->
      <button
        x-on:click="activeTab = 'tab2'"
        :class="{ 
          'bg-background text-primary shadow-sm': activeTab === 'tab2', 
          'text-muted-foreground hover:bg-background/50': activeTab !== 'tab2' 
        }"
        class="flex-1 flex items-center justify-center space-x-2 px-4 py-3 rounded-md transition-all duration-200 text-sm font-medium whitespace-nowrap"
      >
        <span>레시피</span>
      </button>
    </div>
  </div>

  <!-- 탭 콘텐츠 -->
  <div class_comment="border-border rounded-xl [globals.css]">
    <div class="bg-background border border-border rounded-xl p-6 shadow-sm min-h-[200px]">
      <!-- 탭 1 패널 -->
      <div 
        x-show="activeTab === 'tab1'" 
        class_comment="animate-fadeIn [animations.css]"
        class="prose prose-lg max-w-none text-foreground animate-fadeIn"
      >
        <p>탭 1 (재료)의 내용입니다. AI가 여기에 실제 콘텐츠를 채웁니다.</p>
      </div>
      
      <!-- 탭 2 패널 -->
      <div 
        x-show="activeTab === 'tab2'" 
        class="prose prose-lg max-w-none text-foreground animate-fadeIn"
        style="display: none;"
      >
        <p>탭 2 (레시피)의 내용입니다. AI가 여기에 실제 콘텐츠를 채웁니다.</p>
      </div>
    </div>
  </div>
</div>

<!--
  Component: ListBlock (개정판 Blueprint)
  Description: 체크리스트 또는 단계별 가이드를 생성합니다.
  AI는 아래 두 가지 타입(check, step) 중 맥락에 맞는 HTML 스니펫을 생성해야 합니다.
  (AI must generate ONE of the following HTML snippets based on context)
-->

<!-- 
  [AI 생성 예시 1: type="check"]
  - globals.css의 'success' 상태 색상 (bg-success-bg, text-success-text) [cite: globals.css]을 사용합니다.
  - animations.css의 'animate-fadeIn' [cite: animations.css]을 적용합니다.
-->
<div class="soolomon-component my-8" data-component="ListBlock" data-type="check">
  <ul class="space-y-3">
    <!-- AI가 list.items 배열을 반복하여 아래 li를 생성 -->
    <li class="flex items-start p-4 bg-success-bg rounded-lg animate-fadeIn" style="animation-delay: 0.1s;">
      <div class="flex-shrink-0 w-6 h-6 flex items-center justify-center bg-success text-success-foreground rounded-full mr-3">
        <i class="ri-check-line h-4 w-4"></i>
      </div>
      <span class="text-success-text font-medium">여행용 돗자리 챙기기</span>
    </li>
    <li class="flex items-start p-4 bg-success-bg rounded-lg animate-fadeIn" style="animation-delay: 0.2s;">
      <div class="flex-shrink-0 w-6 h-6 flex items-center justify-center bg-success text-success-foreground rounded-full mr-3">
        <i class="ri-check-line h-4 w-4"></i>
      </div>
      <span class="text-success-text font-medium">보조 배터리 (필수!)</span>
    </li>
    <li class="flex items-start p-4 bg-success-bg rounded-lg animate-fadeIn" style="animation-delay: 0.3s;">
      <div class="flex-shrink-0 w-6 h-6 flex items-center justify-center bg-success text-success-foreground rounded-full mr-3">
        <i class="ri-check-line h-4 w-4"></i>
      </div>
      <span class="text-success-text font-medium">물티슈와 쓰레기 봉투</span>
    </li>
  </ul>
</div>

<!-- 
  [AI 생성 예시 2: type="step"]
  - globals.css의 'primary' 브랜드 색상 (bg-primary, text-primary-foreground) [cite: globals.css]을 사용합니다.
  - animations.css의 'animate-fadeIn' [cite: animations.css]을 적용합니다.
-->
<div class="soolomon-component my-8" data-component="ListBlock" data-type="step">
  <ol class="relative border-l border-border ml-3">
    <!-- AI가 list.items 배열을 반복하여 아래 li를 생성 -->
    <li class="mb-6 ml-6 animate-fadeIn" style="animation-delay: 0.1s;">
      <span class="absolute -left-3.5 flex items-center justify-center w-7 h-7 bg-primary text-primary-foreground rounded-full font-bold">
        1
      </span>
      <div class="p-4 bg-muted rounded-lg">
        <h5 class="text-md font-semibold text-foreground">앱 켜고 '배달' 선택</h5>
        <p class="text-sm text-muted-foreground">먼저 배달의민족 앱을 켭니다.</p>
      </div>
    </li>
    <li class="mb-6 ml-6 animate-fadeIn" style="animation-delay: 0.2s;">
      <span class="absolute -left-3.5 flex items-center justify-center w-7 h-7 bg-primary text-primary-foreground rounded-full font-bold">
        2
      </span>
      <div class="p-4 bg-muted rounded-lg">
        <h5 class="text-md font-semibold text-foreground">한강공원 주소 입력</h5>
        <p class="text-sm text-muted-foreground">현재 위치(예: 여의도 2주차장)를 정확히 입력합니다.</p>
      </div>
    </li>
    <li class="ml-6 animate-fadeIn" style="animation-delay: 0.3s;">
      <span class="absolute -left-3.5 flex items-center justify-center w-7 h-7 bg-primary text-primary-foreground rounded-full font-bold">
        3
      </span>
      <div class="p-4 bg-muted rounded-lg">
        <h5 class="text-md font-semibold text-foreground">주문 및 픽업</h5>
        <p class="text-sm text-muted-foreground">주문 후 배달원과 통화하여 픽업합니다.</p>
      </div>
    </li>
  </ol>
</div>

<!--
  Component: MediaCard (개정판 Blueprint)
  Description: 제품, 레시피, 장소 등을 소개하는 카드입니다.
  AI는 'type'에 따라 'product' 또는 'recipe' HTML 스니펫을 생성해야 합니다.
-->

<!-- 
  [AI 생성 예시 1: type="product"]
  - 'card.price', 'card.description' 데이터를 채웁니다.
  - 'bg-secondary' [cite: globals.css] 뱃지를 사용합니다.
-->
<div 
  class="soolomon-component group relative bg-card border border-border rounded-xl overflow-hidden shadow-lg hover-lift animate-fadeIn" 
  data-component="MediaCard"
  data-type="product"
>
  <div class="relative overflow-hidden">
    <img
      src="https://placehold.co/400x300/191970/FFBF00?text=Soolomon+Wine"
      alt="카베르네 소비뇽 2018"
      class_comment="group-hover:scale-110 [animations.css]"
      class="w-full h-48 object-cover group-hover:scale-110 transition-transform duration-300"
    />
    <div class="absolute top-3 left-3">
      <span class_comment="bg-secondary text-secondary-foreground [globals.css]"
            class="bg-secondary text-secondary-foreground px-3 py-1 rounded-full text-xs font-bold uppercase tracking-wide">
        Product
      </span>
    </div>
  </div>
  
  <div class="p-5">
    <h4 class_comment="group-hover:text-primary [globals.css]"
        class="text-xl font-bold text-foreground mb-2 group-hover:text-primary transition-colors line-clamp-2">
      카베르네 소비뇽 2018
    </h4>
    <p class="text-lg font-semibold text-primary mb-3">₩120,000</p>
    <p class="text-sm text-muted-foreground line-clamp-3">
      나파 밸리 산, 풀바디 레드와인. 스테이크와 완벽한 조화를 이룹니다.
    </p>
  </div>
</div>

<!-- 
  [AI 생성 예시 2: type="recipe"]
  - 'card.time', 'card.difficulty' 데이터를 채웁니다.
  - 'bg-primary' [cite: globals.css] 뱃지를 사용합니다.
-->
<div 
  class="soolomon-component group relative bg-card border border-border rounded-xl overflow-hidden shadow-lg hover-lift animate-fadeIn" 
  data-component="MediaCard"
  data-type="recipe"
>
  <div class="relative overflow-hidden">
    <img
      src="https://placehold.co/400x300/FFBF00/191970?text=Soolomon+Recipe"
      alt="불닭 마요"
      class="w-full h-48 object-cover group-hover:scale-110 transition-transform duration-300"
    />
    <div class="absolute top-3 left-3">
      <span class_comment="bg-primary text-primary-foreground [globals.css]"
            class="bg-primary text-primary-foreground px-3 py-1 rounded-full text-xs font-bold uppercase tracking-wide">
        Recipe
      </span>
    </div>
  </div>
  
  <div class="p-5">
    <h4 class="text-xl font-bold text-foreground mb-2 group-hover:text-primary transition-colors line-clamp-2">
      불닭 마요
    </h4>
    <div class="flex items-center space-x-4 text-muted-foreground mb-3">
      <span class="flex items-center text-sm">
        <i class="ri-time-line mr-1"></i>
        5분
      </span>
      <span class="flex items-center text-sm">
        <i class="ri-service-line mr-1"></i>
        하
      </span>
    </div>
    <p class="text-sm text-muted-foreground line-clamp-3">
      매운 불닭볶음면과 마요네즈의 환상적인 조합. K-편의점 꿀조합의 정석.
    </p>
  </div>
</div>

<!--
  Component: ProfileBlock (개정판 Blueprint)
  Description: 전문가 크루(아마라, 홍설화 등)의 인용문이나 서술을 표시합니다.
  AI는 아래 예시 중 맥락에 맞는 type의 HTML 스니펫을 생성해야 합니다.
-->

<!-- 
  [AI 생성 예시 1: type="amara"]
  - globals.css의 'secondary' 색상 (bg-secondary/10, text-secondary) [cite: globals.css]를 사용합니다.
  - 아마라(데이터)의 특성에 맞게 'ri-bar-chart-box-line' 아이콘을 사용합니다.
-->
<div class="soolomon-component my-8 animate-fadeIn" data-component="ProfileBlock" data-type="amara">
  <div class="p-6 bg-secondary/10 border border-secondary/20 rounded-xl">
    <div class="flex items-center space-x-3 mb-3">
      <div class="flex-shrink-0 w-10 h-10 flex items-center justify-center bg-secondary text-secondary-foreground rounded-full">
        <i class="ri-bar-chart-box-line text-xl"></i>
      </div>
      <div>
        <h5 class="font-bold text-foreground">아마라 (Amara)</h5>
        <p class="text-sm text-secondary font-medium">데이터 기반 '대중적인 선택'</p>
      </div>
    </div>
    <div class="prose prose-base text-muted-foreground">
      <p>
        "제 분석 결과, 이 조합의 만족도는 92.4%입니다. 
        대부분의 사용자가 이 안전한 조합에서 가장 높은 점수를 주었습니다. 
        실패 없는 선택을 원한다면 이것이 정답입니다."
      </p>
    </div>
  </div>
</div>

<!-- 
  [AI 생성 예시 2: type="seolhwa"]
  - globals.css의 'primary' 색상 (bg-primary/10, text-primary) [cite: globals.css]를 사용합니다.
  - 홍설화(예술)의 특성에 맞게 'ri-brush-line' 아이콘을 사용합니다.
-->
<div class="soolomon-component my-8 animate-fadeIn" data-component="ProfileBlock" data-type="seolhwa">
  <div class="p-6 bg-primary/10 border border-primary/20 rounded-xl">
    <div class="flex items-center space-x-3 mb-3">
      <div class="flex-shrink-0 w-10 h-10 flex items-center justify-center bg-primary text-primary-foreground rounded-full">
        <i class="ri-brush-line text-xl"></i>
      </div>
      <div>
        <h5 class="font-bold text-foreground">홍설화 (Seol-hwa)</h5>
        <p class="text-sm text-primary font-medium">예술적 직관 '특별한 추천'</p>
      </div>
    </div>
    <div class="prose prose-base text-muted-foreground">
      <p>
        "재미없게. 틀을 깨 보세요. 
        이 와인의 영혼이 당신의 미각과 만나는 순간, 
        완전히 새로운 차원의 경험이 열릴 겁니다. 데이터로는 설명할 수 없죠."
      </p>
    </div>
  </div>
</div>

<!--
  Component: ProsCons (개정판 Blueprint)
  Description: 장점과 단점을 나열하는 2열 그리드입니다.
  AI는 'pros'와 'cons' 배열을 기반으로 <li> 항목을 생성해야 합니다.
-->

<!-- 
  [AI 생성 예시]
  - AI가 'pros'와 'cons' 배열을 기반으로 <li> 항목을 생성합니다.
-->
<div 
  class="soolomon-component my-8 grid md:grid-cols-2 gap-6 animate-fadeIn" 
  data-component="ProsCons"
>
  <!-- 장점 (Pros) -->
  <div class="bg-success-bg/60 border border-success-bg rounded-xl p-6">
    <h5 class="flex items-center text-lg font-semibold text-success-text mb-4">
      <i class="ri-checkbox-circle-line mr-2 text-xl"></i>
      장점 (Pros)
    </h5>
    <ul class="space-y-2">
      <li class="flex items-start text-success-text">
        <i class="ri-check-line mr-2 mt-1 flex-shrink-0"></i>
        <span>뛰어난 청량감과 목넘김.</span>
      </li>
      <li class="flex items-start text-success-text">
        <i class="ri-check-line mr-2 mt-1 flex-shrink-0"></i>
        <span>어떤 음식과도 잘 어울리는 범용성.</span>
      </li>
    </ul>
  </div>

  <!-- 단점 (Cons) -->
  <div class="bg-error-bg/60 border border-error-bg rounded-xl p-6">
    <h5 class="flex items-center text-lg font-semibold text-error-text mb-4">
      <i class="ri-close-circle-line mr-2 text-xl"></i>
      단점 (Cons)
    </h5>
    <ul class="space-y-2">
      <li class="flex items-start text-error-text">
        <i class="ri-close-line mr-2 mt-1 flex-shrink-0"></i>
        <span>향이나 풍미가 다소 약할 수 있음.</span>
      </li>
    </ul>
  </div>
</div>

<!--
  Component: StarRating (개정판 Blueprint)
  Description: 시각적인 별점 점수를 표시합니다.
  AI는 'score'와 'max' 값을 기반으로, style="width: ...%" 값을 계산하여 생성해야 합니다.
-->

<!-- 
  [AI 생성 예시 (score: 4.3, max: 5)]
  - AI가 (4.3 / 5) * 100 = 86% 를 계산하여 'width: 86%'를 생성합니다.
-->
<div 
  class="soolomon-component my-4 flex items-center space-x-2" 
  data-component="StarRating"
>
  <!-- 별점 숫자 -->
  <span class="font-bold text-foreground text-lg">4.3</span>
  
  <!-- 별 아이콘 -->
  <div class="relative flex text-2xl text-muted">
    <!-- 
      배경 (빈 별 5개)
      - globals.css의 'muted' [cite: globals.css] 색상 사용
    -->
    <div class="flex">
      <i class="ri-star-fill"></i>
      <i class="ri-star-fill"></i>
      <i class="ri-star-fill"></i>
      <i class="ri-star-fill"></i>
      <i class="ri-star-fill"></i>
    </div>
    
    <!-- 
      전경 (채워진 별 5개)
      - globals.css의 'primary' [cite: globals.css] 색상 사용
      - 이 div의 'width'를 조절하여 별점을 표시합니다.
    -->
    <div 
      class="absolute top-0 left-0 h-full flex overflow-hidden text-primary" 
      style="width: 86%;" 
    >
      <div class="flex flex-nowrap">
        <i class="ri-star-fill flex-shrink-0"></i>
        <i class="ri-star-fill flex-shrink-0"></i>
        <i class="ri-star-fill flex-shrink-0"></i>
        <i class="ri-star-fill flex-shrink-0"></i>
        <i class="ri-star-fill flex-shrink-0"></i>
      </div>
    </div>
  </div>

  <!-- 최대 점수 (옵션) -->
  <span class="text-sm text-muted-foreground">(5점 만점)</span>
</div>

<!--
  Component: Timeline (개정판 Blueprint)
  Description: 시간 순서에 따른 이벤트(역사, 단계 등)를 표시합니다.
  AI는 'events' 배열을 기반으로 아래와 같은 순수 HTML을 생성해야 합니다.
  (AI must generate this HTML structure based on the 'events' array)
-->

<!-- 
  [AI 생성 예시]
  - AI가 'events' 배열을 기반으로 아래와 같은 순수 HTML을 생성합니다.
-->
<div 
  class="soolomon-component my-8 max-w-2xl mx-auto" 
  data-component="Timeline"
>
  <div class="relative">
    <!-- 타임라인 중앙선 -->
    <div 
      class="absolute left-3.5 top-0 h-full w-0.5"
      style="background-image: linear-gradient(to bottom, var(--primary) 30%, transparent 100%);"
    ></div>
    
    <ul class="space-y-8">
      <!-- 
        [AI 생성 예시 1: Event]
      -->
      <li class="flex items-start animate-slideUp" style="animation-delay: 0.1s;">
        <!-- 아이콘 -->
        <div class="flex-shrink-0 w-7 h-7 flex items-center justify-center bg-primary text-primary-foreground rounded-full z-10 mr-4 ring-4 ring-background">
          <i class="ri-calendar-event-line h-4 w-4"></i>
        </div>
        <!-- 내용 -->
        <div class="flex-1">
          <h5 class="text-primary font-bold text-lg">1990년</h5>
          <div class="p-4 bg-muted rounded-lg mt-1">
            <h6 class="font-semibold text-foreground">브랜드 탄생</h6>
            <p class="text-sm text-muted-foreground">Soolomon이 처음으로 맥주 페어링 서비스를 시작했습니다.</p>
          </div>
        </div>
      </li>
      
      <!-- [AI 생성 예시 2: Event] -->
      <li class="flex items-start animate-slideUp" style="animation-delay: 0.2s;">
        <!-- 아이콘 -->
        <div class="flex-shrink-0 w-7 h-7 flex items-center justify-center bg-primary text-primary-foreground rounded-full z-10 mr-4 ring-4 ring-background">
          <i class="ri-rocket-line h-4 w-4"></i>
        </div>
        <!-- 내용 -->
        <div class="flex-1">
          <h5 class="text-primary font-bold text-lg">2024년</h5>
          <div class="p-4 bg-muted rounded-lg mt-1">
            <h6 class="font-semibold text-foreground">PRD v2.0 런칭</h6>
            <p class="text-sm text-muted-foreground">AI 기반 리치 컴포넌트 아키텍처를 도입하여 고품질 콘텐츠 생성을 시작합니다.</p>
          </div>
        </div>
      </li>
    </ul>
  </div>
</div>

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