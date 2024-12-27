import logging
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils import executor
from dotenv import load_dotenv
import os

load_dotenv()  # .env faylini yuklash
API_TOKEN = os.getenv('API_TOKEN')
bot = Bot(token=API_TOKEN, parse_mode='HTML')
dp = Dispatcher(bot)

@dp.message_handler(commands='start')
async def start_handler(message: types.Message):
    await message.answer("<b>Tabriklayman🥳🥳\nKasal sochlarni davolash uchun oxirgi qadamga yetib keldingiz…</b>")
    await message.answer("<b>Ismingizni kiriting:</b>")

@dp.message_handler(lambda message: message.text and not message.contact)
async def process_name(message: types.Message):
    user_name = message.text

    with open("user_data.txt", "a") as file:
        file.write(f"Name: {user_name}\n")

    phone_button = ReplyKeyboardMarkup(resize_keyboard=True).add(
        KeyboardButton("Telefon raqamni yuborish", request_contact=True)
    )
    await message.answer("<b>Telefon raqamingizni kiriting:</b>", reply_markup=phone_button)


@dp.message_handler(content_types=types.ContentType.CONTACT)
async def process_phone(message: types.Message):
    phone_number = message.contact.phone_number

    with open("user_data.txt", "a") as file:
        file.write(f"Phone: {phone_number}\n")

    remove_keyboard = ReplyKeyboardRemove()
    await message.answer("Raqamingiz qabul qilindi. Rahmat!", reply_markup=remove_keyboard)

    video_path = "vd1.MP4"
    video_caption = "Assalomu alaykum! 👋\n\nSizga va’da qilingan <b>“Kasal sochlarni davolash”</b> mavzusidagi darsga xush kelibsiz!\n\n⏳Davomiyligi: 17minut"
    youtube_button = InlineKeyboardMarkup().add(
        InlineKeyboardButton("Videoni ko'rish", url="https://youtu.be/ikdD3obszyE")
    )

    if os.path.exists(video_path):
        try:
            with open(video_path, "rb") as video:
                await bot.send_video(
                    chat_id=message.chat.id,
                    video=video,
                    caption=video_caption,
                    reply_markup=youtube_button
                )
        except Exception as e:
            await message.answer(f"Videoni yuborishda xatolik yuz berdi: {e}")
    else:
        await message.answer("Fayl topilmadi. Iltimos, administrator bilan bog'laning.")


logging.basicConfig(level=logging.INFO)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
