# ==========================================
# SK 2.0 - Complete Flask Backend
# ==========================================

from flask import Flask, jsonify, request, send_from_directory
from brain import ask_ai

from memory import (
    get_memories,
    add_memory,
    delete_memory,
    clear_memories
)

import os


# ==========================================
# APP CONFIGURATION
# ==========================================

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

FRONTEND_DIR = os.path.abspath(
    os.path.join(BASE_DIR, "..", "frontend")
)


# ==========================================
# HOME
# ==========================================

@app.route("/")
def home():

    return send_from_directory(
        FRONTEND_DIR,
        "index.html"
    )


# ==========================================
# FRONTEND FILES
# ==========================================

@app.route("/<path:filename>")
def frontend_files(filename):

    return send_from_directory(
        FRONTEND_DIR,
        filename
    )


# ==========================================
# STATUS
# ==========================================

@app.route("/api/status", methods=["GET"])
def status():

    return jsonify({

        "status": "online",

        "assistant": "SK 2.0",

        "version": "2.0",

        "message": "Backend is working"

    })


# ==========================================
# HEALTH CHECK
# ==========================================

@app.route("/api/health", methods=["GET"])
def health():

    return jsonify({

        "healthy": True,

        "assistant": "SK 2.0",

        "backend": "Flask",

        "message": "SK 2.0 backend is healthy"

    })


# ==========================================
# AI CHAT
# ==========================================

@app.route("/api/chat", methods=["POST"])
def chat():

    try:

        data = request.get_json(
            silent=True
        ) or {}

        message = data.get(
            "message",
            ""
        )

        conversation = data.get(
            "conversation",
            []
        )

        # ----------------------------------
        # Validate message
        # ----------------------------------

        if not isinstance(message, str):

            return jsonify({

                "success": False,

                "error": "Message must be text."

            }), 400

        message = message.strip()

        if not message:

            return jsonify({

                "success": False,

                "error": "Message is required."

            }), 400


        # ----------------------------------
        # Validate conversation
        # ----------------------------------

        if not isinstance(
            conversation,
            list
        ):

            conversation = []


        # ----------------------------------
        # Ask AI
        # ----------------------------------

        reply = ask_ai(
            message,
            conversation
        )


        # ----------------------------------
        # AI Error
        # ----------------------------------

        if not reply:

            return jsonify({

                "success": False,

                "error":
                    "AI provider did not return a response."

            }), 503


        # ----------------------------------
        # Response
        # ----------------------------------

        return jsonify({

            "success": True,

            "reply": reply

        })


    except Exception as e:

        print(
            "Chat Error:",
            e
        )

        return jsonify({

            "success": False,

            "error":
                "Internal server error."

        }), 500


# ==========================================
# MEMORY - GET ALL
# ==========================================

@app.route(
    "/api/memory",
    methods=["GET"]
)
def get_memory_api():

    try:

        memories = get_memories()

        return jsonify({

            "success": True,

            "count": len(memories),

            "memories": memories

        })

    except Exception as e:

        print(
            "Memory GET Error:",
            e
        )

        return jsonify({

            "success": False,

            "error":
                "Could not load memories."

        }), 500


# ==========================================
# MEMORY - ADD
# ==========================================

@app.route(
    "/api/memory",
    methods=["POST"]
)
def add_memory_api():

    try:

        data = request.get_json(
            silent=True
        ) or {}

        text = data.get(
            "text",
            ""
        )

        category = data.get(
            "category",
            "general"
        )


        # ----------------------------------
        # Validate text
        # ----------------------------------

        if not isinstance(
            text,
            str
        ):

            return jsonify({

                "success": False,

                "error":
                    "Memory text must be text."

            }), 400


        text = text.strip()


        if not text:

            return jsonify({

                "success": False,

                "error":
                    "Memory text is required."

            }), 400


        # ----------------------------------
        # Validate category
        # ----------------------------------

        if not isinstance(
            category,
            str
        ):

            category = "general"

        category = category.strip()


        if not category:

            category = "general"


        # ----------------------------------
        # Save Memory
        # ----------------------------------

        memory = add_memory(
            text,
            category
        )


        return jsonify({

            "success": True,

            "message":
                "Memory saved successfully.",

            "memory": memory

        }), 201


    except Exception as e:

        print(
            "Memory Add Error:",
            e
        )

        return jsonify({

            "success": False,

            "error":
                "Could not save memory."

        }), 500


# ==========================================
# MEMORY - DELETE ONE
# ==========================================

@app.route(
    "/api/memory/<int:memory_id>",
    methods=["DELETE"]
)
def delete_memory_api(memory_id):

    try:

        deleted = delete_memory(
            memory_id
        )


        if not deleted:

            return jsonify({

                "success": False,

                "error":
                    "Memory not found."

            }), 404


        return jsonify({

            "success": True,

            "message":
                "Memory deleted successfully."

        })


    except Exception as e:

        print(
            "Memory Delete Error:",
            e
        )

        return jsonify({

            "success": False,

            "error":
                "Could not delete memory."

        }), 500


# ==========================================
# MEMORY - DELETE ALL
# ==========================================

@app.route(
    "/api/memory",
    methods=["DELETE"]
)
def delete_all_memories_api():

    try:

        clear_memories()


        return jsonify({

            "success": True,

            "message":
                "All memories cleared successfully."

        })


    except Exception as e:

        print(
            "Memory Clear Error:",
            e
        )

        return jsonify({

            "success": False,

            "error":
                "Could not clear memories."

        }), 500


# ==========================================
# ERROR HANDLER - 404
# ==========================================

@app.errorhandler(404)
def page_not_found(error):

    return jsonify({

        "success": False,

        "error": "Route not found."

    }), 404


# ==========================================
# ERROR HANDLER - 500
# ==========================================

@app.errorhandler(500)
def internal_server_error(error):

    return jsonify({

        "success": False,

        "error":
            "Internal server error."

    }), 500


# ==========================================
# START SERVER
# ==========================================

if __name__ == "__main__":

    print("")
    print("================================")
    print("        SK 2.0 SERVER")
    print("================================")
    print("Assistant : SK 2.0")
    print("Backend   : Flask")
    print("Frontend  :", FRONTEND_DIR)
    print("")
    print("Open:")
    print("http://127.0.0.1:5000")
    print("")
    print("API:")
    print("GET    /api/status")
    print("GET    /api/health")
    print("POST   /api/chat")
    print("GET    /api/memory")
    print("POST   /api/memory")
    print("DELETE /api/memory/<id>")
    print("DELETE /api/memory")
    print("================================")
    print("")

    app.run(
        host="127.0.0.1",
        port=5000,
        debug=True
    )