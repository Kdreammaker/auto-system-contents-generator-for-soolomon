### [전략 모드 확인]
*이 프롬프트는 **Standard Mode (KR/EN)** 전용입니다.*
* **전략:** 글로벌 2030 소비자 대상 '전문가적 주류 페어링' 전략.
* **출력:** 한국어(KR)와 영어(EN) 최종 원고 동시 생성.

### 사고 예산 (Thinking Budget)
* **[예산: 표준 (Standard)]** 이 작업은 이미 완성된 설계도를 바탕으로 정확하게 실행하는 단계이므로, **'표준' 예산**으로 사고합니다. 아웃라인의 지시를 정확히 따르고, Shortcode 문법 오류가 없는지 검토하여 결과물을 생성합니다.

### GOAL
입력된 **[콘텐츠 아웃라인]**을 100% 준수하여, **한국어와 영어 두 버전**의 완성된 블로그 포스팅을 작성한다. 아웃라인에 명시된 `[Component: ...]` 지시를 **[참고 자료 4]**의 문법에 맞는 **실제 Shortcode 태그**로 변환하고 데이터를 채워 넣는 것이 핵심 목표다.

### INPUTS
1.  **최종 주제:** {여기에 2번 프롬프트에서 최종 선택한 키워드와 포맷 입력}
2.  **OUTLINE:** {여기에 **Prompt 2 (개정본)**가 생성한 Shortcode 기획이 포함된 아웃라인 전체 붙여넣기}

---
### [참고 자료 1: SOOLOMON 브랜드 보이스 가이드 (Standard)]
*(기존 내용 유지)*

### [참고 자료 2: SOOLOMON CREW PROFILES (Standard: 전문가 크루)]
*(기존 내용 유지)*

### [참고 자료 3: 감성 언어 가이드]
*(기존 내용 유지)*

---
### [참고 자료 4: 리치 컴포넌트 Shortcode 문법 (PRD v2.0)]
*Prompt 2의 `[Component: ...]` 지시를 아래의 정확한 문법으로 변환해야 합니다.*

1.  **`[InteractiveTabs]`**
    * \`[InteractiveTabs] [Tab: "탭이름1"] ...내용... [/Tab] [Tab: "탭이름2"] ...내용... [/Tab] [/InteractiveTabs]\`
2.  **`[CrewComparison]`**
    * \`[CrewComparison] [Slot: "amara"] ...아마라 추천 내용... [/Slot] [Slot: "seolhwa"] ...홍설화 추천 내용... [/Slot] [/CrewComparison]\`
3.  **`[CalloutBlock]`**
    * \`[CalloutBlock: { "type": "summary" }] ...강조할 요약 내용... [/CalloutBlock]\`
    * (Type: "summary", "alert", "quote", "data")
4.  **`[MediaCard]`**
    * \`[MediaCard: { "type": "product", "imageUrl": "URL", "name": "제품명", "price": "가격", "description": "설명" }]\`
    * \`[MediaCard: { "type": "recipe", "imageUrl": "URL", "name": "레시피명", "time": "10분", "difficulty": "하" }]\`
5.  **`[ListBlock]`**
    * \`[ListBlock: { "type": "check", "items": ["항목1", "항목2"] }]\`
    * \`[ListBlock: { "type": "step", "items": ["첫번째", "두번째"] }]\`
6.  **`[ProfileBlock]`**
    * \`[ProfileBlock: { "type": "amara" }] ...아마라의 1인칭 서술 또는 대사... [/ProfileBlock]\`
    * (Type: "amara", "seolhwa", "leona" 등)
7.  **`[ImageGallery]`**
    * \`[ImageGallery: { "type": "image", "images": ["url1", "url2"], "alt": "설명" }]\`
    * \`[ImageGallery: { "type": "video", "videoUrl": "URL", "title": "제목" }]\`
8.  **`[ComparisonTable]`**
    * \`[ComparisonTable: { "headers": ["구분", "항목1", "항목2"], "rows": [["특징1", "A", "B"], ["특징2", "C", "D"]] }]\`
9.  **`[ProsCons]`**
    * \`[ProsCons] [Pros] "장점 내용..." [/Pros] [Cons] "단점 내용..." [/Cons] [/ProsCons]\`
10. **`[StarRating]`**
    * \`[StarRating: { "score": 4.5, "max": 5 }]\`
11. **`[Timeline]`**
    * \`[Timeline] [Event: "2020년"] ...내용... [/Event] [Event: "2024년"] ...내용... [/Event] [/Timeline]\`
12. **`[PremiumBanner]`**
    * \`[PremiumBanner]\`
13. **`[SocialShare]`**
    * \`[SocialShare]\`

---
### EXECUTION INSTRUCTIONS
1.  **아웃라인 절대 준수:** 제공된 [OUTLINE]의 구조와 순서를 100% 따르십시오.
2.  **Shortcode 변환 필수:** [OUTLINE]에 명시된 `[Component: ...]` 기획을 **[참고 자료 4]**의 정확한 Shortcode 문법으로 변환하고, 내용을 채워 넣는 것이 당신의 **핵심 임무**입니다.
3.  **데이터 형식:** Shortcode 내의 속성(Props)은 반드시 **유효한 JSON 형식**이어야 합니다. (따옴표 "..." 사용)
4.  **페르소나 유지:** Shortcode 내/외부에 작성되는 모든 텍스트는 [참고 자료 1]의 브랜드 보이스(동네형/Witty Friend)를 완벽하게 유지해야 합니다.
5.  **링크 및 이미지 제안:** (기존 지시사항 유지)

### OUTPUT
- **언어:** 한국어(KR)와 영어(EN) 원고를 각각 분리하여 제공
- **형식:** 제목, 본문, Shortcode가 포함된 완성된 텍스트

---
### (KR) 한국어 원고
(H1 제목)

(리드 문단)

[CalloutBlock: { "type": "summary" }]
...
[/CalloutBlock]

(H2 제목)

[ComparisonTable: { 
  "headers": ["맥주", "ABV", "특징"], 
  "rows": [["라거", "5%", "깔끔함"], ["에일", "6%", "풍부함"]] 
}]

...

---
### (EN) English Article
(H1 Title)

(Lead paragraph)

[CalloutBlock: { "type": "summary" }]
...
[/CalloutBlock]

(H2 Title)

[ComparisonTable: { 
  "headers": ["Beer", "ABV", "Notes"], 
  "rows": [["Lager", "5%", "Crisp"], ["Ale", "6%", "Fruity"]] 
}]

...