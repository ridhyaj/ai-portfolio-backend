from fastapi import FastAPI
from pydantic import BaseModel
from openai import OpenAI
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware
import os


load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # we’ll restrict later
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

client = OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1",
)

class Question(BaseModel):
    message: str

@app.get("/")
def root():
    return {"message": "AI Portfolio Backend Running"}

@app.post("/chat")
def chat(question: Question):
    try:
        response = client.chat.completions.create(
            model="groq/compound",  # Free Groq model
            messages=[
                {
                    "role": "system",
                    "content": "You are Ridhya's AI assistant. Answer professionally about her AI and full stack skills."
                },
                {
                    "role": "user",
                    "content": question.message
                }
            ],
        )

        return {
            "response": response.choices[0].message.content
        }

    except Exception as e:
        return {"error": str(e)}
