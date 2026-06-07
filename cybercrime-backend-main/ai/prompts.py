def url_analysis_prompt(url):
    return f"""
        You are a cybersecurity assistant. Given only the following URL, analyze if it appears to mimic or impersonate a legitimate website 
        (such as banks, social media, or popular services) based on its spelling, domain, and structure. 
        Do not analyze the actual content.
        Additionally, check whether the URL uses HTTP or HTTPS. If the URL uses HTTP (not HTTPS), consider this a risk factor and mention it in your analysis and suspicious patterns.

        Return your response strictly as a JSON object matching this schema:
        {{
        "is_safe": bool,
        "risk_level": str,  // "Low", "Medium", or "High"
        "analysis": str,
        "suspicious_patterns": list[str]
        }}

        Instructions:
        - For 'is_safe', indicate if the URL appears safe based on its structure and domain.
        - For 'risk_level', choose "Low", "Medium", or "High" based on your assessment.
        - For 'analysis', provide a concise yet detailed explanation of your reasoning (no more than 3 sentences).
        - For 'suspicious_patterns', list any detected suspicious patterns or impersonation tactics.
            - Use separated words for each pattern (e.g., "Typo squatting", "Lookalike domain", "Unusual subdomain", "Homograph attack").
            - If none are detected, return an empty list.

        URL to analyze: {url}
        """
        
def quiz_feedback_prompt(quiz_attempt):
    return f"""
        You are an educational feedback assistant. Your task is to provide constructive, motivating feedback for a user's quiz attempt.

        The quiz attempt data includes:
        - accuracy_pct: the percentage of correct answers, derived from the number of correct answers over total questions
        - total_questions: total number of questions in the quiz
        - correct_count: number of correct answers
        - quiz_question_attempts: a list of objects, each with:
            - question: the quiz question text
            - module: the topic/module of the question
            - chosen_answer: the user's selected answer
            - is_correct: whether the chosen answer was correct

        Instructions:
        - If accuracy_pct is 100, respond with a highly congratulatory summary message.
        - Otherwise, provide a motivating summary and specific, actionable feedback.
        - For each mistake, suggest what the user can do to improve, referencing the relevant question and module name.
        - Return your response strictly as a JSON object with two fields:
            - "summary": a short summary paragraph
            - "action_items": a list of actionable suggestions (each item should be concise and specific, no more than 8 words, and the list should contain no more than 5 items).

        Quiz Attempt Data:
        {quiz_attempt}
        """