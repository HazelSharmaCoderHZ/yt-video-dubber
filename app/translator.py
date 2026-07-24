from math import ceil
from pathlib import Path
import time

from app.gemini_translator import GeminiTranslator
from app.utils.batching import chunk_list
from app.utils.json_utils import load_segments, save_segments


class Translator:
    def __init__(self):
        self.provider = GeminiTranslator()

    def translate(
        self,
        transcript_path: str,
        output_path: str,
        target_language: str = "en",
        batch_size: int = 25,
        max_retries: int = 3,
    ):
        transcript_path = Path(transcript_path)
        output_path = Path(output_path)

        source_language, segments = load_segments(transcript_path)

        total_batches = ceil(len(segments) / batch_size)

        print(f"\nTranslating {len(segments)} segments...")
        print(f"Batch size: {batch_size}")
        print(f"Total batches: {total_batches}\n")

        for batch_number, batch in enumerate(
            chunk_list(segments, batch_size),
            start=1,
        ):
            texts = [segment.original for segment in batch]

            for attempt in range(max_retries):
                try:
                    translations = self.provider.translate_batch(
                        texts,
                        target_language,
                    )
                    break

                except Exception:
                    print(
                        f"Batch {batch_number}: attempt "
                        f"{attempt + 1}/{max_retries} failed."
                    )

                    if attempt == max_retries - 1:
                        raise

                    wait_time = 2 ** attempt

                    print(f"Retrying in {wait_time} seconds...\n")

                    time.sleep(wait_time)

            for segment, translated in zip(batch, translations):
                segment.translated = translated

            # Checkpoint after every successful batch
            save_segments(
                output_path,
                source_language,
                target_language,
                segments,
            )

            print(
                f"✓ Batch {batch_number}/{total_batches} completed"
            )

        print(f"\nTranslated transcript saved to: {output_path}")

        return str(output_path)