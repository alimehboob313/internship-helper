# Internship Helper

A small LangChain project that compares a job description with a list of my skills, then drafts a cover letter. I built it to learn LangChain by making something I'd actually use.

## What it does

1. **Match analysis:** a prompt template, the Gemini model, and structured output (a Pydantic model) return a fit score, matching skills, missing skills, and a short summary.
2. **Cover letter draft:** a second chain returns plain text, and the prompt tells the model to use only the skills listed and never to invent experience.

## Setup

1. Create a virtual environment with Python 3.13 and activate it.
2. Install the packages: `pip install langchain langchain-google-genai python-dotenv`
3. Create a `.env` file containing `GOOGLE_API_KEY=your_key_here`
4. Create `job.txt` with the job description and `skills.txt` with your real skills, and state your student status in `skills.txt`.
5. Run: `python analyzer.py`

`job.txt`, `skills.txt`, and `.env` are git-ignored, so they never get committed.

## Notes

- It uses the free Gemini API tier. Each run makes two API calls, so the daily quota runs out fast.
- The script stops with a message if either text file is empty.
- The cover letter is only a draft. Read it, fix anything untrue, and add your own name before using it.

## Built with

Python, LangChain, Gemini (via `langchain-google-genai`), Pydantic
