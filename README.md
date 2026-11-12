**AI RESPONSE EVALUATOR**

A Python prototype that uses a locally running language model through Ollama to evaluate AI-generated responses against a user prompt.

The evaluator requests structured results, validates them with Pydantic, and scores several aspects of response quality. It is a learning project exploring LLM-as-a-judge evaluation, not a production-grade fact checker.
Features
- Generates an AI response and evaluates it using Ollama's chat() API.
- Uses a configurable system prompt and a 1–5 scoring rubric.
- Evaluates instruction following, factual accuracy, relevance, completeness, and overall quality.
- Requests JSON matching a Pydantic schema and validates the returned data.
- Handles empty responses, validation errors, connection failures, and Ollama response errors.
- Supports controlled testing by substituting a fixed response for the generated response.

Requirements:

- Python 3.10 or newer
- Ollama installed and running locally
- The qwen3.5:4b model available in Ollama
- Python packages: ollama, pydantic, and httpx

Usage:

Run the evaluator from the project directory:
python main.py
The script sends a user prompt to the model, then asks the model to evaluate the generated response. The evaluation is validated against the EvaluationResult Pydantic model and printed to the terminal.