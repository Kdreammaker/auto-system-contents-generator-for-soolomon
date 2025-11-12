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

    async def run_pipeline(self):
        """전체 자동화 파이프라인 실행"""
        logger.info("콘텐츠 자동 생성 파이프라인 시작.")
        try:
            self.output_dir.mkdir(parents=True, exist_ok=True)
            
            # 단계별 실행
            research_result = await self.step1_research()
            structure_result = await self.step2_structure(research_result)
            
            # 이후 단계들은 여기에 추가될 예정
            # await self.step3_content(research_result, structure_result)
            
            logger.info(f"✓ 파이프라인 성공적으로 완료. 결과물은 '{self.output_dir}' 폴더를 확인하세요.")
            
        except Exception as e:
            logger.error(f"✗ 파이프라인 실행 중 심각한 오류 발생: {e}", exc_info=True)
            raise

# 스크립트 실행 지점
if __name__ == "__main__":
    pipeline = ContentAutomationPipeline()
    asyncio.run(pipeline.run_pipeline())
