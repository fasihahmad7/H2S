# AI Interview Assistant

An intelligent interview preparation tool powered by Google's Gemini AI that provides real-time feedback on interview responses and helps you improve your interview skills.

## Demo
Watch the demo on YouTube: [AI Interview Assistant Demo](https://youtu.be/2btoXXkE9K0)

## Features

- 🤖 AI-powered interview questions generation
- 📝 Real-time answer analysis and feedback
- 💡 Intelligent feedback on response quality
- 🎯 Technical accuracy assessment
- 📊 Performance tracking and improvement suggestions

## Setup

1. Clone the repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Create a `.env` file with your Google AI API key:
   ```
   GOOGLE_API_KEY=your_api_key_here
   ```
4. Run the application:
   ```bash
   streamlit run app.py
   ```

## Project Structure

```
ai_interview_assistant/
├── app.py              # Main application file
├── requirements.txt    # Project dependencies
├── README.md          # Documentation
└── src/
    ├── components/    # UI components
    │   └── dashboard.py
    ├── database/     # Data persistence
    │   └── db_manager.py
    └── utils/        # Utility functions
        ├── config.py
        ├── helpers.py
        └── interview_analyzer.py
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
