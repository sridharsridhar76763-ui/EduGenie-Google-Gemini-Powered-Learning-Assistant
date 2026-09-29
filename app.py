import json
import os
from typing import List

from dotenv import load_dotenv
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, Field
from google import genai


# --------------------------------------------------
# Load environment variables
# --------------------------------------------------

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
GEMINI_MODEL = os.getenv(
    "GEMINI_MODEL",
    "gemini-3.8-flash"
)


# --------------------------------------------------
# FastAPI application
# --------------------------------------------------

app = FastAPI(
    title="EduGenie",
    description="Google Gemini Powered Learning Assistant",
    version="1.0.0"
)


# --------------------------------------------------
# Templates
# --------------------------------------------------

templates = Jinja2Templates(
    directory="templates"
)


# --------------------------------------------------
# Gemini Client
# --------------------------------------------------

def get_gemini_client():

    if not GEMINI_API_KEY:

        raise RuntimeError(
            "GEMINI_API_KEY is missing. "
            "Please add your Gemini API key to the .env file."
        )

    return genai.Client(
        api_key=GEMINI_API_KEY
    )


async def generate_text(prompt: str) -> str:

    client = get_gemini_client()

    response = client.models.generate_content(
        model=GEMINI_MODEL,
        contents=prompt
    )

    if not response.text:

        raise RuntimeError(
            "Gemini returned an empty response."
        )

    return response.text.strip()


# --------------------------------------------------
# Request Models
# --------------------------------------------------

class QARequest(BaseModel):

    question: str = Field(
        ...,
        min_length=1,
        max_length=12000
    )


class ExplainRequest(BaseModel):

    concept: str = Field(
        ...,
        min_length=1,
        max_length=12000
    )

    level: str = "beginner"


class QuizRequest(BaseModel):

    topic: str = Field(
        ...,
        min_length=1,
        max_length=5000
    )

    level: str = "beginner"

    count: int = Field(
        default=3,
        ge=1,
        le=10
    )


class SummaryRequest(BaseModel):

    text: str = Field(
        ...,
        min_length=1,
        max_length=12000
    )

    level: str = "beginner"


class LearningPathRequest(BaseModel):

    topic: str = Field(
        ...,
        min_length=1,
        max_length=5000
    )

    level: str = "beginner"

    hours_per_week: float = Field(
        default=5,
        gt=0,
        le=80
    )

    weeks: int = Field(
        default=4,
        ge=1,
        le=12
    )


# --------------------------------------------------
# Home Page
# --------------------------------------------------

@app.get(
    "/",
    response_class=HTMLResponse
)
async def home(request: Request):

    return templates.TemplateResponse(
        "index.html",
        {
            "request": request
        }
    )


# --------------------------------------------------
# Health Check
# --------------------------------------------------

@app.get("/health")
async def health():

    return {
        "status": "ok",
        "application": "EduGenie",
        "message": "EduGenie is running successfully"
    }


# --------------------------------------------------
# Q&A
# --------------------------------------------------

@app.post("/qa")
async def question_answer(
    request: QARequest
):

    prompt = f"""
You are EduGenie, an AI educational assistant.

Answer the student's question clearly and accurately.

Student Question:
{request.question}

Instructions:
- Use simple language.
- Explain step by step when necessary.
- Give examples where useful.
- Keep the answer educational.
- Avoid unnecessary complexity.
"""

    answer = await generate_text(prompt)

    return {
        "answer": answer
    }


# --------------------------------------------------
# Explain Concept
# --------------------------------------------------

@app.post("/explain")
async def explain(
    request: ExplainRequest
):

    prompt = f"""
You are an expert educational tutor.

Explain the following concept to a
{request.level} level student.

Concept:
{request.concept}

Instructions:

1. Give a simple definition.
2. Explain the concept step by step.
3. Give a practical example.
4. Mention important points.
5. Use easy-to-understand language.
"""

    explanation = await generate_text(prompt)

    return {
        "explanation": explanation
    }


# --------------------------------------------------
# Quiz Generation
# --------------------------------------------------

@app.post("/quiz")
async def quiz(
    request: QuizRequest
):

    prompt = f"""
Create a multiple-choice educational quiz.

Topic:
{request.topic}

Student Level:
{request.level}

Number of Questions:
{request.count}

Return ONLY valid JSON.

The JSON must have this format:

{{
    "title": "Quiz title",
    "questions": [
        {{
            "question": "Question text",
            "options": [
                "Option A",
                "Option B",
                "Option C",
                "Option D"
            ],
            "answer": "Correct option",
            "explanation": "Short explanation"
        }}
    ]
}}

Rules:
- Each question must contain exactly 4 options.
- Only one answer must be correct.
- Do not duplicate questions.
- Questions should test understanding.
"""

    result = await generate_text(prompt)

    # Remove Markdown code fences if Gemini adds them
    result = result.strip()

    if result.startswith("```json"):

        result = result[
            len("```json"):
        ]

    if result.endswith("```"):

        result = result[:-3]

    result = result.strip()

    try:

        quiz_data = json.loads(result)

    except json.JSONDecodeError:

        return {
            "title": "Generated Quiz",
            "questions": [],
            "raw_response": result
        }

    return quiz_data


# --------------------------------------------------
# Summarization
# --------------------------------------------------

@app.post("/summarize")
async def summarize(
    request: SummaryRequest
):

    prompt = f"""
Summarize the following educational text
for a {request.level} learner.

Text:
{request.text}

Provide:

1. A short summary.
2. Important key points.
3. Simple and clear explanations.

Use this format:

Summary:
...

Key Points:
- ...
- ...
- ...
"""

    summary = await generate_text(prompt)

    return {
        "summary": summary
    }


# --------------------------------------------------
# Personalized Learning Path
# --------------------------------------------------

@app.post("/learn/recommendations")
async def learning_recommendations(
    request: LearningPathRequest
):

    prompt = f"""
Create a personalized learning path.

Topic:
{request.topic}

Learner Level:
{request.level}

Available Hours Per Week:
{request.hours_per_week}

Number of Weeks:
{request.weeks}

Requirements:

- Start with beginner concepts.
- Gradually progress to intermediate topics.
- Move toward advanced concepts.
- Include weekly topics.
- Include practical activities.
- Include learning resources.
- Make the plan realistic.
- Include final advice.

Return a clear week-by-week learning plan.
"""

    learning_path = await generate_text(prompt)

    return {
        "topic": request.topic,
        "level": request.level,
        "hours_per_week": request.hours_per_week,
        "weeks": request.weeks,
        "learning_path": learning_path
    }


# --------------------------------------------------
# Run directly with:
#
# python app.py
# --------------------------------------------------

if __name__ == "__main__":

    import uvicorn

    uvicorn.run(
        "app:app",
        host="127.0.0.1",
        port=8000,
        reload=True
    )