# AI Interview Assistant

An intelligent interview preparation tool powered by Google's Gemini AI that provides real-time feedback on interview responses and helps you improve your interview skills.

## Demo
Watch the demo on YouTube: [AI Interview Assistant Demo](https://youtu.be/2btoXXkE9K0)

## Features

- 🤖 AI-powered interview questions generation
- 🎙️ Speech-to-text input support
- 📝 Real-time answer analysis and feedback
- 💡 Intelligent feedback on response quality
- 🎯 Technical accuracy assessment
- 📊 Performance tracking and improvement suggestions
- 🔄 Streamlined interview flow with organized responses
- 🎓 Model answers for learning and improvement
- 🏗️ **NEW**: Modular architecture with separation of concerns
- 📋 **NEW**: Comprehensive logging and error handling
- 🧪 **NEW**: Unit testing framework
- ⚡ **NEW**: Improved performance and reduced rerun loops

## Setup

1. Clone the repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
   This will install all required packages, including:
   - Streamlit for the web interface
   - Google Generative AI for intelligent responses
   - SpeechRecognition for voice input
   - PyAudio for microphone support
   - Other data processing and visualization libraries

3. Create a `.env` file with your Google AI API key:
   ```
   GOOGLE_API_KEY=your_api_key_here
   ```

4. Run the application:
   ```bash
   streamlit run app.py
   ```

### Voice Input Setup
For speech-to-text functionality:
- Ensure you have a working microphone
- Grant microphone permissions when prompted
- Click the microphone button to start recording your answer
- Speak clearly and the system will transcribe your response

## Project Structure

```
ai_interview_assistant/
├── app.py                      # Main application entry point (refactored)
├── requirements.txt            # Project dependencies
├── README.md                  # Documentation
├── .env.example               # Environment configuration example
├── tests/                     # Unit tests
│   ├── __init__.py
│   └── test_session_manager.py
└── src/
    ├── components/            # UI components
    │   ├── audio_input.py     # Speech-to-text component
    │   ├── custom_text_input.py # Custom text input component
    │   └── dashboard.py       # Analytics and metrics dashboard
    ├── controllers/           # Application controllers
    │   ├── __init__.py
    │   └── interview_controller.py # Interview flow controller
    ├── services/              # Business logic services
    │   ├── __init__.py
    │   ├── ai_service.py      # AI operations service
    │   └── session_manager.py # Session state management
    ├── ui/                    # User interface management
    │   ├── __init__.py
    │   └── ui_manager.py      # UI rendering and styling
    └── utils/                 # Utility functions
        ├── config.py          # Configuration and constants
        ├── helpers.py         # Common utility functions
        ├── interview_analyzer.py # Interview analysis logic
        ├── metrics_calculator.py # Metrics calculation
        └── logging_config.py  # Logging configuration
```

## Usage

1. Select the position you're interviewing for
2. Choose the type of question (technical, behavioral, problem-solving)
3. Generate interview questions
4. Provide your answers
5. Receive detailed feedback and suggestions for improvement

## Analysis Metrics

- Response Quality: Evaluates the completeness and relevance of your answers
- Technical Accuracy: Assesses the correctness of technical responses
- Communication Structure: Analyzes the organization and clarity of your written responses
