from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.dispatcher import FSMContext

TOKEN = "8170876051:AAEMyCrWJ4zpxIWdNqBBww4ecLWZ-743qJs"
bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())

kb = ReplyKeyboardMarkup(resize_keyboard=True)
kb_inline = InlineKeyboardMarkup()
inline_sale_kb = InlineKeyboardMarkup()

button_calculate = KeyboardButton(text='Расчитать')
button_info = KeyboardButton(text='Информация')
button_sale = KeyboardButton(text='Купить')
inline_button_calc = KeyboardButton(text='Рассчитать норму калорий', callback_data='calories')
inline_button_formula = KeyboardButton(text='Формулы расчёта', callback_data='formulas')
product1_in_but = KeyboardButton(text = 'Product1', callback_data='product_buying')
product2_in_but = KeyboardButton(text = 'Product2', callback_data='product_buying')
product3_in_but = KeyboardButton(text = 'Product3', callback_data='product_buying')
product4_in_but = KeyboardButton(text = 'Product4', callback_data='product_buying')

kb.add(button_calculate, button_info, button_sale)
kb_inline.add(inline_button_calc, inline_button_formula)
inline_sale_kb.add(product1_in_but, product2_in_but, product3_in_but, product4_in_but)


class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()


@dp.message_handler(commands=['start'])
async def command_start(message):
    await message.answer('Привет! Я бот помогающий твоему здоровью.', reply_markup=kb)


@dp.message_handler(text='Расчитать')
async def main_menu(message):
    await message.answer('Выберите опцию', reply_markup=kb_inline)

@dp.message_handler(text='Купить')
async def get_buying_list(message):
    for i in range(4):
        with open(f'{i+1}.jpg', 'rb') as img:
            await message.answer_photo(img, f'Название: Product{i + 1} | Описание: описание {i + 1} | Цена: {(i + 1) * 100}')
    await message.answer('Выберите товар для покупки', reply_markup=inline_sale_kb)


@dp.callback_query_handler(text='product_buying')
async def send_confirm_message(call):
    await call.message.answer(text='Вы успешно приобрели продукт!', reply_markup=kb_inline)
    await call.answer()

@dp.callback_query_handler(text='formulas')
async def get_formulas(call):
    await call.message.answer(text='10 x Вес + 6.25 х Рост - 5 х Возраст + 5', reply_markup=kb_inline)
    await call.answer()


@dp.callback_query_handler(text='calories')
async def set_age(call):
    await call.message.answer(text='Введите свой возраст')
    await call.answer()
    await UserState.age.set()


@dp.message_handler(state=UserState.age)
async def set_growth(message, state):
    await state.update_data(age=int(message.text))
    await message.answer('Введите свой рост:', reply_markup=kb)
    await UserState.growth.set()


@dp.message_handler(state=UserState.growth)
async def set_weight(message, state):
    await state.update_data(growth=int(message.text))
    await message.answer('Введите свой вес:', reply_markup=kb)
    await UserState.weight.set()


@dp.message_handler(state=UserState.weight)
async def send_calories(message, state):
    await state.update_data(weight=int(message.text))
    data = await state.get_data()
    norma = 10 * data['weight'] + 6.25 * data['growth'] - 5 * data['age'] + 5
    await message.answer(f'Ваша норма калорий: {norma} кКал', reply_markup=kb)
    await state.finish()


@dp.message_handler()
async def all_messages(message):
    await message.answer('Введите команду /start, чтобы начать общение.')


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
