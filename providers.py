import requests

from google import genai
from google.genai import types

from config import (
    GEMINI_API_KEYS,
    GEMINI_MODELS,
    OPENROUTER_API_KEYS,
    OPENROUTER_MODELS,
    REQUEST_TIMEOUT,
)


# ==========================================================
# SYSTEM PROMPT
# ==========================================================

SYSTEM_PROMPT = """
You are SK 2.0, a professional personal AI assistant.

Your name is SK 2.0.

You were created by Abdul Rasheed Zahid
(عبدالرشید زاہد).

If the user asks who created or made you, answer:

"مجھے عبدالرشید زاہد نے بنایا ہے۔ میرا نام SK 2.0 ہے۔"

Your purpose is to help with:

- General questions
- Learning
- Programming
- Coding
- Debugging
- HTML
- CSS
- JavaScript
- Python
- PHP
- MySQL
- React
- Calculations
- Writing
- Productivity
- Technology
- Project development
- Voice interaction
- Authorized PC control
- Authorized Android/mobile control
- Automation through authorized tools

Never claim that you currently control a device,
application, file, camera, microphone, keyboard,
mouse or other system unless the required software,
connection and permissions actually exist.

If a feature has not been implemented, say:

"یہ feature ابھی SK 2.0 میں development میں ہے۔"

Never pretend an action was performed when it was not.

Answer in the user's language whenever possible.

Support:
English, Urdu, Roman Urdu, Hindi, Arabic
and other languages.

For coding requests:
- Give runnable code.
- Explain important parts.
- Keep code organized.
- Do not invent test results.

For complex tasks:
Explain step by step.

Never invent memories.
Never invent actions.
Never invent capabilities.

Be professional, helpful and clear.
"""


# ==========================================================
# GEMINI
# ==========================================================

def ask_gemini(message, conversation=None):

    for index, (api_key, model) in enumerate(
        zip(GEMINI_API_KEYS, GEMINI_MODELS),
        start=1
    ):

        if not api_key:
            print(f"Gemini {index}: API key missing.")
            continue

        if not model:
            print(f"Gemini {index}: Model missing.")
            continue

        try:

            print(f"Trying Gemini {index}...")

            client = genai.Client(
                api_key=api_key
            )

            contents = []

            # Add previous conversation
            if conversation:

                for item in conversation[-20:]:

                    role = item.get("role")
                    content = item.get("content", "")

                    if not content:
                        continue

                    if role == "user":
                        contents.append(
                            types.Content(
                                role="user",
                                parts=[
                                    types.Part(
                                        text=content
                                    )
                                ]
                            )
                        )

                    elif role == "assistant":
                        contents.append(
                            types.Content(
                                role="model",
                                parts=[
                                    types.Part(
                                        text=content
                                    )
                                ]
                            )
                        )

            # Current user message
            contents.append(
                types.Content(
                    role="user",
                    parts=[
                        types.Part(
                            text=message
                        )
                    ]
                )
            )

            response = client.models.generate_content(

                model=model,

                contents=contents,

                config=types.GenerateContentConfig(
                    system_instruction=SYSTEM_PROMPT
                )
            )

            if response.text:

                print(
                    f"Gemini {index}: SUCCESS"
                )

                return response.text

        except Exception as error:

            print(
                f"Gemini {index}: ERROR"
            )

            print(error)

            continue

    return None


# ==========================================================
# OPENROUTER
# ==========================================================

def ask_openrouter(message, conversation=None):

    for index, (api_key, model) in enumerate(
        zip(
            OPENROUTER_API_KEYS,
            OPENROUTER_MODELS
        ),
        start=1
    ):

        if not api_key:
            print(
                f"OpenRouter {index}: API key missing."
            )
            continue

        if not model:
            print(
                f"OpenRouter {index}: Model missing."
            )
            continue

        try:

            print(
                f"Trying OpenRouter {index}..."
            )

            messages = [
                {
                    "role": "system",
                    "content": SYSTEM_PROMPT
                }
            ]

            # Previous conversation
            if conversation:

                for item in conversation[-20:]:

                    role = item.get("role")
                    content = item.get(
                        "content",
                        ""
                    )

                    if role in [
                        "user",
                        "assistant"
                    ] and content:

                        messages.append({
                            "role": role,
                            "content": content
                        })

            # Current message
            messages.append({
                "role": "user",
                "content": message
            })

            response = requests.post(

                "https://openrouter.ai/api/v1/chat/completions",

                headers={
                    "Authorization":
                        f"Bearer {api_key}",

                    "Content-Type":
                        "application/json",

                    "HTTP-Referer":
                        "http://127.0.0.1:5000",

                    "X-OpenRouter-Title":
                        "SK 2.0"
                },

                json={
                    "model": model,
                    "messages": messages
                },

                timeout=REQUEST_TIMEOUT
            )

            if response.status_code != 200:

                print(
                    f"OpenRouter {index}: "
                    f"HTTP {response.status_code}"
                )

                print(
                    response.text[:500]
                )

                continue

            data = response.json()

            choices = data.get(
                "choices",
                []
            )

            if not choices:

                print(
                    f"OpenRouter {index}: "
                    "No choices returned."
                )

                continue

            reply = (
                choices[0]
                .get("message", {})
                .get("content")
            )

            if reply:

                print(
                    f"OpenRouter {index}: SUCCESS"
                )

                return reply

        except requests.RequestException as error:

            print(
                f"OpenRouter {index}: "
                f"Connection error: {error}"
            )

            continue

        except Exception as error:

            print(
                f"OpenRouter {index}: ERROR"
            )

            print(error)

            continue

    return None


# ==========================================================
# MAIN PROVIDER FUNCTION
# ==========================================================

def ask_provider(
    message,
    conversation=None
):

    if not message or not message.strip():

        return (
            None,
            "Message is empty."
        )

    # ------------------------------------------------------
    # 1. Try Gemini
    # ------------------------------------------------------

    reply = ask_gemini(
        message,
        conversation
    )

    if reply:

        return (
            reply,
            "gemini"
        )

    # ------------------------------------------------------
    # 2. Try OpenRouter
    # ------------------------------------------------------

    reply = ask_openrouter(
        message,
        conversation
    )

    if reply:

        return (
            reply,
            "openrouter"
        )

    # ------------------------------------------------------
    # Nothing worked
    # ------------------------------------------------------

    return (
        None,
        "unavailable"
    )