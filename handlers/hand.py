
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, Message

from data.loops import Loop
from data.parser import parsing
from loader import dp, bot


@dp.callback_query_handler(text_startswith="", state="*")
async def gg(call: CallbackQuery, state: FSMContext):
    pass


@dp.message_handler(state='')
async def gg(message: Message, state: FSMContext):
    pass


@dp.message_handler(text="gg")
async def gg(message: Message, state: FSMContext):
    await message.answer("gg")
    await parsing()

@dp.callback_query_handler(text_startswith="", state="")
async def gg(call: CallbackQuery, state: FSMContext):
    pass


@dp.message_handler(text="start")
async def gg(message: Message, state: FSMContext):
    user = message.from_user
    loop = Loop.get_loop(user.id)

    if loop.is_running:
        return await message.answer('Loop is already running')

    await loop.start()
    await message.answer('Started!')


@dp.message_handler(text="stop")
async def gg(message: Message, state: FSMContext):
    user = message.from_user
    loop = Loop.get_loop(user.id)
    await message.answer('Stopping...')
    await loop.stop()
    await bot.send_message(user.id, 'Loop successfully stopped.')
