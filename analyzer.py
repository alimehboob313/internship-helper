from dotenv import load_dotenv
from pydantic import BaseModel, Field
from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.output_parsers import StrOutputParser

load_dotenv()


class MatchAnalysis(BaseModel):
    matching_skills: list[str] = Field(description="Skills from the candidate that match the job")
    missing_skills: list[str] = Field(description="Skills the job asks for that the candidate lacks")
    fit_score: int = Field(description="Overall fit from 0 to 100")
    summary: str = Field(description="Two sentence honest assessment")


llm = ChatGoogleGenerativeAI(model="gemini-flash-lite-latest")
structured_llm = llm.with_structured_output(MatchAnalysis)

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are an honest career advisor. Compare the candidate to the job. Never invent skills the candidate did not list."),
    ("human", "JOB DESCRIPTION:\n{job}\n\nCANDIDATE SKILLS:\n{skills}"),
])

chain = prompt | structured_llm

job = open("job.txt", encoding="utf-8").read()
skills = open("skills.txt", encoding="utf-8").read()
if not job.strip() or not skills.strip():
    raise SystemExit("job.txt or skills.txt is empty. Fill both files first.")
result = chain.invoke({"job": job, "skills": skills})
print("Fit score:", result.fit_score)
print("\nMatching skills:")
for s in result.matching_skills:
    print(" -", s)
print("\nMissing skills:")
for s in result.missing_skills:
    print(" -", s)
print("\nSummary:", result.summary)

letter_prompt = ChatPromptTemplate.from_messages([
    ("system", "You write short, honest internship cover letters. Use only the skills the candidate listed. Never claim experience they did not state. If the job needs something they lack, show willingness to learn instead of pretending. Keep it under 200 words."),
    ("human", "JOB DESCRIPTION:\n{job}\n\nCANDIDATE SKILLS:\n{skills}"),
])

letter_chain = letter_prompt | llm | StrOutputParser()

letter = letter_chain.invoke({"job": job, "skills": skills})
print("\n--- Cover letter draft ---\n")
print(letter)