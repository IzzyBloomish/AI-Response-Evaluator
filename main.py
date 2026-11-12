from ollama import chat, ResponseError
from pydantic import BaseModel, Field, ValidationError
from typing import Literal
import httpx

class EvaluationResult(BaseModel):
    follows_instructions: Literal['Yes', 'No', 'Partially']
    factual_accuracy: int = Field(ge=1, le=5)
    relevance: int = Field(ge=1, le=5)
    completeness: int = Field(ge=1, le=5)
    overall_score: int = Field(ge=1, le=5)
    rationale: str



user_prompt = [{"role": "user", "content": "Name three European countries and their capitals."}]
user_prompt_extracted = user_prompt[0]['content']
instructions = """You are an AI evaluator.
You must rate the AI response following these criteria and considering this scoring rubric:
Scoring rubric (1-5):
1 = Very poor
2 = Poor
3 = Acceptable
4 = Good
5 = Excellent 
- Instruction following: Evaluate whether the response follows the user's explicit instructions, including format, structure, and constraints. Do not penalize factual errors here unless factual correctness is explicitly required.
- Factual accuracy: Evaluate whether the information provided is factually correct. Penalize incorrect claims, not missing information. Do not assume uncertain claims are true.
- Relevance: Is the response related to the prompt?
- Completeness: Evaluate whether the response includes all the information requested by the user. Penalize missing information, not incorrect facts.
- Overall quality: Rate the response on a scale from 1 to 5.
- Rationale: Justify each dimension's rating, especially scores below 5 or instruction-following ratings other than 'Yes'."""

try:
    
    response_bot = chat(model='qwen3.5:4b', messages=user_prompt)
    mock_response_bot = "France — Madrid, Germany — Berlin, Italy — Rome."
    response = chat(
    model='qwen3.5:4b',
    messages=[
        {"role": "system", "content": instructions},

        {"role": "user", "content": f"Prompt: {user_prompt_extracted}\n"
        f"AI Response: {response_bot.message.content}"
        }
    ],format=EvaluationResult.model_json_schema())
    if response.message.content:
        try:
            validated_eval = EvaluationResult.model_validate_json(response.message.content)
            print(validated_eval)
        except ValidationError as val_error:
            print(f"Error: {val_error}")
    else:
        print("The response is empty")
except httpx.ConnectError as conn_error:
    print(f"Error: {conn_error}")
except ConnectionError as connection_error:
    print(f"Error: {connection_error}")
except ResponseError as resp_error:
    print(f"Error: {resp_error}")
    if resp_error.status_code == 404:
        print("Error 404")


