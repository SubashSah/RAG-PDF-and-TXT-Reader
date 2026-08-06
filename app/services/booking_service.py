import json

from langchain_core.prompts import ChatPromptTemplate

from app.schemas import BookingExtraction
from app.services.llm_service import generate_response

PROMPT = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
You are an information extraction assistant.

Your task is to determine whether the user's latest message is requesting an interview booking.

There are only two possible intents:

1. general_chat
2. book_interview

Always return ONLY a valid JSON object.

If the user is NOT requesting an interview booking, return exactly in this format:

{{
    "intent": "general_chat",
    "name": null,
    "email": null,
    "date": null,
    "time": null
}}

If the user IS requesting an interview booking, return exactly in this format:

{{
    "intent": "book_interview",
    "name": "<name or null>",
    "email": "<email or null>",
    "date": "<date or null>",
    "time": "<time or null>"
}}

Rules:
- Extract only information explicitly mentioned by the user.
- Do not guess missing fields.
- Use null for missing values.
- Do not include markdown.
- Do not include explanations.
- Do not return anything except the JSON object.
            """.strip(),
        ),
        (
            "human",
            "{question}",
        ),
    ]
)


def extract_booking(question: str) -> BookingExtraction:
    """
    Detect interview booking intent and extract booking details.
    """

    messages = PROMPT.format_messages(
        question=question,
    )

    response = generate_response(messages)

    response = response.strip()

    if response.startswith("```json"):
        response = response.replace("```json", "").replace("```", "").strip()
    elif response.startswith("```"):
        response = response.replace("```", "").replace("```", "").strip()

    data = json.loads(response)

    return BookingExtraction(**data)