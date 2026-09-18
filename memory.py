# ==========================================
# SK 2.0 - Long Term Memory System
# ==========================================

import json
from pathlib import Path
from datetime import datetime


# ------------------------------------------
# Memory File
# ------------------------------------------

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
MEMORY_FILE = DATA_DIR / "memory.json"


# ------------------------------------------
# Make sure data folder exists
# ------------------------------------------

DATA_DIR.mkdir(parents=True, exist_ok=True)


# ------------------------------------------
# Load Memories
# ------------------------------------------

def load_memories():

    try:

        if not MEMORY_FILE.exists():

            save_memories([])

            return []

        with open(
            MEMORY_FILE,
            "r",
            encoding="utf-8"
        ) as file:

            data = json.load(file)

        memories = data.get("memories", [])

        if not isinstance(memories, list):
            return []

        return memories

    except (json.JSONDecodeError, OSError):

        # Recover from damaged JSON
        save_memories([])

        return []


# ------------------------------------------
# Save Memories
# ------------------------------------------

def save_memories(memories):

    DATA_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    data = {
        "memories": memories
    }

    with open(
        MEMORY_FILE,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            data,
            file,
            ensure_ascii=False,
            indent=4
        )


# ------------------------------------------
# Add Memory
# ------------------------------------------

def add_memory(text, category="general"):

    text = str(text).strip()

    if not text:
        return None

    memories = load_memories()

    # Avoid exact duplicates
    for memory in memories:

        if memory.get("text", "").lower() == text.lower():
            return memory

    memory = {
        "id": len(memories) + 1,
        "text": text,
        "category": category,
        "created_at": datetime.now().isoformat(
            timespec="seconds"
        )
    }

    memories.append(memory)

    save_memories(memories)

    return memory


# ------------------------------------------
# Get All Memories
# ------------------------------------------

def get_memories():

    return load_memories()


# ------------------------------------------
# Search Memories
# ------------------------------------------

def search_memories(keyword):

    keyword = str(keyword).strip().lower()

    if not keyword:
        return []

    memories = load_memories()

    results = []

    for memory in memories:

        text = memory.get(
            "text",
            ""
        ).lower()

        if keyword in text:
            results.append(memory)

    return results


# ------------------------------------------
# Delete Memory By ID
# ------------------------------------------

def delete_memory(memory_id):

    memories = load_memories()

    new_memories = [
        memory
        for memory in memories
        if memory.get("id") != memory_id
    ]

    if len(new_memories) == len(memories):
        return False

    # Re-number IDs
    for index, memory in enumerate(
        new_memories,
        start=1
    ):
        memory["id"] = index

    save_memories(new_memories)

    return True


# ------------------------------------------
# Clear All Memories
# ------------------------------------------

def clear_memories():

    save_memories([])

    return True


# ------------------------------------------
# Memory Context For AI
# ------------------------------------------

def get_memory_context():

    memories = load_memories()

    if not memories:
        return ""

    lines = []

    for memory in memories:

        text = memory.get(
            "text",
            ""
        )

        category = memory.get(
            "category",
            "general"
        )

        lines.append(
            f"- [{category}] {text}"
        )

    return "\n".join(lines)


# ------------------------------------------
# Test
# ------------------------------------------

if __name__ == "__main__":

    print("SK 2.0 Memory System")
    print("--------------------")

    memories = get_memories()

    print(
        f"Memories stored: {len(memories)}"
    )

    print(
        "Memory file:",
        MEMORY_FILE
    )