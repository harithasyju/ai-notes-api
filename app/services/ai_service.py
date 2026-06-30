from google import genai

from app.config import settings

client = genai.Client(api_key=settings.GEMINI_API_KEY)


def summarize_note(title: str, content: str) -> str:
    prompt = f"""
    Summarize the following note clearly and concisely.

    Title: {title}

    Content:
    {content}

    Return only the summary.
    """

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
    )

    return response.text