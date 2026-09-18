import requests

from config import OPENROUTER_API_KEY_1


OPENROUTER_TTS_URL = "https://openrouter.ai/api/v1/audio/speech"


def text_to_speech(text):
    if not text or not text.strip():
        return None, "Text is empty."

    if not OPENROUTER_API_KEY_1:
        return None, "OpenRouter API key is missing."

    try:
        response = requests.post(
            OPENROUTER_TTS_URL,
            headers={
                "Authorization":
                    f"Bearer {OPENROUTER_API_KEY_1}",
                "Content-Type":
                    "application/json"
            },
            json={
                "model": "deepgram/flux-tts:free",
                "input": text,
                "voice": "flux-alexis-en"
            },
            timeout=60
        )

        if response.status_code != 200:
            return None, (
                f"TTS Error {response.status_code}: "
                f"{response.text}"
            )

        return response.content, None

    except requests.RequestException as e:
        return None, f"Connection Error: {e}"

    except Exception as e:
        return None, f"TTS Error: {e}"