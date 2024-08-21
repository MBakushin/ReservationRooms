import os
from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils import executor
from datetime import datetime
from sqlalchemy.orm import Session
from . import crud, schemas
from .database import SessionLocal

API_TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

async def start(message: types.Message):
    await message.reply("Welcome! Use /register to register and /book_room to start booking.")

async def register(message: types.Message):
    user = message.from_user
    tg_id = user.id
    nick = user.username

    # Connect to DB
    db = SessionLocal()
    peer = crud.get_peer(db, tg_id)
    if peer:
        await message.reply("You are already registered!")
        return

    # Register new user
    crud.create_peer(db, tg_id, nick)
    await message.reply(f"Registered successfully with nick: {nick}")

async def book_room(message: types.Message):
    db = SessionLocal()
    rooms = crud.get_rooms(db)
    keyboard = [[InlineKeyboardButton(room.name, callback_data=f"select_room:{room.id}")]
                for room in rooms]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await message.reply("Please select a room:", reply_markup=reply_markup)

async def button_callback_handler(query: types.CallbackQuery):
    data = query.data.split(":")
    if data[0] == "select_room":
        room_id = int(data[1])
        db = SessionLocal()
        room = crud.get_room(db, room_id)
        today = datetime.now().date()

        slots = generate_weekly_slots_sync(room_id, today)
        keyboard = generate_weekly_keyboard(slots)
        await query.message.edit_text(f"Selected room: {room.name}. Choose a time slot:", reply_markup=keyboard)

def main():
    dp.register_message_handler(start, commands=["start"])
    dp.register_message_handler(register, commands=["register"])
    dp.register_message_handler(book_room, commands=["book_room"])
    dp.register_callback_query_handler(button_callback_handler)

    executor.start_polling(dp)

if __name__ == '__main__':
    main()
