import random
import re

def create_answers_questions():
    name_fiels = ['1vs1200.txt']
    with open(f'quiz/{name_fiels[0]}', 'r', encoding="KOI8-R") as my_file:
    	content = my_file.read()
    blocks = content.split('\n\n')
    blocks = [block.strip() for block in blocks if block.strip()]
    start_idx = 0
    for i, item in enumerate(blocks):
    	if "Вопрос" in item:
    	    start_idx = i
    	    break
    blocks = blocks[start_idx:]
    filtered = [block for block in blocks if not("Автор:" in block or "Источник:" in block)]
    answer_question = {}
    for item in range(0, len(filtered)-1, 2):
        q_block = filtered[item]
        a_block = filtered[item + 1]
        if "Вопрос" in q_block and "Ответ" in a_block:
        	key = q_block.strip()
        	values = a_block.strip()
        	answer_question[key] = values
    return answer_question


def clearing_answer(answer):
    answer = re.sub(r'^Ответ:\s*', '', answer, flags=re.IGNORECASE)
    text = re.sub(r'\s*\([^)]*\)', '', answer)
    parts = text.split('.', 1)
    result = parts[0] if parts else text
    print(result)
    return result.strip().lower()

def get_random_question_answer():
    answer_question = create_answers_questions()
    question, answer = random.choice(list(answer_question.items()))
    answer = clearing_answer(answer)
    return question, answer

def checking_answer(text, answer):
	if text.strip().lower()==answer:
		return True
	else:
		return False
