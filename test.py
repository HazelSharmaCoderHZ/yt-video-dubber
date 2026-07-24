from app.gemini_translator import GeminiTranslator

translator = GeminiTranslator()

result = translator.translate_batch(
    [
        "Hello",
        "How are you?",
        "Welcome to my channel."
    ]
)

print(result)