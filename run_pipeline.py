import asyncio
import os
import yaml
import logging
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv

# .env 파일에서 환경 변수 로드
load_dotenv()

# 로깅 기본 설정
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class ContentAutomationPipeline:
    def __init__(self, base_dir="./content-output"):
        self.base_dir = Path(base_dir)
        self.date_str = datetime.now().strftime("%y%m%d")
        self.output_dir = self.base_dir / self.date_str
        self.prompts = self._load_prompts()
        
        # API 키 (실제 사용 시점에서 로드)
        self.perplexity_api_key = os.getenv("PERPLEXITY_API_KEY")
        self.gemini_api_key = os.getenv("GEMINI_API_KEY")
        self.claude_api_key = os.getenv("CLAUDE_API_KEY")
        self.nano_banana_api_key = os.getenv("NANO_BANANA_API_KEY")
        # ... 다른 API 키들도 필요에 따라 추가

    def _load_prompts(self):
        """prompts 폴더에서 .yaml 프롬프트 파일들을 로드합니다."""
        prompts = {}
        prompt_dir = Path("./prompts")
        if not prompt_dir.exists():
            logger.warning(f"프롬프트 폴더({prompt_dir})를 찾을 수 없습니다.")
            return prompts
            
        for prompt_file in prompt_dir.glob("*.yaml"):
            try:
                with open(prompt_file, 'r', encoding='utf-8') as f:
                    prompts[prompt_file.stem] = yaml.safe_load(f)
                    logger.info(f"'{prompt_file.name}' 프롬프트를 로드했습니다.")
            except Exception as e:
                logger.error(f"'{prompt_file.name}' 프롬프트 로드 중 오류 발생: {e}")
        return prompts

    def _save_result(self, step_name: str, file_name: str, content: str, lang: str = 'kr', extension: str = 'md'):
        """결과물을 지정된 경로에 파일로 저장합니다."""
        step_dir = self.output_dir / step_name
        step_dir.mkdir(parents=True, exist_ok=True)
        
        file_path = step_dir / f"{file_name}.{extension}"
        
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            logger.info(f"결과물이 '{file_path}'에 저장되었습니다.")
        except Exception as e:
            logger.error(f"'{file_path}' 파일 저장 중 오류 발생: {e}")

    async def step1_research(self):
        """Step 1: 콘텐츠 소재 조사 (Mockup)"""
        logger.info("Step 1: 콘텐츠 소재 조사 시작...")
        prompt_data = self.prompts.get('prompt1-research', {})
        
        # --- Mockup 로직 ---
        # 실제 API 호출 대신, 프롬프트 내용을 기반으로 한 Mockup 결과 생성
        # logger.info(f"API Key 'PERPLEXITY_API_KEY' 사용 예정: {self.perplexity_api_key[:5]}...")
        logger.info("실제 Perplexity API 호출은 생략합니다 (Mockup).")
        
        mock_result = f"""
# AI 기술 동향 조사 (Mockup)

## 개요
- Perplexity API를 통해 생성된 Mockup 데이터입니다.
- 원본 프롬프트 질문: {prompt_data.get('query', 'N/A')}

## 주요 동향
1.  **초거대 언어 모델(LLM)의 발전**: GPT-4, Gemini 등 더욱 정교한 모델 등장
2.  **멀티모달 AI**: 텍스트뿐만 아니라 이미지, 음성을 동시에 이해하고 생성하는 기술 확산
3.  **AI 윤리 및 안전성**: AI의 사회적 영향을 고려한 규제 및 기술적 논의 활발
"""
        self._save_result("step1", "step1-research-kr", mock_result)
        logger.info("Step 1 완료.")
        return mock_result

    async def step2_structure(self, research_result: str):
        """Step 2: 콘텐츠 구조 설계 (Mockup)"""
        logger.info("Step 2: 콘텐츠 구조 설계 시작...")
        prompt_template = self.prompts.get('prompt2-structure', {}).get('prompt', '')
        
        # --- Mockup 로직 ---
        # 실제 API 호출 대신, 프롬프트와 이전 단계 결과를 조합하여 Mockup 결과 생성
        # logger.info(f"API Key 'GEMINI_API_KEY' 사용 예정: {self.gemini_api_key[:5]}...")
        logger.info("실제 Gemini API 호출은 생략합니다 (Mockup).")

        # 프롬프트에 이전 단계 결과 삽입 (시뮬레이션)
        full_prompt = prompt_template.format(research_result=research_result)
        
        mock_result = f"""
# 블로그 글 구조 (Mockup)

아래는 Gemini API를 통해 생성된 Mockup 구조입니다.

---
{full_prompt}
---

## 제안된 구조

### 1. 서론
- AI 기술이 우리 삶에 미치는 영향과 최신 동향에 대한 관심 환기
- 생성형 AI가 가져올 미래에 대한 기대감 조성

### 2. 본론

#### 2.1. 초거대 언어 모델(LLM)의 진화
- GPT-3부터 Gemini까지의 발전 과정
- LLM이 비즈니스에 활용되는 실제 사례 소개

#### 2.2. 멀티모달 AI의 시대
- 텍스트를 넘어 이미지와 소리를 이해하는 AI
- DALL-E, Midjourney 등 이미지 생성 AI의 원리와 가능성

#### 2.3. AI 윤리와 미래 과제
- AI 발전에 따른 사회적, 윤리적 딜레마
- 앞으로 우리가 준비해야 할 것들

### 3. 결론
- AI 기술의 미래 전망 요약
- 독자들이 AI 시대를 어떻게 맞이해야 할지에 대한 제언
"""
        self._save_result("step2", "step2-structure-kr", mock_result)
        logger.info("Step 2 완료.")
        return mock_result

    async def step3_content(self, research_result: str, structure_result: str):
        """Step 3: 콘텐츠 작성, 이미지 생성, 표현 교정 (Mockup)"""
        logger.info("Step 3: 콘텐츠 작성 시작...")
        prompt_data = self.prompts.get('prompt3-content', {})
        
        # --- Mockup 로직 ---
        logger.info("실제 Gemini API (콘텐츠 작성) 호출은 생략합니다 (Mockup).")
        
        # 프롬프트에 이전 단계 결과 삽입 (시뮬레이션)
        full_prompt = prompt_data.get('prompt', '').format(
            research_result=research_result,
            structure_result=structure_result
        )
        
        mock_content = f"""
# AI 기술의 미래: 생성형 AI가 가져올 변화 (Mockup)

## 서론
AI 기술은 빠르게 발전하며 우리 삶의 모든 영역에 깊은 영향을 미치고 있습니다. 특히 최근 몇 년간 생성형 AI의 등장은 기술의 패러다임을 근본적으로 바꾸고 있습니다. 본 글에서는 최신 AI 기술 동향과 생성형 AI가 시장에 미치는 영향, 그리고 미래 전망에 대해 심층적으로 다룹니다.

## 본론

### 1. 초거대 언어 모델(LLM)의 진화
LLM은 방대한 텍스트 데이터를 학습하여 인간과 유사한 텍스트를 생성하는 AI 모델입니다. GPT-3, GPT-4, 그리고 구글의 Gemini와 같은 모델들은 단순한 정보 검색을 넘어, 창의적인 글쓰기, 코드 생성, 복잡한 문제 해결 등 다양한 분야에서 놀라운 성능을 보여주고 있습니다.
![image_placeholder_1](images/001.jpg)
이러한 LLM의 발전은 정보 접근성을 높이고, 콘텐츠 생산 방식을 혁신하며, 새로운 비즈니스 기회를 창출하고 있습니다. 기업들은 LLM을 활용하여 고객 서비스 자동화, 마케팅 콘텐츠 생성, 연구 개발 가속화 등 다양한 방식으로 경쟁력을 강화하고 있습니다.

### 2. 멀티모달 AI의 시대
텍스트 기반의 LLM을 넘어, 이제 AI는 이미지, 음성, 비디오 등 다양한 형태의 데이터를 이해하고 생성하는 멀티모달(Multimodal) 시대로 진입하고 있습니다. 구글의 Gemini는 텍스트, 이미지, 오디오, 비디오를 동시에 처리하며 더욱 복잡하고 현실적인 상호작용을 가능하게 합니다.
![image_placeholder_2](images/002.jpg)
DALL-E, Midjourney와 같은 이미지 생성 AI는 텍스트 프롬프트만으로 고품질의 이미지를 만들어내며 예술, 디자인, 광고 분야에 혁명을 가져오고 있습니다. 이러한 멀티모달 AI는 인간의 창의성을 증폭시키고, 이전에는 상상하기 어려웠던 새로운 형태의 콘텐츠와 서비스를 가능하게 할 것입니다.

### 3. AI 윤리와 미래 과제
AI 기술의 발전은 긍정적인 변화와 함께 윤리적, 사회적 과제도 던지고 있습니다. 딥페이크와 같은 기술 오용 문제, AI로 인한 일자리 변화, 데이터 편향성 문제 등이 대표적입니다.
![image_placeholder_3](images/003.jpg)
따라서 AI 기술 개발과 함께 투명성, 공정성, 책임성을 확보하기 위한 윤리적 가이드라인과 규제 마련이 시급합니다. 기술 개발자, 정책 입안자, 사회 구성원 모두가 협력하여 AI가 인류에게 이로운 방향으로 발전할 수 있도록 노력해야 할 것입니다.

## 결론
생성형 AI를 중심으로 한 최신 AI 기술은 인류에게 전례 없는 기회를 제공하고 있습니다. 기술의 잠재력을 최대한 활용하면서도, 발생할 수 있는 문제점들을 현명하게 해결해 나간다면, 우리는 더욱 풍요롭고 혁신적인 미래를 맞이할 수 있을 것입니다. 지속적인 연구와 사회적 논의를 통해 AI가 모두에게 이로운 기술로 자리매김할 수 있도록 노력해야 합니다.
"""
        self._save_result("step3", "step3-content-kr", mock_content)
        
        # 이미지 생성 (Mockup)
        image_paths = await self._generate_images(mock_content)
        
        # 표현 교정 (Mockup)
        revised_content_w_feedback, revised_content_final = await self._revise_content(mock_content)
        
        self._save_result("step3", "step3-revised-w.feedback-kr", revised_content_w_feedback)
        self._save_result("step3", "step3-revised-final-kr", revised_content_final)

        # HTML 변환 (Mockup)
        await self._convert_to_html(revised_content_final, "AI 기술의 미래: 생성형 AI가 가져올 변화")
        
        logger.info("Step 3 완료.")
        return revised_content_final

    async def _generate_images(self, content: str):
        """이미지 생성 (Mockup)"""
        logger.info("이미지 생성 시작 (Mockup)...")
        # 콘텐츠에서 이미지 플레이스홀더 추출 (정규식 사용)
        import re
        image_placeholders = re.findall(r'!(?P<alt>\[.*?\])\((?P<path>images/\d{3}\.jpg)\)', content)
        
        generated_image_paths = []
        for i, (alt_text, path) in enumerate(image_placeholders):
            # 실제 Nano Banana API 호출 대신 Mockup 이미지 생성 시뮬레이션
            image_name = f"step3-image-{str(i+1).zfill(3)}.jpg"
            image_dir = self.output_dir / "step3" / "images"
            image_dir.mkdir(parents=True, exist_ok=True)
            mock_image_path = image_dir / image_name
            
            # 실제 이미지 파일 생성 대신, 파일이 생성되었다고 가정
            with open(mock_image_path, 'w', encoding='utf-8') as f:
                f.write(f"Mockup Image Content for {alt_text} - {image_name}")
            
            generated_image_paths.append(str(mock_image_path))
            logger.info(f"Mockup 이미지 생성: {mock_image_path}")
        
        logger.info("이미지 생성 완료 (Mockup).")
        return generated_image_paths

    async def _revise_content(self, original_content: str):
        """콘텐츠 표현 교정 (Mockup)"""
        logger.info("콘텐츠 표현 교정 시작 (Mockup)...")
        prompt_data = self.prompts.get('prompt3-revision', {})
        
        # --- Mockup 로직 ---
        logger.info("실제 Claude API 호출은 생략합니다 (Mockup).")
        
        # 원본 콘텐츠에 교정 의견을 추가하는 Mockup
        revised_w_feedback = f"""
{original_content}

<!-- 교정 의견: 서론의 문장을 좀 더 간결하게 수정했습니다. -->
<!-- 교정 의견: '놀라운 성능을 보여주고 있습니다'를 '뛰어난 성능을 입증하고 있습니다'로 변경하여 표현을 강화했습니다. -->
<!-- 교정 의견: 'AI 윤리와 미래 과제' 섹션에서 문단 간의 연결을 자연스럽게 다듬었습니다. -->
"""
        # 최종 본문은 교정 의견이 없는 버전
        revised_final = original_content.replace("놀라운 성능을 보여주고 있습니다", "뛰어난 성능을 입증하고 있습니다")
        revised_final += "\n\n(이것은 교정된 최종 본문 Mockup입니다.)"
        
        logger.info("콘텐츠 표현 교정 완료 (Mockup).")
        return revised_w_feedback, revised_final

    async def _convert_to_html(self, content_body: str, title: str):
        """Markdown 콘텐츠를 HTML로 변환 (Mockup)"""
        logger.info("HTML 변환 시작 (Mockup)...")
        template_path = Path("./templates/content-template.html")
        if not template_path.exists():
            logger.error(f"HTML 템플릿 파일 '{template_path}'을 찾을 수 없습니다.")
            return

        with open(template_path, 'r', encoding='utf-8') as f:
            html_template = f.read()

        # Markdown to HTML 변환 (실제로는 markdown2 라이브러리 사용)
        # 여기서는 간단히 마크다운 헤더를 HTML 태그로 변환하는 Mockup
        html_content_body = content_body.replace("# ", "<h1>").replace("## ", "<h2>").replace("### ", "<h3>")
        html_content_body = html_content_body.replace("</h1>", "</h1>").replace("</h2>", "</h2>").replace("<h3>", "</h3>")
        
        # 이미지 경로 업데이트 (Mockup)
        html_content_body = html_content_body.replace("images/", f"./step3/images/")

        final_html = html_template.format(
            title=title,
            published_date=datetime.now().strftime("%Y-%m-%d"),
            content_body=html_content_body
        )
        
        self._save_result("step3", "step3-final-kr", final_html, extension='html')
        logger.info("HTML 변환 완료 (Mockup).")

    async def step4_social(self, blog_content: str):
        """Step 4: SNS 콘텐츠 변환 (Mockup)"""
        logger.info("Step 4: SNS 콘텐츠 변환 시작...")
        prompt_data = self.prompts.get('prompt4-social', {})

        # --- Mockup 로직 ---
        logger.info("실제 Gemini API (SNS 콘텐츠 변환) 호출은 생략합니다 (Mockup).")

        full_prompt = prompt_data.get('prompt', '').format(blog_content=blog_content)

        mock_social_content = f"""
# 인스타그램 포스트 (Mockup)

---
{full_prompt}
---

✨ AI 기술의 미래, 생성형 AI가 가져올 놀라운 변화! ✨

최신 AI 트렌드와 함께 우리 삶이 어떻게 혁신될지 궁금하신가요? 🤔
블로그에서 자세한 내용을 확인하고, AI 시대의 주인공이 되어보세요!

#AI기술 #생성형AI #미래기술 #인공지능 #기술트렌드 #혁신 #AI시대 #블로그포스트

🔗 지금 바로 확인하기: [블로그 링크]
"""
        self._save_result("step4", "step4-social-kr", mock_social_content)
        logger.info("Step 4 완료.")
        return mock_social_content

    async def run_pipeline(self):
        """전체 자동화 파이프라인 실행"""
        logger.info("콘텐츠 자동 생성 파이프라인 시작.")
        try:
            self.output_dir.mkdir(parents=True, exist_ok=True)
            
            # 단계별 실행
            research_result = await self.step1_research()
            structure_result = await self.step2_structure(research_result)
            
            content_final_result = await self.step3_content(research_result, structure_result)
            
            social_content_result = await self.step4_social(content_final_result)
            
            logger.info(f"✓ 파이프라인 성공적으로 완료. 결과물은 '{self.output_dir}' 폴더를 확인하세요.")
            
        except Exception as e:
            logger.error(f"✗ 파이프라인 실행 중 심각한 오류 발생: {e}", exc_info=True)
            raise

# 스크립트 실행 지점
if __name__ == "__main__":
    pipeline = ContentAutomationPipeline()
    asyncio.run(pipeline.run_pipeline())
