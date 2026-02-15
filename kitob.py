import asyncio
from aiogram import Bot, Dispatcher
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from aiogram.filters import Command
from config import API_TOKEN, CHANNEL_USERNAME, CHANNEL_URL

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

# Inline тугмача: пайванди ба канал
keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Обуна шудан ба канал", url=CHANNEL_URL)],
        [InlineKeyboardButton(text="Санҷиши обуна", callback_data="check_sub")]
    ]
)

@dp.message(Command(commands=["start"]))
async def start(message: Message):
    await message.reply(
        "Барои истифодаи бот, аввал ба канали мо обуна шавед ва тугмаи 'Санҷиши обуна'-ро пахш кунед:",
        reply_markup=keyboard
    )

@dp.callback_query(lambda c: c.data == "check_sub")
async def check_subscription(callback: CallbackQuery):
    user_id = callback.from_user.id
    try:
        member = await bot.get_chat_member(chat_id=CHANNEL_USERNAME, user_id=user_id)
        if member.status != "left":
            await callback.answer(text="✅ Шумо обуна ҳастед!")
            await bot.send_message(user_id, "Ҳозир бот кор мекунад!")
        else:
            await callback.answer(text="❌ Аввал ба канали мо обуна шавед!")
    except Exception:
        await callback.answer(text="Хатогӣ шуд. Ботро админ таъин кунед!")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
