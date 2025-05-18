from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import asyncio
from crud_functions import *

api = '7383476265:AAErU5wbb_7d4j9GVX-K96CrcqLQQcQ2z4k'
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())


ik = InlineKeyboardMarkup(resize_keyboard=True)
inline_button = InlineKeyboardButton(text='Рассчитать норму калорий', callback_data='calories')
inline_button_1 = InlineKeyboardButton(text='Формулы расчёта', callback_data='formulas')

ik.add(inline_button)
ik.add(inline_button_1)

inline_button_2 = InlineKeyboardButton(text='Product1', callback_data='product_buying')
inline_button_3 = InlineKeyboardButton(text='Product2', callback_data='product_buying')
inline_button_4 = InlineKeyboardButton(text='Product3', callback_data='product_buying')
inline_button_5 = InlineKeyboardButton(text='Product4', callback_data='product_buying')
by_ik = InlineKeyboardMarkup(resize_keyboard=True).row(inline_button_2,
                                                       inline_button_3, inline_button_4,
                                                       inline_button_5)

@dp.message_handler(text='Купить')
async def get_buying_list(message):
    users = get_all_products()
    for i in users:
        await message.answer(f'Название: {i[1]} | Описание: {i[2]} | Цена: {i[3]}')
        with open(f'files/{i[0]}.png', 'rb') as img:
            await message.answer_photo(img)
    await message.answer(text='Выберите продукт для покупки:', reply_markup=by_ik)

@dp.callback_query_handler(text="product_buying")
async def send_confirm_message(call):
    await call.message.answer('Поздравляю! Вы успешно купили продукт!')
    await call.answer()

@dp.message_handler(text='Рассчитать')
async def main_menu(message):
    await message.answer(text='Выберите опцию:', reply_markup=ik)


@dp.callback_query_handler(text='formulas')
async def get_formulas(call):
    await call.message.answer('Формула Миффлина-Сан Жеора – это одна из самых последних формул расчета '
                              'калорий для оптимального'
                      'похудения или сохранения нормального веса:' 
                      'для мужчин: 10 х вес (кг) + 6,25 x рост (см) – 5 х возраст (г) + 5;'
                      'для женщин: 10 x вес (кг) + 6,25 x рост (см) – 5 x возраст (г) – 161.')


kb = ReplyKeyboardMarkup(resize_keyboard=True)
button = KeyboardButton(text='Рассчитать')
kb.add(button)
button_1 = KeyboardButton(text='Информация')
kb.insert(button_1)
button_2 = KeyboardButton(text="Купить")
kb.add(button_2)

@dp.message_handler(text= 'Информация')
async def bot_inform(message):
    await message.answer('Данный бот создан учеником Urban University для практики в создании ТГ-ботов.')



class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()


@dp.callback_query_handler(text= 'calories')
async def set_age(call):
    print(f'Запущен алгоритм подсчета калорий. \nОжидаем "Возраст"')
    await call.message.answer(f'Введите свой возраст, пожалуйста:')
    await UserState.age.set()


@dp.message_handler(state=UserState.age)
async def set_growth(message, state):
    print(f'Возраст установлен: \n{message.text} \nОжидаем "Рост"')
    await state.update_data(age= message.text)
    await message.answer(f'Введите свой рост, пожалуйста:')
    await UserState.growth.set()



@dp.message_handler(state= UserState.growth)
async def set_weight(message, state):
    print(f'Установлен рост: \n{message.text} \nОжидаем "Вес"')
    await state.update_data(growth= message.text)
    await message.answer(f'Введите свой вес, пожалуйста:')
    await UserState.weight.set()


@dp.message_handler(state= UserState.weight)
async def send_calories(message, state):
    print(f'Вес установлен:\n{message.text}')
    await state.update_data(weight=message.text)
    data = await state.get_data()
    result_calories = (10 * int(data["weight"])) + (6.25 * int(data["growth"])) - (5 * int(data["age"])) + 5
    await message.answer(f'Ваша норма калорий: \n{result_calories}')
    print(f'Вычисления закончены: \n{result_calories}')
    await state.finish()


@dp.message_handler(text = ['Urban'])
async def rinat_message(message):
     print('Urban')
     await message.answer('Служебное сообщение')

@dp.message_handler(commands=['start'])
async def start(message):
      print('Начало работы бота. Всё ок.')
      await message.answer('Привет! Я бот помогающий твоему здоровью. '
                           '\nНажмите на кнопку "Рассчитать", чтобы посчитать '
                           'необходимое количество калорий', reply_markup=kb)

@dp.message_handler()
async def all_message(message):
    print('Введено случайное сообщение')
    await message.answer('Введите команду /start, чтобы начать общение.')



if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)