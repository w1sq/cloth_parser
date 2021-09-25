# coding=utf8
import asyncio
from asyncio import events
import logging
import aiogram.utils.markdown as fmt
from datetime import datetime
from aiogram import Bot, Dispatcher, executor,types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types import InputTextMessageContent, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton, InlineQueryResultPhoto
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.filters import Text
from aiogram.types.bot_command import BotCommand
from aiogram.types.inline_query_result import InlineQueryResultArticle
from sqlite3 import IntegrityError
from db_data import db_session
from db_data.__all_models import Users
with open('key.txt','r') as file:
    API_KEY = file.readline()
logging.basicConfig(level=logging.INFO, filename='botlogs.log')
bot = Bot(token=API_KEY)
storage = MemoryStorage()
db_session.global_init()
dp = Dispatcher(bot, storage=storage)
print('Bot started')

def generate_inline_keyboard (*answer):
    keyboard = InlineKeyboardMarkup()
    temp_buttons = []
    for i in answer:
        temp_buttons.append(InlineKeyboardButton(text=str(i[0]), callback_data=str(i[1])))
    keyboard.add(*temp_buttons)
    return keyboard


async def set_commands(bot: Bot):
    commands = [
        BotCommand(command="/start", description="Запустить бота")
    ]
    await bot.set_my_commands(commands)

@dp.message_handler(commands=['remove'])
async def remove(message):
    if message.chat.username == 'artem_kokorev':
        db_sess = db_session.create_session()
        try:
            user = db_sess.query(Users).get(message.text.split()[-1])
        except Exception:
            await message.answer('Вы ввели неправильный тег пользователя, попробуйте снова')
            return
        db_sess.delete(user)
        db_sess.commit()
        db_sess.close()
        await message.answer('Вы успешно удалили пользователя')

@dp.message_handler(commands=['list'])
async def return_list(message):
    if message.chat.id == 0:
        db_sess = db_session.create_session()
        users = db_sess.query(Users).all()
        string = ''
        for user in users:
            string += user.name+' '
        db_sess.close()
        if string != '':
            await message.answer(string)
        else:
            await message.answer('Нет пользователей')

@dp.message_handler(commands=['start'])
async def start(message):
    try:
        user_name = message.chat.username
    except Exception:
        await message.answer('Создайте уникальный nickname телеграма чтобы воспользоваться ботом.')
        return
    db_sess = db_session.create_session()
    user = db_sess.query(Users).get(user_name)
    db_sess.close()
    if user:
        await message.answer(f'Добро пожаловать назад, {user_name}')
    else:
        await message.answer(f'Подожди пока тебя пустят')
        await bot.send_message('631874013', f'@{message.chat.username} хочет получить доступ к боту',reply_markup=generate_inline_keyboard(['Допустить',f'#pass {message.chat.id} {message.chat.username}']))
        
@dp.callback_query_handler(lambda call: True)
async def ans(call):
    message = call.message
    if call.data.startswith('#pass'):
        db_sess = db_session.create_session()
        user=Users(name=call.data.split()[2],telegram_id=call.data.split()[1])
        db_sess.add(user)
        db_sess.commit()
        db_sess.close()
        await bot.send_message(call.data.split()[1],'Администратор подтвердил вас')

async def send(text):
    db_sess = db_session.create_session()
    users = db_sess.query(Users).all()
    db_sess.close()
    for user in users:
        await bot.send_message(user.telegram_id, text, parse_mode='html')

#if __name__ == '__main__':
loop = asyncio.get_event_loop()
loop.run_until_complete(set_commands(bot))
loop.create_task(dp.start_polling())
#asyncio.ensure_future(dp.start_polling(), loop=loop)
#loop.run_until_complete(dp.start_polling())
