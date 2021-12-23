from main import bot, dp, anti_flood
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from config import ADMIN_ID
import sqlConnect
import messages.msg as msg
import keyboards.inline_kb as kb_il

message_status = {}


async def sand_to_admin(dp):
    await bot.send_message(chat_id=ADMIN_ID, text=f"bot_started")


@dp.message_handler(commands=['start'])
@dp.throttled(anti_flood, rate=3)
async def start_message(message: Message):
    if sqlConnect.exist_user(int(message.from_user.id)):
        return await bot.send_message(message.from_user.id, msg.exist_user_start)
    ref = message.text.split()[1] if len(message.text.split()) > 1 else 0
    if str(ref).isdigit() and ref != 0:
        if sqlConnect.exist_user(int(ref)):
            sqlConnect.add_new_user(int(message.from_user.id), int(ref), balance=500)
            sqlConnect.update_balance(int(ref), 100)
            return await bot.send_message(message.from_user.id, text=msg.new_user_on_ref)
    sqlConnect.add_new_user(int(message.from_user.id), 0, balance=250)
    return await bot.send_message(message.from_user.id, text=msg.new_user_no_ref)


@dp.message_handler(commands=['refka'])
@dp.throttled(anti_flood, rate=3)
async def get_ref(message: Message):
    return await bot.send_message(message.from_user.id, text=msg.ref_text + str(message.from_user.id))


@dp.message_handler(commands=['menu'])
@dp.throttled(anti_flood, rate=3)
async def get_menu(message: Message):
    user = sqlConnect.get_user_info(message.from_user.id)
    return await bot.send_message(message.from_user.id, text=msg.menu.format(*user), reply_markup=kb_il.inline_menu_kb)


# ________________________________________ КНОПКИ ____________________________________________________________


@dp.callback_query_handler(lambda x: x.data == 'invite')
@dp.throttled(anti_flood, rate=3)
async def invite_friend_btn(callback_query: CallbackQuery):
    user_id = callback_query.from_user.id
    return await bot.send_message(user_id, text=msg.ref_text + str(user_id))


@dp.callback_query_handler(lambda x: x.data == 'out')
@dp.throttled(anti_flood, rate=3)
async def out_cash_btn(callback_query: CallbackQuery):
    user_id = callback_query.from_user.id
    await bot.message
    return await bot.send_message(user_id, text=msg.out_text)

# ________________________________________ END _______________________________________________________________


@dp.message_handler(content_types=['text'])
@dp.throttled(anti_flood, rate=1)
async def echo(message: Message):
    await bot.send_message(message.from_user.id, text=message.text)
