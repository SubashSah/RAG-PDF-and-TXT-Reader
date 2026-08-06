from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

from app.services.chat_history_service import get_chat_history
from app.services.llm_service import generate_response
from app.services.vector_store_service import retrieve_documents
from app.services.booking_service import extract_booking
from app.services.booking_db_service import save_booking

PROMPT = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
            You are a helpful AI assistant.

            Answer the user's question ONLY using the provided context.

            If the answer cannot be found in the context, say:

            "I couldn't find that information in the uploaded documents."

            Do not make up answers.
                        """.strip(),
        ),
        MessagesPlaceholder(variable_name="chat_history"),
        (
            "human",
            """
            Context:
            {context}

            Question:
            {question}
                        """.strip(),
        ),
    ]
)


def chat(session_id: str, question: str) -> str:
    """
    Execute the custom RAG pipeline.
    """

    booking = extract_booking(question)

    if booking.intent == "book_interview":

        if not all(
            [
                booking.name,
                booking.email,
                booking.date,
                booking.time,
            ]
        ):
            return (
                "To book an interview, please provide your "
                "name, email, preferred date and preferred time "
                "in a single message."
            )

        save_booking(
            name=booking.name,
            email=booking.email,
            date=booking.date,
            time=booking.time,
        )

        return (
            "Your interview has been booked successfully.\n\n"
            f"Name: {booking.name}\n"
            f"Email: {booking.email}\n"
            f"Date: {booking.date}\n"
            f"Time: {booking.time}"
        )

    documents = retrieve_documents(question)

    if not documents:
        return "Please upload a document before asking questions."

    context = "\n\n".join(document.page_content for document in documents)

    chat_history = get_chat_history(session_id)

    messages = PROMPT.format_messages(
        context=context,
        question=question,
        chat_history=chat_history.messages,
    )

    answer = generate_response(messages)

    chat_history.add_user_message(question)
    chat_history.add_ai_message(answer)
    return answer
