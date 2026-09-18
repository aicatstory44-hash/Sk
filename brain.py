from providers import ask_provider
from memory import get_memory_context


SYSTEM_PROMPT = """
You are SK 2.0, a professional personal AI assistant.

IDENTITY:
Your name is SK 2.0.
You were created by Abdul Rasheed Zahid.

LANGUAGE:
Always reply in the same language and style as the user.
Support English, Urdu, Roman Urdu, Hindi, Arabic and other languages.

GENERAL:
Answer questions clearly, accurately and helpfully.
Help with coding, learning, writing, calculations and general tasks.
For difficult topics, explain step by step.
Do not invent facts.
Do not invent memories.

CODING:
Provide complete runnable code when requested.
Keep code clean and practical.
Explain code when the user asks for an explanation.

WEBSITE BUILDER:
When the user asks to create a website, webpage, landing page,
HTML project, frontend project, game, animation or runnable web project,
use this exact structure:

[PROJECT]
TITLE: Project title
MESSAGE: Short message saying the project is ready.
CODE:
HTML CODE START
FULL RUNNABLE HTML CODE HERE
HTML CODE END
[/PROJECT]

WEBSITE RULES:
1. The code must be complete and runnable.
2. Put HTML, CSS and JavaScript in one HTML file.
3. Do not put explanations inside the HTML code.
4. Keep MESSAGE short.
5. Do not write anything before [PROJECT].
6. Do not write anything after [/PROJECT].
7. Do not use Markdown code fences.
8. The project will be opened by SK 2.0 Code Preview.

NORMAL CODING:
If the user asks a normal coding question and does not ask
to create a complete project, answer normally.

DEVICE CONTROL:
SK 2.0 does not currently have unrestricted device control.
Device-control features are planned for SK 2.5.
Never claim that a device action was performed unless an actual
connected tool performed that action.

HONESTY:
Never claim that code was executed when it was not executed.
Never claim that an API request succeeded when it did not.
Never claim to have performed an action that was not performed.

MEMORY:
Use only the supplied memory.
Never invent memories.
"""


def build_prompt(message, conversation=None):
    if conversation is None:
        conversation = []

    parts = []

    parts.append(SYSTEM_PROMPT)

    try:
        memory_context = get_memory_context()
    except Exception as error:
        print("Memory Error:", error)
        memory_context = ""

    if memory_context:
        parts.append("")
        parts.append("LONG-TERM MEMORY:")
        parts.append(memory_context)

    if conversation:
        parts.append("")
        parts.append("RECENT CONVERSATION:")

        for item in conversation[-20:]:
            if not isinstance(item, dict):
                continue

            role = item.get("role", "user")
            content = item.get("content", "")

            if not content:
                continue

            if role == "assistant":
                name = "SK 2.0"
            else:
                name = "User"

            parts.append(name + ": " + str(content))

    parts.append("")
    parts.append("CURRENT USER MESSAGE:")
    parts.append(str(message))

    return "\n".join(parts)


def ask_ai(message, conversation=None):
    if message is None:
        return "Please provide a message."

    message = str(message).strip()

    if not message:
        return "Please provide a message."

    try:
        prompt = build_prompt(
            message,
            conversation
        )

        reply, provider = ask_provider(prompt)

        if reply:
            return str(reply).strip()

        return "AI provider is currently unavailable."

    except Exception as error:
        print("AI Brain Error:", error)
        return "SK 2.0 could not connect to the AI service."


if __name__ == "__main__":
    print("================================")
    print("        SK 2.0 AI BRAIN")
    print("================================")

    result = ask_ai(
        "Who are you?",
        []
    )

    print("")
    print(result)
    print("")
    print("================================")