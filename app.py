from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
import os
from google import genai

# Load env variables
load_dotenv()

app = Flask(__name__)

# Gemini client
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

SYSTEM_PROMPT = """
You are an AI student mentor for the HomeIntern platform.
Recommend ONLY courses and internships provided by HomeIntern.
Be honest, friendly, and practical.
"""

# Dummy HomeIntern data (can expand later)
HOMEINTERN_DATA = {
    "courses": [
        {"name": "Python Basics", "level": "Beginner", "duration": "1 Month", "url": "/courses/python"},
        {"name": "Web Development", "level": "Beginner", "duration": "2 Months", "url": "/courses/web"}
    ],
    "internships": [
        {"name": "AI Internship", "level": "Beginner", "duration": "3 Months", "url": "/internships/ai"},
        {"name": "Web Internship", "level": "Beginner", "duration": "2 Months", "url": "/internships/web"}
    ]
}

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_msg = request.json.get("message", "")

    context = f"""
HomeIntern Courses:
{HOMEINTERN_DATA['courses']}

HomeIntern Internships:
{HOMEINTERN_DATA['internships']}
"""

    prompt = SYSTEM_PROMPT + context + "\nStudent: " + user_msg + "\nAI:"

    try:
        response = client.models.generate_content(
            model="gemini-3-flash-preview",
            contents=prompt
        )
        reply = response.text
    except Exception as e:
        reply = (
            "⚠️ I'm currently busy due to high traffic.\n"
            "Please try again in a moment 🙂"
        )
        print("Gemini error:", e)

    return jsonify({"reply": reply})

# 🔴 THIS PART IS CRITICAL
if __name__ == "__main__":
    app.run(debug=True)
