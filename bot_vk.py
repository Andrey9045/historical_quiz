import os
from dotenv import load_dotenv
import vk_api as vk
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.utils import get_random_id
import redis

from service import checking_answer, get_random_question_answer, clearing_answer, create_answers_questions

def get_keyboard():
    keyboard = VkKeyboard(one_time=True)
    keyboard.add_button('Новый вопрос', color=VkKeyboardColor.PRIMARY)
    keyboard.add_line()
    keyboard.add_button('Сдаться', color=VkKeyboardColor.NEGATIVE)
    return keyboard

def echo(event, vk_api, keyboard):
    vk_api.messages.send(
        user_id=event.user_id,
        message=event.text,
        random_id=random.randint(1, 1000),
        keyboard=keyboard.get_keyboard()
    )

def send_message(vk_api, peer_id, text, keyboard=None):
    params = {
        'user_id': peer_id,
        'message': text,
        'random_id': get_random_id()
    }
    if keyboard:
        params['keyboard']=keyboard.get_keyboard()

    vk_api.messages.send(**params)

def handle_new_question_request(vk_api, peer_id, redis_client):
    question, answer = get_random_question_answer()
    redis_client.set(f"Вопрос {peer_id}", question)
    redis_client.set(f"Ответ {peer_id}", answer)
    send_message(vk_api, peer_id, question, get_keyboard())

def show_correct_answer(vk_api, peer_id, redis_client):
    answer = redis_client.get(f"Ответ {peer_id}")
    send_message(vk_api, peer_id, answer, get_keyboard())
    question, answer = get_random_question_answer()
    redis_client.set(f"Вопрос {peer_id}", question)
    redis_client.set(f"Ответ {peer_id}", answer)
    send_message(vk_api, peer_id, question, get_keyboard())

def handle_solution_attempt(vk_api, peer_id, redis_client, text):
    answer = redis_client.get(f"Ответ {peer_id}")
    if not checking_answer(text, answer):
        send_message(vk_api, peer_id, "Ответ не верный, попробуй еще раз)", get_keyboard())
    else:
        send_message(vk_api, peer_id, "Совершенно верно, бери новый вопрос)", get_keyboard())

if __name__ == '__main__':
    load_dotenv()
    vk_token = os.environ["VK_TOKEN"]
    redis_host = os.environ['REDIS_HOST']
    redis_port = os.environ['REDIS_PORT']
    redis_password = os.environ['REDIS_PASSWORD']
    r = redis.Redis(
        host=redis_host,
        port=redis_port,
        password=redis_password,
        decode_responses=True)
    r.ping()

    vk_session = vk.VkApi(token=vk_token)
    vk_api = vk_session.get_api()
    longpoll = VkLongPoll(vk_session)
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            text = event.text.strip()
            peer_id = event.peer_id
            if event.text == "Новый вопрос":
                handle_new_question_request(vk_api, peer_id, r)
            elif event.text == "Сдаться":
                show_correct_answer(vk_api, peer_id, r)
            else:
                handle_solution_attempt(vk_api, peer_id, r, event.text)

            #    handle_new_question_request(event, vk_api, keyboard)
            #echo(event, vk_api, keyboard) 

