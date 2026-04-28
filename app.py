from flask import Flask, request, jsonify
from openai import OpenAI
import os

app = Flask(__name__)

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

def generate_study_plan(goal, time, weakness, deadline):
    prompt = f"""
    Create a personalized study plan:

    Goal: {goal}
    Daily Study Time: {time}
    Weakness: {weakness}
    Deadline: {deadline}

    Output:
    1. Summary
    2. Today's Study Plan
    3. Smart Insights
    """

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a strict and practical study coach."},
            {"role": "user", "content": prompt}
        ]
    )

    return response.choices[0].message.content


@app.route("/")
def home():
    return "Study Planner API is running"


@app.route("/generate", methods=["POST"])
def generate():
    data = request.json

    result = generate_study_plan(
        data.get("goal"),
        data.get("time"),
        data.get("weakness"),
        data.get("deadline")
    )

    return jsonify({"result": result})
