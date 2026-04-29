from langchain_anthropic import ChatAnthropic
from ..config import ANTHROPIC_API_KEY, CLAUDE_MODEL

def get_claude_llm():
    return ChatAnthropic(
        api_key=ANTHROPIC_API_KEY,
        model=CLAUDE_MODEL,
        temperature=0.2,
        max_tokens=1024
    )