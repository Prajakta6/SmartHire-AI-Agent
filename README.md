# SmartHire AI Agent

SmartHire AI Agent is a text-based mock interview assistant that evaluates candidate answers using a local LLM through Ollama. It simulates technical interviews, scores responses, and generates a final interview report saved under the `reports/` folder.

This project is designed to demonstrate practical AI agent workflows such as prompt engineering, LLM integration, answer evaluation, interview automation, and report generation.

## Features

- Full mock interview mode
- Topic-wise interview mode
- Question bank for technical topics
- LLM-based answer evaluation using local Ollama
- Score extraction and average performance calculation
- Interview history tracking
- Final report generation as a `.txt` file

## Tech Stack

- Python
- Ollama
- Llama 3 model
- `requests` for API communication
- Text-based console interface

## Project Structure

```text
SmartHire_AI_Agent/
├── README.md
├── main.py
├── interview_agent.py
├── llm_engine.py
├── questions.py
├── report_generator.py
├── requirements.txt
└── reports/
```

## File Overview

- `main.py` - Application entry point and interview menu
- `questions.py` - Question bank with topic-wise interview questions
- `llm_engine.py` - Connects to Ollama and sends prompts to the LLM
- `interview_agent.py` - Handles evaluation, scoring, and final report generation
- `report_generator.py` - Saves the final interview report to `reports/`
- `reports/` - Output folder for generated interview reports

## Prerequisites

Before running the project, make sure you have:

- Python 3.8 or newer
- [Ollama](https://ollama.com) installed
- A working local LLM model available, such as `llama3`

## Setup and Installation

1. Clone or download the project folder.
2. Open a terminal in the project directory.
3. Install Python dependencies:

```bash
pip install -r requirements.txt
```

4. Pull the Llama 3 model if it is not already installed:

```bash
ollama pull llama3
```

5. Start the Ollama server:

```bash
ollama serve
```

## Running the Application

From the project root, run:

```bash
python main.py
```

You will see a menu like this:

```text
Select Interview Mode
1. Start Full Interview
2. Start Topic-wise Interview
3. Exit
```

## How It Works

1. The user enters their name.
2. The app presents either all interview questions or questions from one chosen topic.
3. For each question, the user types an answer.
4. The answer is sent to the LLM for evaluation.
5. The model returns a score, strengths, missing points, improved answer, and suggestions.
6. The application tracks scores across the entire interview.
7. A final interview report is generated and saved in `reports/`.

## Example Workflow

```text
Enter Student name: Prajakta

Select Interview Mode
1. Start Full Interview
2. Start Topic-wise Interview
3. Exit
```

After answering questions, the program prints the evaluation and saves a report file such as:

```text
reports/SmartHire_AI_Agent_Prajakta_Interview_Report_16_11_2026_22_12_19.txt
```

## Troubleshooting

If the app shows a connection error, check the following:

- Ollama is installed and running
- The `llama3` model is downloaded
- Port `11434` is available
- The command `ollama serve` is active before running the app

## Notes

This project is intended for learning and demonstration. It uses a local model rather than a cloud API, which makes it suitable for offline experimentation and educational use.

## License

This project is provided for educational purposes and can be modified or extended as needed.
