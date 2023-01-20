import datetime
from datetime import date
from aiogram import Bot, types
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from aiogram.dispatcher import Dispatcher, FSMContext
from aiogram.utils import executor
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup

start_date = date(2023, 1, 2)
users1 = ['Игорь', 'Евгений']
users2 = ['Илья', 'YALW']

bot = Bot(token='5963586192:AAEgtVge2OOon91Kf60siKD7o03PT8LF7PE')
dp = Dispatcher(bot=bot)


def get_keyboard() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add(KeyboardButton('Смена'), KeyboardButton('Бросить кость'))
    return kb


class ClientState(StatesGroup):
    smena = State()


@dp.message_handler(commands=['start'])
async def start_cmd(message: types.Message):
    user_name = message.from_user.first_name
    await message.reply(f'Здарова {user_name}', reply_markup=get_keyboard())


@dp.message_handler(Text(equals='Смена'))
async def smena(message: types.Message):
    await ClientState.smena.set()
    await message.answer('Введи дату (дд.мм.гг)')


@dp.message_handler(Text(equals='Бросить кость'))
async def smena(message: types.Message):
    await message.answer_dice()


@dp.message_handler(state=ClientState.smena)
async def calculate_date(message: types.Message, state: FSMContext):
    user_name = message.from_user.first_name
    try:
        if user_name in users1 or users2:
            str_date = message.text
            current_date = datetime.datetime.strptime(str_date, '%d.%m.%y').date()
            count_days = current_date - start_date
            diff = count_days.days
            sign = diff % 28
            if user_name in users1:
                if sign <= 14:
                    await message.reply('Ты в первой смене, лох!')
                else:
                    await message.reply('Ты во вторую! Возрадуйся!')
            if user_name in users2:
                if sign <= 14:
                    await message.reply('Ты во вторую! Возрадуйся!')
                else:
                    await message.reply('Ты в первую, лох!')
    except ValueError:
        await message.reply('Некорректная дата')
    await state.finish()


@dp.message_handler()
async def all_message(message: types.Message):
    user_name = message.from_user.first_name
    await message.reply(f'{user_name} лох!')
    print(message.from_user.first_name, message.from_user.id, message.text)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
