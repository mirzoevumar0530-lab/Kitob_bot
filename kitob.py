import asyncio
from aiogram import Bot, Dispatcher
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from aiogram.filters import Command
from aiogram.exceptions import TelegramBadRequest
from config import API_TOKEN, CHANNEL_USERNAME, CHANNEL_URL

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

# Inline клавиатура барои санҷиши обуна
subscription_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="Обуна шудан ба канал", url=CHANNEL_URL
            )
        ],
        [
            InlineKeyboardButton(
                text="Санҷиши обуна", callback_data="check_sub"
            )
        ]
    ]
)

# URL-и канали спонсор мустақиман дар код
SPONSOR_CHANNEL_URL = "@sponkitob"  # username бо @ ё public channel

# Функсия барои санҷиши URL / username-и канал
async def is_valid_channel(url_or_username):
    try:
        await bot.get_chat(url_or_username)
        return True
    except TelegramBadRequest:
        return False

# /start
@dp.message(Command(commands=["start"]))
async def start(message: Message):
    await message.reply(
        "Барои истифодаи бот, аввал ба канали мо обуна шавед ва тугмаи 'Санҷиши обуна'-ро пахш кунед:",
        reply_markup=subscription_keyboard
    )

# Callback барои санҷиши обуна ва спонсор
@dp.callback_query(lambda c: c.data == "check_sub")
async def check_subscription(callback: CallbackQuery):
    user_id = callback.from_user.id
    try:
        # Санҷиши обуна бо username
        member = await bot.get_chat_member(chat_id=CHANNEL_USERNAME, user_id=user_id)
        if member.status != "left":
            # Санҷиши канали спонсор
            if await is_valid_channel(SPONSOR_CHANNEL_URL):
                sponsor_keyboard = InlineKeyboardMarkup(
                    inline_keyboard=[
                        [InlineKeyboardButton(text="💖 Спонсор шудан", url=f"https://t.me/{SPONSOR_CHANNEL_URL[1:]}")]
                    ]
                )
                await callback.message.edit_text(
                    "✅ Шумо обуна ҳастед!\n\nАкнун шумо метавонед спонсор шавед:",
                    reply_markup=sponsor_keyboard
                )
            else:
                await callback.answer(
                    text="❌ Линк ё аккаунт спонсор нодуруст аст!",
                    show_alert=True
                )
        else:
            await callback.answer(
                text="❌ Аввал ба канали мо обуна шавед!",
                show_alert=True
            )
    except Exception:
        await callback.answer(
            text="Хатогӣ шуд. Ботро админ таъин кунед!",
            show_alert=True
        )

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
