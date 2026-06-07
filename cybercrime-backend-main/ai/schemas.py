import enum

from pydantic import BaseModel


class ChatbotResponse(BaseModel):
    response: str
    follow_up_questions: list[str]

class QuizFeedback(BaseModel):
    summary: str
    action_items: list[str]
    
class RiskLevel(enum.Enum):
    Low = "Low"
    Medium = "Medium"
    High = "High"
    
class UrlAnalysis(BaseModel):
    is_safe: bool
    risk_level: RiskLevel 
    analysis: str  
    suspicious_patterns: list[str] 