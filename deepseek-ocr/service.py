from __future__ import annotations

import bentoml
from bentoml.models import HuggingFaceModel
from typing import List
from PIL.Image import Image as PILImage
from vllm import LLM, SamplingParams
from vllm.model_executor.models.deepseek_ocr import NGramPerReqLogitsProcessor

PROMPT_FREE_OCR = "<image>\nFree OCR."
# for doc-to-markdown with layout grounding:
# PROMPT_FREE_OCR = "<image>\n<|grounding|>Convert the document to markdown."

bento_image = bentoml.images.Image(python_version="3.12") \
    .python_packages("Pillow", "numpy<2.3") \
    .run('pip install -U vllm --pre --extra-index-url https://wheels.vllm.ai/nightly')

@bentoml.service(
    name="deepseek-ocr-vllm",
    image=bento_image,
    resources={
        "gpu": 1,
        "gpu_type": "nvidia-a100-80gb",
    },
)
class DeepSeekOCR:
    model_path = HuggingFaceModel("deepseek-ai/DeepSeek-OCR")

    def __init__(self) -> None:
        self.llm = LLM(
            model=self.model_path,
            trust_remote_code=True,
            enable_prefix_caching=False,
            mm_processor_cache_gb=0,
            logits_processors=[NGramPerReqLogitsProcessor],
        )

        self.sampling = SamplingParams(
            temperature=0.0,
            max_tokens=8192,
            # ngram logit processor args
            extra_args=dict(
                ngram_size=30,
                window_size=90,
                whitelist_token_ids={128821, 128822},  # whitelist: <td>, </td>
            ),
            skip_special_tokens=False,
        )

    @bentoml.api
    def ocr_image(self, image: PILImage, prompt: str = PROMPT_FREE_OCR) -> str:
        # convert to RGB
        if image.mode != "RGB":
            image = image.convert("RGB")

        model_input = [{"prompt": prompt, "multi_modal_data": {"image": image}}]
        outputs = self.llm.generate(model_input, self.sampling)
        return outputs[0].outputs[0].text

    @bentoml.api
    def ocr_batch(self, images: list[PILImage], prompt: str = PROMPT_FREE_OCR) -> list[str]:
        rgb_images = [(img if img.mode == "RGB" else img.convert("RGB")) for img in images]
        model_input = [{"prompt": prompt, "multi_modal_data": {"image": img}} for img in rgb_images]
        outputs = self.llm.generate(model_input, self.sampling)
        return [o.outputs[0].text for o in outputs]
