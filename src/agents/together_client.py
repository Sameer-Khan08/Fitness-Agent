from together import Together

try:
    from src.config.settings import TOGETHER_API_KEY
except Exception:
    TOGETHER_API_KEY = None


TEXT_MODEL = "MiniMaxAI/MiniMax-M3"


def generate_together_text(
    system_prompt: str,
    user_prompt: str,
    temperature: float = 0.4,
    max_tokens: int = 900,
) -> str:
    """
    Generate text using Together AI.
    """

    if not TOGETHER_API_KEY:
        return (
            "AI explanation is unavailable because TOGETHER_API_KEY is missing. "
            "The rule-based plan is still available."
        )

    try:
        client = Together(api_key=TOGETHER_API_KEY)

        response = client.chat.completions.create(
            model=TEXT_MODEL,
            messages=[
                {
                    "role": "system",
                    "content": system_prompt,
                },
                {
                    "role": "user",
                    "content": user_prompt,
                },
            ],
            temperature=temperature,
            max_tokens=max_tokens,
        )

        return response.choices[0].message.content

    except Exception as e:
        return f"AI explanation failed safely. Error: {str(e)}"