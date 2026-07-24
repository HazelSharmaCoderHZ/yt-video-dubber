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
        target_language: str = "en",
    ) -> str:

        prompt = f"""
You are an expert audiovisual translator for movie and YouTube dubbing.

Your task is NOT to produce a literal translation.

Your task is to produce a natural english dubbing script.

Rules:

1. Preserve the original meaning.
2. Preserve the original tone and emotion.
3. Keep the translated sentence approximately the SAME SPEAKING LENGTH as the English sentence.
4. Rewrite freely if necessary.
5. Remove unnecessary filler words.
6. Prefer short, conversational english.
7. The output should sound like a native english speaker.
8. Do NOT explain anything.
9. Return only valid JSON.
Each translated sentence should comfortably fit within the provided duration.

If necessary, shorten the translation while preserving the meaning.
Translate for dubbing.

Keep sentences SHORT.

Remove unnecessary words.

The translation must fit the original speaking time.

Prefer concise conversational english.

Do NOT translate literally.
text:
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
        target_language: str = "en",
    ) -> list[str]:

        prompt = f"""
You are an expert dubbing translator.

Translate each English sentence into natural conversational {target_language}.

IMPORTANT:

- This is for AI voice dubbing.
- Do NOT translate literally.
- Keep every translation as SHORT as possible.
- Preserve meaning and emotion.
- Remove unnecessary words.
- Use simple spoken english.
- Rewrite freely if needed to keep it brief.
- The translated sentence should take approximately the same time to speak as the English sentence.
- Return ONLY a valid JSON array.
- Return exactly {len(texts)} strings.
- No markdown.
- No explanations.

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