import os
import random
import re

def create_answers_questions(filename):
    base_dir = "quiz"
    full_path = os.path.join(base_dir, filename)
    with open(full_path, 'r', encoding="KOI8-R") as my_file:
    	content = my_file.read()
    blocks = content.split('\n\n')
    blocks = [block.strip() for block in blocks if block.strip()]
    start_idx = 0
    for index, block in enumerate(blocks):
    	if "Вопрос" in block:
    	    start_idx = index
    	    break
    blocks = blocks[start_idx:]
    filtered = [block for block in blocks if not("Автор:" in block or "Источник:" in block)]
    answer_question = {}
    for index in range(0, len(filtered)-1, 2):
        q_block = filtered[index]
        a_block = filtered[index + 1]
        if "Вопрос" in q_block and "Ответ" in a_block:
        	key = q_block.strip()
        	values = a_block.strip()
        	answer_question[key] = values
    return answer_question


def normalize_answer(answer):
    answer = re.sub(r'^Ответ:\s*', '', answer, flags=re.IGNORECASE)
    text = re.sub(r'\s*\([^)]*\)', '', answer)
    parts = text.split('.', 1)
    cleaned_answer = parts[0] if parts else text
    return cleaned_answer.strip().lower()

def get_random_question_answer(questions_answers):
    question, answer = random.choice(list(questions_answers.items()))
    answer = normalize_answer(answer)
    return question, answer

def is_correct(text, answer):
	return  text.strip().lower() == answer
