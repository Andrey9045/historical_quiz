import os
import argparse
from dotenv import load_dotenv
import vk_api as vk
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.utils import get_random_id
import redis

from receiving_questions_and_checking_answer import is_correct, get_random_question_answer, normalize_answer, create_answers_questions

def get_keyboard():
    keyboard = VkKeyboard(one_time=True)
    keyboard.add_button('Новый вопрос', color=VkKeyboardColor.PRIMARY)
    keyboard.add_line()
    keyboard.add_button('Сдаться', color=VkKeyboardColor.NEGATIVE)
    return keyboard

def send_message(vk_api, peer_id, text, keyboard=None):
    params = {
        'user_id': peer_id,
        'message': text,
        'random_id': get_random_id()
    }
    if keyboard:
        params['keyboard']=keyboard.get_keyboard()

    vk_api.messages.send(**params)

def handle_new_question_request(vk_api, peer_id, redis_client, questions_answers):
    question, answer = get_random_question_answer(questions_answers)
    redis_client.set(f"Вопрос {peer_id}", question)
    redis_client.set(f"Ответ {peer_id}", answer)
    send_message(vk_api, peer_id, question, get_keyboard())

def show_correct_answer(vk_api, peer_id, redis_client, questions_answers):
    answer = redis_client.get(f"Ответ {peer_id}")
    send_message(vk_api, peer_id, answer, get_keyboard())
    question, answer = get_random_question_answer(questions_answers)
    redis_client.set(f"Вопрос {peer_id}", question)
    redis_client.set(f"Ответ {peer_id}", answer)
    send_message(vk_api, peer_id, question, get_keyboard())

def handle_solution_attempt(vk_api, peer_id, redis_client, text):
    answer = redis_client.get(f"Ответ {peer_id}")
    if is_correct(text, answer):
        send_message(vk_api, peer_id, "Совершенно верно, бери новый вопрос)", get_keyboard())
    else:
        send_message(vk_api, peer_id, "Ответ не верный, попробуй еще раз)", get_keyboard())

def main():
    load_dotenv()
    vk_token = os.environ["VK_TOKEN"]
    redis_host = os.environ['REDIS_HOST']
    redis_port = os.environ['REDIS_PORT']
    redis_password = os.environ['REDIS_PASSWORD']
    parser = argparse.ArgumentParser(
        description = "Имя файла с вопросами"
    )
    parser.add_argument('filename', help='Введите имя файла с вопросами')
    args = parser.parse_args()
    filename = args.filename
    questions_answers = create_answers_questions(filename)
    redis_client = redis.Redis(
        host=redis_host,
        port=redis_port,
        password=redis_password,
        decode_responses=True)
    redis_client.ping()

    vk_session = vk.VkApi(token=vk_token)
    vk_api = vk_session.get_api()
    longpoll = VkLongPoll(vk_session)
    for event in longpoll.listen():
        if not (event.type == VkEventType.MESSAGE_NEW and event.to_me):
            continue
        text = event.text.strip()
        peer_id = event.peer_id
        if event.text == "Новый вопрос":
            handle_new_question_request(vk_api, peer_id, redis_client, questions_answers)
        elif event.text == "Сдаться":
            show_correct_answer(vk_api, peer_id, redis_client, questions_answers)
        else:
            handle_solution_attempt(vk_api, peer_id, redis_client, event.text)

if __name__ == '__main__':
    main()

