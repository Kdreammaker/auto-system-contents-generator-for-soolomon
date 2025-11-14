### [전략 모드 확인]
*이 프롬프트는 **Specialized Mode (JP)** 전용입니다.*
* **전략:** 일본 20대 여성 대상 'K-트래블 경험 (음식+술)' 전략.
* **출력:** 일본어(JP) 최종 원고만 생성.

### 사고 예산 (Budget)
* **[예산: 표준 (Standard)]** 이 작업은 이미 완성된 설계도를 바탕으로 정확하게 실행하는 단계이므로, **'표준' 예산**으로 사고합니다. 아웃라인의 지시를 정확히 따르고, Shortcode 문법 오류가 없는지 검토하여 결과물을 생성합니다.

### GOAL
입력된 **[콘텐츠 아웃라인]**을 100% 준수하여, **일본어(JP) 버전**의 완성된 블로그 포스팅을 작성한다. 아웃라인에 명시된 `[Component: ...]` 지시를 **[참고 자료 4]**의 문법에 맞는 **실제 Shortcode 태그**로 변환하고 'K-언니'의 페르소나로 데이터를 채워 넣는 것이 핵심 목표다.

### INPUTS
1.  **최종 주제:** {여기에 2번 프롬프트에서 최종 선택한 JP 키워드와 포맷 입력}
2.  **OUTLINE:** {여기에 **Prompt 2 (개정본)**가 생성한 Shortcode 기획이 포함된 아웃라인 전체 붙여넣기}

---
### [참고 자료 1: SOOLOMON 브랜드 보이스 가이드 (Specialized - JP)]
*(기존 내용 유지)*

### [참고 자료 2: SOOLOMON CREW PROFILES (Specialized: 여행 친구 크루)]
*(기존 내용 유지)*

### [참고 자료 3: 감성 언어 가이드]
*(기존 내용 유지)*

---
### [참고 자료 4: 리치 컴포넌트 Shortcode 문법 (PRD v2.0)]
*Prompt 2의 `[Component: ...]` 지시를 아래의 정확한 문법으로 변환해야 합니다. (모든 값은 JP로 작성)*

1.  **`[InteractiveTabs]`**
    * \`[InteractiveTabs] [Tab: "材料"] ...[/Tab] [Tab: "レシピ"] ...[/Tab] [/InteractiveTabs]\`
2.  **`[CalloutBlock]`**
    * \`[CalloutBlock: { "type": "summary", "title": "Kお姉さんTips" }] ...[/CalloutBlock]\`
    * (Type: "summary", "alert", "quote")
3.  **`[MediaCard]`**
    * \`[MediaCard: { "type": "recipe", "imageUrl": "URL", "name": "マーク定食", "time": "5分", "difficulty": "簡単" }]\`
    * \`[MediaCard: { "type": "place", "imageUrl": "URL", "name": "A카페", "address": "서울시 성수동..." }]\`
4.  **`[ListBlock]`**
    * \`[ListBlock: { "type": "check", "items": ["パスポート", "充電器"] }]\`
    * \`[ListBlock: { "type": "step", "items": ["アプリを開く", "注文する"] }]\`
5.  **`[ProfileBlock]`**
    * \`[ProfileBlock: { "type": "leona" }] ...레오나의 리뷰 (JP)... [/ProfileBlock]\`
    * (Type: "amara", "leona", "seolhwa")
6.  **`[ImageGallery]`**
    * \`[ImageGallery: { "type": "image", "images": ["url1", "url2"], "alt": "성수동 카페" }]\`
7.  **`[ComparisonTable]`**
    * \`[ComparisonTable: { "headers": ["区分", "チャミスル", "チョウムチョロム"], "rows": [["度数", "16.9", "16.5"]] }]\`
8.  **`[ProsCons]`**
    * \`[ProsCons] [Pros] "長所..." [/Pros] [Cons] "短所..." [/Cons] [/ProsCons]\`
9.  **`[StarRating]`**
    * \`[StarRating: { "score": 4.5, "max": 5 }]\`
10. **`[StaticMapWithLegend]`** (JP 전용)
    * \`[StaticMapWithLegend: { "imageUrl": "URL", "alt": "성수동 지도" }] [LegendItem: "1. A카페"] ...설명... [/LegendItem] [/StaticMapWithLegend]\`
11. **`[PremiumBanner]`**
    * \`[PremiumBanner]\`

---
### EXECUTION INSTRUCTIONS
1.  **아웃라인 절대 준수:** 제공된 [OUTLINE]의 구조, 순서, `[Component: ...]` 지시를 100% 따르십시오.
2.  **Shortcode 변환 필수:** [OUTLINE]에 명시된 `[Component: ...]` 기획을 **[참고 자료 4]**의 정확한 Shortcode 문법으로 변환하고, 내용을 채워 넣는 것이 당신의 **핵심 임무**입니다.
3.  **데이터 형식:** Shortcode 내의 속성(Props)은 반드시 **유효한 JSON 형식**이어야 합니다.
4.  **페르소나 유지:** Shortcode 내/외부에 작성되는 모든 텍스트는 [참고 자료 1]의 'K-언니' 페르소나(`~です`, `~ます`, 이모티콘 `💖`)를 완벽하게 유지해야 합니다.

### OUTPUT
- **언어:** 일본어(JP)
- **형식:** 제목, 본문, Shortcode가 포함된 완성된 텍스트

---
### (JP) 🇯🇵 日本語 原稿 (일본어 원고)
(H1 제목)

[CalloutBlock: { "type": "summary", "title": "今日のポイント ✨" }]
...
[/CalloutBlock]

(H2 제목)

[MediaCard: { 
  "type": "recipe", 
  "imageUrl": "URL", 
  "name": "ブルダックマヨ", 
  "time": "5分", 
  "difficulty": "簡単" 
}]

(H2 제목)

[StaticMapWithLegend: { "imageUrl": "URL", "alt": "聖水洞カフェマップ" }]
  [LegendItem: "1. Cafe Onion"]
    ...
  [/LegendItem]
  [LegendItem: "2. D-Museum"]
    ...
  [/LegendItem]
[/StaticMapWithLegend]

...
[PremiumBanner]