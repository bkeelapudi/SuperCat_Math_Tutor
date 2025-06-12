# Math Q&A Slack Bot (Python)

A simple Slack bot that provides expert math tutoring for your team using the Strands Agents SDK. This bot automatically detects math questions in channels and provides step-by-step solutions.

## Features

- Automatically detects math questions in Slack channels
- Provides detailed, step-by-step solutions
- Responds in threads to keep channels clean
- Supports a wide range of math topics:
  - Algebra
  - Calculus
  - Geometry
  - Probability
  - Statistics
  - Trigonometry
  - Number theory

## How It Works

1. Post any math question in a Slack channel where the bot is present
2. The bot automatically detects math questions and responds with a solution
3. Get step-by-step explanations to help understand the concepts

## Example Questions

- "What is the derivative of x^2 * sin(x)?"
- "Solve the equation 3x + 5 = 17"
- "Find the area of a circle with radius 5"
- "What is the formula for the quadratic equation?"
- "Calculate the probability of getting exactly 3 heads in 10 coin flips"

## Installation

1. Clone this repository
2. Run the installation script:
   ```bash
   ./install.sh
   ```
   This will:
   - Create a Python virtual environment
   - Install required dependencies
   - Create a `.env` file from the template

3. Edit the `.env` file with your Slack and AWS credentials

4. Start the bot:
   ```bash
   source venv/bin/activate
   python src/main.py
   ```

## Slack App Setup

1. Create a new Slack app at https://api.slack.com/apps
2. Add the following Bot Token Scopes:
   - `app_mentions:read`
   - `channels:history`
   - `channels:read`
   - `chat:write`
   - `reactions:write`
3. Enable Socket Mode
4. Install the app to your workspace
5. Copy the Bot Token, Signing Secret, and App Token to your `.env` file

## Development

For development, you may want to install additional tools:
```bash
pip install pytest black flake8
```

## Configuration

The bot is configured in the `src/main.py` file. You can modify:

- The system prompt for the math tutor
- Math question detection patterns
- Response formatting
- Slack event handling

## Technologies Used

- [Strands Agents SDK](https://github.com/strands-agents/sdk-python)
- [Strands Agents Tools](https://github.com/strands-agents/tools)
- Amazon Bedrock Claude for AI capabilities (default)
- Slack Bolt SDK for Slack integration
- Python 3.10+

## License

MIT
