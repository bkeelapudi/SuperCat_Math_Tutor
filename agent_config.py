"""
Strands Agent Configuration for Math Q&A Bot
"""
import re

def is_math_question(message):
    """
    Detect if a message contains a math question
    """
    # Check for common math question indicators
    math_patterns = [
        r'solve', r'calculate', r'find', r'what is', r'how much', r'equation',
        r'\d+\s*[\+\-\*\/\^\=\(\)]',  # Numbers with operators
        r'\d+\s*x\s*\d+',             # Multiplication with 'x'
        r'derivative', r'integral',    # Calculus terms
        r'algebra', r'geometry',       # Math subjects
        r'triangle', r'circle',        # Geometric shapes
        r'sin|cos|tan|log',            # Math functions
        r'\d+\s*\^\s*\d+',             # Exponents
        r'square root', r'√',          # Square roots
        r'\d+\s*\/',                   # Fractions
        r'\d+\s*\%'                    # Percentages
    ]
    
    for pattern in math_patterns:
        if re.search(pattern, message, re.IGNORECASE):
            return True
    
    return False

# Agent configuration
agent_config = {
    # Agent configuration
    "agent": {
        "name": "Math Tutor",
        "description": "A specialized bot that provides expert math tutoring. This bot answers math questions with step-by-step solutions.",
        "instructions": """
            You are an expert math tutor. Provide clear, step-by-step explanations for any math question.
            Include the final answer clearly marked. If appropriate, suggest alternative approaches or provide additional context
            about the mathematical concepts involved. If the question is unclear or not math-related, politely ask for clarification
            while staying in your role as a math tutor.
            
            Always format mathematical expressions properly. Use markdown formatting for equations when appropriate.
            
            Example topics you can help with:
            - Algebra
            - Calculus
            - Geometry
            - Probability
            - Statistics
            - Trigonometry
            - Number theory
        """
    },
    
    # Model configuration
    "model": {
        "provider": "bedrock",
        "name": "anthropic.claude-3-sonnet-20240229-v1:0",
        "parameters": {
            "temperature": 0.2,  # Lower temperature for more precise math answers
            "max_tokens": 1000
        }
    },
    
    # Slack integration configuration
    "slack": {
        # Channels the bot should monitor
        "channels": ["general", "random", "math-help"],
        
        # Events to listen for
        "events": ["message", "app_mention"],
        
        # Response settings
        "response_type": "thread",  # Respond in threads to keep channels clean
        
        # Custom message formatting
        "message_formatting": {
            "thinking": ":thinking_face: Analyzing math question...",
            "error": "I'm sorry, I encountered an error while solving this math problem. Please try again later."
        }
    }
}
