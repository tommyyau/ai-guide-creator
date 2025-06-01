# AI Guide Creator

An AI-powered guide creation system using CrewAI that generates comprehensive, well-structured guides on any topic with proper markdown formatting and observability through Arize Phoenix.

## Features

- 🤖 **AI-Powered Content Generation**: Uses CrewAI with content writer and reviewer agents
- 📝 **Clean Markdown Output**: Properly formatted guides with correct heading hierarchy
- 🔍 **Observability**: Integrated with Arize Phoenix for monitoring and debugging
- 🎯 **Audience-Specific**: Supports beginner, intermediate, and advanced content levels
- 📊 **Structured Process**: Outline creation → Content writing → Review → Compilation

## Installation

Ensure you have Python >=3.10 <3.13 installed on your system. This project uses [UV](https://docs.astral.sh/uv/) for dependency management.

First, if you haven't already, install uv:

```bash
pip install uv
```

Next, navigate to your project directory and install the dependencies:

```bash
crewai install
```

## Configuration

### Required: OpenAI API Key

Add your OpenAI API key to a `.env` file:

```bash
cp env.example .env
# Edit .env and add your OPENAI_API_KEY
```

### Optional: Phoenix Observability

To enable observability with Arize Phoenix (free hosted version):

1. **Sign up** at [https://app.phoenix.arize.com](https://app.phoenix.arize.com)
2. **Get your API key** from the Phoenix dashboard
3. **Add to your `.env` file**:
   ```bash
   PHOENIX_API_KEY=your_phoenix_api_key_here
   ```

With Phoenix enabled, you'll get:
- 📊 Real-time monitoring of your AI agents
- 🔍 Detailed traces of CrewAI execution
- 📈 Performance metrics and debugging insights
- 🎯 LLM call tracking and analysis

## Running the Project

To create a guide, run:

```bash
crewai run
```

The program will ask for:
1. **Topic**: What you want to create a guide about
2. **Audience Level**: beginner, intermediate, or advanced

**Note**: You may not see your typing in the terminal, but your input is being recorded. Just type your answer and press Enter.

## Output

The system generates:
- `output/guide_outline.json` - The structured outline
- `output/complete_guide.md` - Your complete guide in clean markdown format

## Project Structure

```
guide_creator_flow/
├── src/guide_creator_flow/
│   ├── main.py                 # Main flow logic
│   ├── phoenix_config.py       # Phoenix observability setup
│   └── crews/content_crew/     # CrewAI agents and tasks
├── output/                     # Generated guides
└── README.md
```

## Observability Dashboard

When Phoenix is enabled, visit [https://app.phoenix.arize.com](https://app.phoenix.arize.com) to see:
- Agent execution traces
- LLM performance metrics
- Content generation pipeline analysis
- Error tracking and debugging

## Support

For support, questions, or feedback:

- Visit [CrewAI documentation](https://docs.crewai.com)
- Check [Arize Phoenix docs](https://docs.arize.com/phoenix)
- [CrewAI GitHub repository](https://github.com/joaomdmoura/crewai)

Let's create comprehensive guides with the power of AI and observability!
