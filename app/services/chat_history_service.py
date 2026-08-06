import os

from dotenv import load_dotenv
from langchain_redis import RedisChatMessageHistory

load_dotenv()


def get_chat_history(session_id: str) -> RedisChatMessageHistory:
    """
    Return the Redis chat history for a session.
    """

    return RedisChatMessageHistory(
        session_id=session_id,
        redis_url=os.getenv("REDIS_URL"),
    )
