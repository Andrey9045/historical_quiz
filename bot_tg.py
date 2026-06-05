import os
import argparse
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Updater, CallbackContext, CommandHandler, MessageHandler, Filters, ConversationHandler, RegexHandler
from keyboards import control_buttons
import redis


from service import checking_answer, get_random_question_answer, clearing_answer, create_answers_questions 


QUESTION, ANSWER, PASS = range(3)


def start(update: Update, context: CallbackContext):
	context.bot.send_message(chat_id=update.effective_chat.id, text='Привет) Нажми на "Новый вопрос"', reply_markup=control_buttons())
	return QUESTION

def handle_new_question_request(update: Update, context: CallbackContext):
    text = update.message.text
    user_id = update.effective_user.id
    redis_client = context.bot_data['redis']
    path = context.bot_data['path']
    question, answer = get_random_question_answer(path)
    redis_client.set(f"Вопрос {user_id}", question)
    redis_client.set(f"Ответ {user_id}", answer)
    context.bot.send_message(chat_id=update.effective_chat.id, text=question, reply_markup=control_buttons())
    return ANSWER

def handle_solution_attempt(update: Update, context: CallbackContext):
    text = update.message.text
    user_id = update.effective_user.id
    redis_client = context.bot_data['redis']
    answer = redis_client.get(f"Ответ {user_id}")
    if not checking_answer(text, answer):
        context.bot.send_message(chat_id=update.effective_chat.id, text="Ответ не верный, попробуй еще раз)", reply_markup=control_buttons())
        return ANSWER
    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text="Совершенно верно, бери новый вопрос)", reply_markup=control_buttons())
        return QUESTION

def show_correct_answer(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    redis_client = context.bot_data['redis']
    path = context.bot_data['path']
    answer = redis_client.get(f"Ответ {user_id}")
    context.bot.send_message(chat_id=update.effective_chat.id, text=answer, reply_markup=control_buttons())
    question, answer = get_random_question_answer(path)
    redis_client.set(f"Вопрос {user_id}", question)
    redis_client.set(f"Ответ {user_id}", answer)
    context.bot.send_message(chat_id=update.effective_chat.id, text=question, reply_markup=control_buttons())
    return ANSWER

def cancel():
    pass


if __name__ == '__main__':
    load_dotenv()
    tg_token = os.environ['TG_TOKEN']
    redis_host = os.environ['REDIS_HOST']
    redis_port = os.environ['REDIS_PORT']
    redis_password = os.environ['REDIS_PASSWORD']
    parser = argparse.ArgumentParser(
        description='Имя файла с вопосами'
    )
    parser.add_argument('filename', help='Имя файла с вопросами')
    args = parser.parse_args()
    filename = args.filename
    r = redis.Redis(
        host=redis_host,
        port=redis_port,
        password=redis_password,
        decode_responses=True)
    r.ping()
    updater = Updater(token=tg_token, use_context=True)
    dp = updater.dispatcher
    dp.bot_data['redis'] = r
    dp.bot_data['filename'] = filename
    conv_handler = ConversationHandler(
    	entry_points=[CommandHandler('start', start)],
    	states={
    	    QUESTION: [RegexHandler('Новый вопрос', handle_new_question_request)],
    	    ANSWER: [
                RegexHandler('Сдаться', show_correct_answer),
                MessageHandler(Filters.text, handle_solution_attempt)
            ],
    	},
        fallbacks=[CommandHandler('cancel', cancel)],
    )
    dp.add_handler(conv_handler)

    updater.start_polling()
    updater.idle()