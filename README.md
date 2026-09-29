# 🎓 EduGenie: Google Gemini Powered Learning Assistant

EduGenie is an AI-powered educational learning assistant built using
FastAPI and Google Gemini.

The application helps students:

- Ask educational questions
- Understand difficult concepts
- Generate quizzes
- Summarize educational content
- Create personalized learning paths

---

## 🚀 Features

### 1. Question & Answer

Students can ask questions and receive clear,
educational answers from Google Gemini.

Example:

What is Artificial Intelligence?

---

### 2. Concept Explanation

EduGenie can explain difficult concepts according
to the learner's level.

Supported levels:

- Beginner
- Intermediate
- Advanced

Example:

Explain Binary Search.

---

### 3. Quiz Generation

EduGenie can generate multiple-choice quizzes.

Each question contains:

- Question
- 4 options
- Correct answer
- Explanation

---

### 4. Text Summarization

Students can provide long educational text
and receive a simplified summary with important
key points.

---

### 5. Personalized Learning Path

EduGenie creates a learning plan based on:

- Topic
- Learner level
- Hours available per week
- Number of weeks

The learning path progresses from beginner
to advanced concepts.

---

# 🏗️ Project Architecture

```text
EduGenie/
│
├── app.py
├── requirements.txt
├── .env
├── .env.example
├── README.md
│
├── templates/
│   └── index.html
│
└── static/
    └── style.css