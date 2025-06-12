#!/usr/bin/env python3
"""
Math Q&A Slack Bot using Strands Agents SDK
"""
import os
import sys
import logging
import re
from dotenv import load_dotenv
from strands import Agent, tool
from strands_tools import calculator

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# Define the system prompt for the math tutor
MATH_TUTOR_SYSTEM_PROMPT = """
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

# Define a function to detect math questions
def is_math_question(text):
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
        if re.search(pattern, text, re.IGNORECASE):
            return True
    
    return False

@tool
def math_tutor(query: str) -> str:
    """
    Process and respond to math-related queries using a specialized math agent.
    
    Args:
        query: A mathematical question or problem from the user
        
    Returns:
        A detailed mathematical answer with explanations and steps
    """
    # Format the query for the math agent with clear instructions
    formatted_query = f"Please solve the following mathematical problem, showing all steps and explaining concepts clearly: {query}"
    
    try:
        logger.info("Processing math question")
        # Create the math agent with calculator capability
        math_agent = Agent(
            system_prompt=MATH_TUTOR_SYSTEM_PROMPT,
            tools=[calculator],
        )
        agent_response = math_agent(formatted_query)
        text_response = str(agent_response)

        if len(text_response) > 0:
            return text_response

        return "I apologize, but I couldn't solve this mathematical problem. Please check if your query is clearly stated or try rephrasing it."
    except Exception as e:
        # Return specific error message for math processing
        logger.error(f"Error processing math query: {e}", exc_info=True)
        return f"Error processing your mathematical query: {str(e)}"

def setup_slack_bot():
    """
    Set up and run the Slack bot
    """
    try:
        from slack_bolt import App
        from slack_bolt.adapter.socket_mode import SocketModeHandler
        
        # Initialize the Slack Bolt app
        app = App(
            token=os.environ.get("SLACK_BOT_TOKEN"),
            signing_secret=os.environ.get("SLACK_SIGNING_SECRET")
        )
        
        # Create the math agent
        math_agent = Agent(
            system_prompt=MATH_TUTOR_SYSTEM_PROMPT,
            tools=[calculator],
        )
        
        @app.event("message")
        def handle_message_events(event, say):
            """Handle message events in channels"""
            # Skip messages from bots
            if event.get("bot_id"):
                return
                
            # Get the message text
            message_text = event.get("text", "")
            
            # Check if it's a math question
            if is_math_question(message_text):
                # Send a "thinking" message
                thinking_message = say(
                    text=":thinking_face: Analyzing math question...",
                    thread_ts=event.get("ts")
                )
                
                try:
                    # Process the math question
                    formatted_query = f"Please solve the following mathematical problem, showing all steps and explaining concepts clearly: {message_text}"
                    response = math_agent(formatted_query)
                    
                    # Send the response in a thread
                    say(
                        text=str(response),
                        thread_ts=event.get("ts")
                    )
                except Exception as e:
                    # Send error message
                    say(
                        text=f"I'm sorry, I encountered an error while solving this math problem: {str(e)}",
                        thread_ts=event.get("ts")
                    )
        
        @app.event("app_mention")
        def handle_app_mention_events(event, say):
            """Handle app mention events"""
            # Get the message text (remove the app mention)
            message_text = event.get("text", "")
            # Remove the app mention part
            message_text = re.sub(r'<@[A-Z0-9]+>', '', message_text).strip()
            
            if not message_text:
                say(
                    text="Hello! I'm a math tutor bot. Ask me any math question, and I'll help solve it step by step.",
                    thread_ts=event.get("ts")
                )
                return
                
            # Always process app mentions as potential math questions
            try:
                # Send a "thinking" message
                say(
                    text=":thinking_face: Analyzing math question...",
                    thread_ts=event.get("ts")
                )
                
                # Process the math question
                formatted_query = f"Please solve the following mathematical problem, showing all steps and explaining concepts clearly: {message_text}"
                response = math_agent(formatted_query)
                
                # Send the response in a thread
                say(
                    text=str(response),
                    thread_ts=event.get("ts")
                )
            except Exception as e:
                # Send error message
                say(
                    text=f"I'm sorry, I encountered an error while solving this math problem: {str(e)}",
                    thread_ts=event.get("ts")
                )
        
        # Start the app
        logger.info("Starting Math Q&A Slack Bot...")
        handler = SocketModeHandler(app, os.environ.get("SLACK_APP_TOKEN"))
        handler.start()
        
    except Exception as e:
        logger.error(f"Failed to initialize Slack bot: {e}", exc_info=True)
        sys.exit(1)

if __name__ == "__main__":
    setup_slack_bot()
