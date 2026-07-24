import json
import os

from dotenv import load_dotenv
from google import genai

load_dotenv()


class GeminiTranslator:
    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY")

        if not api_key:
            raise ValueError("GEMINI_API_KEY not found.")

        self.client = genai.Client(api_key=api_key)

    def translate(
        self,
        text: str,
        target_language: str = "hi",
    ) -> str:

        prompt = f"""
Translate the following text into {target_language}.

Rules:
- Preserve the meaning.
- Keep names unchanged.
- Return ONLY the translated text.
- Do not add explanations.

Text:
{text}
"""

        response = self.client.models.generate_content(
            model="gemini-3.5-flash-lite",
            contents=prompt,
        )

        return response.text.strip()

    def translate_batch(
        self,
        texts: list[str],
        target_language: str = "hi",
    ) -> list[str]:

        prompt = f"""
Translate each sentence into {target_language}.

Rules:
- Preserve meaning.
- Keep names unchanged.
- Translate each sentence independently.
- Return ONLY a valid JSON array of translated strings.
- The output array must contain exactly {len(texts)} items.
- Do not use markdown.
- Do not wrap the JSON in ```.

Input:
{json.dumps(texts, ensure_ascii=False, indent=2)}
"""

        response = self.client.models.generate_content(
            model="gemini-3.5-flash-lite",
            contents=prompt,
        )

        result = response.text.strip()

        try:
            translations = json.loads(result)
        except json.JSONDecodeError as e:
            raise ValueError(
                f"Gemini returned invalid JSON:\n{result}"
            ) from e

        if not isinstance(translations, list):
            raise ValueError("Gemini response is not a JSON array.")

        if len(translations) != len(texts):
            raise ValueError(
                f"Expected {len(texts)} translations but got {len(translations)}."
            )

        return translations