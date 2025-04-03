def is_question(prompt: str) -> bool:
    return prompt.strip().endswith("?")