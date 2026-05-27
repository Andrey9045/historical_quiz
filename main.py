import os
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Updater, CallbackContext, CommandHandler, MessageHandler, Filters


#name_fiels = ['1vs1200.txt']



#with open(f'quiz/{name_fiels[0]}', 'r', encoding="KOI8-R") as my_file:
#	content = my_file.read()
#blocks = content.split('\n\n')
#blocks = [block.strip() for block in blocks if block.strip()]
#start_idx = 0
#for i, item in enumerate(blocks):
#	if "Вопрос" in item:
#	    start_idx = i
#	    break
#blocks = blocks[start_idx:]
#filtered = [block for block in blocks if not("Автор:" in block or "Источник:" in block)]
#answer_question = {}
#for item in range(0, len(filtered)-1, 2):
#    q_block = filtered[item]
#    a_block = filtered[item + 1]
#    if "Вопрос" in q_block and "Ответ" in a_block:
#    	key = q_block.strip()
#    	values = a_block.strip()
#    	answer_question[key] = values
#print(answer_question)

def start(update: Update, context: CallbackContext):
	context.bot.send_message(chat_id=update.effective_chat.id, text='Привет')

def echo(update: Update, context: CallbackContext):
	context.bot.send_message(chat_id=update.effective_chat.id, text=update.message.text)

if __name__ == '__main__':
    load_dotenv()
    tg_token = os.environ['TG_TOKEN']
    updater = Updater(token=tg_token, use_context=True)
    dispatcher = updater.dispatcher
    start_handler = CommandHandler('start', start)
    echo_handler = MessageHandler(Filters.text & (~Filters.command), echo)
    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(echo_handler)

    updater.start_polling()
    updater.idle()