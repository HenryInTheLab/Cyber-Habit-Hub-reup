from google import genai

from ai.config import DEFAULT_MODEL, SYSTEM_INSTRUCTION
from ai.prompts import quiz_feedback_prompt, url_analysis_prompt
from ai.schemas import ChatbotResponse, QuizFeedback, UrlAnalysis
from backend.settings import GOOGLE_API_KEY

client = genai.Client(api_key=GOOGLE_API_KEY)

def generate_ai_response(prompt, schema=None, system_instruction=None, model=DEFAULT_MODEL):
    """
    Helper to get a parsed ai response as a JSON object using a given schema.
    """
    mime_type = "application/json" if schema is not None else "text/plain"
    response = client.models.generate_content(
        model=model,
        contents=prompt,
        config={
            "system_instruction": system_instruction,
            "response_mime_type": mime_type,
            "response_schema": schema,
        }
    )
    return response.parsed if schema is not None else response.text

def generate_chatbot_response(prompt, model=DEFAULT_MODEL):
    return generate_ai_response(
        prompt=prompt, 
        schema=ChatbotResponse,
        system_instruction=SYSTEM_INSTRUCTION,
        model=model,
    )

def generate_quiz_feedback(quiz, model=DEFAULT_MODEL):
    """
    Uses Gemini AI to generate improvement points for a quiz attempt.
    """
    return generate_ai_response(
        prompt=quiz_feedback_prompt(quiz), 
        schema=QuizFeedback,
        model=model,
    )

def generate_url_analysis(url, model=DEFAULT_MODEL):
    """
    Uses Gemini AI to analyze a URL and provide insights about its safety.
    """
    return generate_ai_response(
        prompt=url_analysis_prompt(url), 
        schema=UrlAnalysis, 
        model=model,
    )