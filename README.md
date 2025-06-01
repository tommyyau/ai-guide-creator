# 🤖 AI Guide Creator

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![CrewAI](https://img.shields.io/badge/CrewAI-0.121.1+-green.svg)](https://docs.crewai.com)
[![Phoenix](https://img.shields.io/badge/Phoenix-10.5.0+-orange.svg)](https://phoenix.arize.com)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

An AI-powered guide creation system using CrewAI that generates comprehensive, well-structured guides on any topic with proper markdown formatting and observability through Arize Phoenix.

## ✨ Features

- 🤖 **AI-Powered Content Generation**: Uses CrewAI with specialized content writer and reviewer agents
- 📝 **Clean Markdown Output**: Properly formatted guides with correct heading hierarchy
- 🔍 **Real-time Observability**: Integrated with Arize Phoenix for monitoring and debugging
- 🎯 **Audience-Specific**: Supports beginner, intermediate, and advanced content levels
- 📊 **Structured Process**: Outline creation → Content writing → Review → Compilation
- 🔄 **Multi-Agent Collaboration**: Content writer and reviewer agents work together
- 🛠️ **Easy Configuration**: Simple environment-based setup

## 🚀 Quick Start

### Prerequisites

- Python 3.10 or higher
- OpenAI API key
- (Optional) Arize Phoenix account for observability

### Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/tommyyau/ai-guide-creator.git
   cd ai-guide-creator/guide_creator_flow
   ```

2. **Install dependencies**:
   ```bash
   # Using uv (recommended)
   uv sync
   
   # Or using pip
   pip install -e .
   ```

3. **Configure environment**:
   ```bash
   cp env.example .env
   # Edit .env and add your API keys
   ```

4. **Run your first guide**:
   ```bash
   crewai run
   ```

## ⚙️ Configuration

### Required: OpenAI API Key

Add your OpenAI API key to the `.env` file:

```bash
OPENAI_API_KEY=your_openai_api_key_here
```

### Optional: Phoenix Observability

To enable real-time monitoring with Arize Phoenix:

1. **Sign up** at [https://app.phoenix.arize.com](https://app.phoenix.arize.com) (free)
2. **Get your API key** from the Phoenix dashboard
3. **Add to your `.env` file**:
   ```bash
   PHOENIX_API_KEY=your_phoenix_api_key_here
   PHOENIX_COLLECTOR_ENDPOINT=https://app.phoenix.arize.com/v1/traces
   PHOENIX_PROJECT_NAME=ai-guide-creator
   ```

With Phoenix enabled, you'll get:
- 📊 Real-time monitoring of your AI agents and workflows
- 🔍 Detailed traces of CrewAI execution and agent collaboration
- 💰 **Token usage and cost tracking** for all OpenAI API calls
- ⏱️ **Performance metrics** including latency and response times
- 📈 Performance trends and debugging insights
- 🎯 **Complete LLM call visibility** with input/output token counts
- 🚨 Error tracking and alert capabilities

## 📖 Usage

### Basic Usage

```bash
# Run the guide creator
crewai run

# Or use the direct command
guide-creator
```

The program will prompt you for:
1. **Topic**: What you want to create a guide about
2. **Audience Level**: `beginner`, `intermediate`, or `advanced`

**Note**: You may not see your typing in the terminal, but your input is being recorded. Just type your answer and press Enter.

### Example Session

```
=== Create Your Comprehensive Guide ===

What topic would you like to create a guide for? Python programming
Who is your target audience? (beginner/intermediate/advanced) beginner

Creating a guide on Python programming for beginner audience...
```

### Output

The system generates:
- `output/guide_outline.json` - The structured outline
- `output/complete_guide.md` - Your complete guide in clean markdown format

## 🏗️ Project Structure

```
ai-guide-creator/
├── src/guide_creator_flow/
│   ├── main.py                 # Main flow logic
│   ├── phoenix_config.py       # Phoenix observability setup
│   └── crews/content_crew/     # CrewAI agents and tasks
│       ├── content_crew.py     # Crew definition
│       └── config/             # Agent and task configurations
├── tests/                      # Test suite
│   ├── test_phoenix.py         # Phoenix configuration tests
│   └── run_tests.py           # Test runner
├── output/                     # Generated guides
├── .env.example               # Environment template
└── README.md
```

## 🧪 Testing

Run the test suite to verify your configuration:

```bash
# Run all tests
python tests/run_tests.py

# Test Phoenix configuration specifically
python tests/test_phoenix.py
```

## 🔍 Observability Dashboard

When Phoenix is enabled, visit [https://app.phoenix.arize.com](https://app.phoenix.arize.com) to see:

- **Agent Execution Traces**: How your AI agents collaborate step-by-step
- **Token Usage Metrics**: Real-time input/output token counts for each LLM call
- **Cost Tracking**: Detailed cost breakdown per section and total guide generation
- **Performance Analytics**: Response times, latency trends, and throughput metrics
- **Content Generation Pipeline**: Complete workflow visibility from outline to final guide
- **Error Tracking & Debugging**: Identify and debug issues when they occur
- **Scalability Insights**: Monitor how performance changes with guide complexity
- **Usage Patterns**: Track which topics/audiences require more resources

## 🛠️ Development

### Setting up Development Environment

```bash
# Install with development dependencies
uv sync --extra dev

# Or with pip
pip install -e ".[dev]"
```

### Code Quality Tools

```bash
# Format code
black src/ tests/

# Sort imports
isort src/ tests/

# Lint code
flake8 src/ tests/
```

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=guide_creator_flow
```

## 🐛 Troubleshooting

### Common Issues

**1. "Import 'crewai' could not be resolved"**
- Ensure your IDE is using the correct Python interpreter
- Activate your virtual environment: `source .venv/bin/activate`

**2. Phoenix not showing traces**
- Verify your `PHOENIX_API_KEY` is set correctly
- Check the Phoenix dashboard at https://app.phoenix.arize.com
- Run `python tests/test_phoenix.py` to verify configuration

**3. Input not visible during typing**
- This is normal behavior with `crewai run`
- Your input is being captured even if not displayed
- Just type and press Enter

**4. OpenAI API errors**
- Verify your `OPENAI_API_KEY` is valid
- Check your OpenAI account has sufficient credits
- Ensure the API key has the necessary permissions

### Getting Help

- 📚 [CrewAI Documentation](https://docs.crewai.com)
- 🔍 [Arize Phoenix Docs](https://docs.arize.com/phoenix)
- 🐛 [Report Issues](https://github.com/tommyyau/ai-guide-creator/issues)

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [CrewAI](https://crewai.com) for the multi-agent framework
- [Arize Phoenix](https://phoenix.arize.com) for observability platform
- [OpenAI](https://openai.com) for the language models

---

**Built with ❤️ using CrewAI and Phoenix**

*Create comprehensive guides with the power of AI and observability!*
