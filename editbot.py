import asyncio
import logging
from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command
from aiogram.types import Message

# Logging xatolarni terminalda ko'rsatib turadi
logging.basicConfig(level=logging.INFO)

API_TOKEN = "8895452093:AAGNgqeob0ZKz0Yg-8hoduGcLsnOyWNY2pA"

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

user_del_patterns = {}


@dp.message(Command("start"))
async def start_handler(message: Message):
    await message.answer(
        "👋 Salom!\n\n"
        "O'chirmoqchi bo'lgan matningizni quyidagi ko'rinishda yuboring:\n"
        "/del O'chiriladigan matn"
    )


@dp.message(Command("del"))
async def set_delete_pattern(message: Message):
    text = message.text or ""
    pattern = text.replace("/del", "", 1).strip()

    if not pattern:
        await message.answer(
            "⚠️ Iltimos, /del dan keyin o'chiriladigan matnni yozing."
        )
        return

    user_del_patterns[message.from_user.id] = pattern
    await message.answer(
        f"✅ Qabul qilindi!\n\n"
        f"Endi videolardan ushbu matn olib tashlanadi:\n"
        f"👉 <code>{pattern}</code>",
        parse_mode="HTML",
    )


@dp.message(F.video | F.document | F.animation)
async def process_media(message: Message):
    user_id = message.from_user.id
    pattern = user_del_patterns.get(user_id)
    caption = message.caption or ""

    if pattern and pattern in caption:
        new_caption = caption.replace(pattern, "").strip()
    else:
        new_caption = caption

    try:
        if message.video:
            await message.answer_video(
                video=message.video.file_id, caption=new_caption
            )
        elif message.document:
            await message.answer_document(
                document=message.document.file_id, caption=new_caption
            )
        elif message.animation:
            await message.answer_animation(
                animation=message.animation.file_id, caption=new_caption
            )
    except Exception as err:
        await message.answer(f"Xatolik yuz berdi: {err}")


async def main():
    print("Bot muvaffaqiyatli ishga tushdi!")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
