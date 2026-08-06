import os

from dotenv import load_dotenv
from langchain_core.messages import BaseMessage
from langchain_groq import ChatGroq

load_dotenv()

llm = ChatGroq(
    model="llama-3.1-8b-instant",
    api_key=os.getenv("GROQ_API_KEY"),
    temperature=0,
)


def generate_response(messages: list[BaseMessage]) -> str:
    """
    Generate a response using the Groq LLM.
    """

    response = llm.invoke(messages)

    return response.content.strip()
