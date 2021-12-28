from main import bot, dp, anti_flood
from aiogram.types import Message, CallbackQuery, InputMedia, InputFile
from config import ADMIN_ID
import sqlConnect
import messages.msg as msg
import keyboards.inline_kb as kb_il
from render_images.render import main_render


message_status = {}


async def sand_to_admin(dp):
    await bot.send_message(chat_id=ADMIN_ID, text=f"bot_started")


async def get_menu_back(user_id):
    user = sqlConnect.get_user_info(user_id)
    return await bot.send_photo(user_id, photo=main_render(user_id, *user), reply_markup=kb_il.inline_menu_kb)


async def get_menu_btn(user_id, message_id):
    user = sqlConnect.get_user_info(user_id)
    file = InputMedia(media=InputFile(main_render(user_id, *user)))
    return await bot.edit_message_media(chat_id=user_id, message_id=message_id,
                                        media=file, reply_markup=kb_il.inline_menu_kb)


@dp.message_handler(commands=['start'])
@dp.throttled(anti_flood, rate=3)
async def start_message(message: Message):
    if sqlConnect.exist_user(int(message.from_user.id)):
        await bot.send_message(message.from_user.id, msg.exist_user_start)
        return await get_menu_back(message.from_user.id)

    ref = message.text.split()[1] if len(message.text.split()) > 1 else 0

    if str(ref).isdigit() and ref != 0:
        if sqlConnect.exist_user(int(ref)):
            sqlConnect.add_new_user(int(message.from_user.id), int(ref), balance=500)
            sqlConnect.update_balance(int(ref), 100)
            await bot.send_message(message.from_user.id, text=msg.new_user_on_ref)
            return await get_menu_back(message.from_user.id)

    sqlConnect.add_new_user(int(message.from_user.id), 0, balance=250)

    await bot.send_message(message.from_user.id, text=msg.new_user_no_ref)
    return await get_menu_back(message.from_user.id)


@dp.message_handler(commands=['menu'])
@dp.throttled(anti_flood, rate=3)
async def get_menu(message: Message):
    user_id = message.from_user.id
    return await get_menu_back(user_id)


# ________________________________________ КНОПКИ ____________________________________________________________


@dp.callback_query_handler(lambda x: x.data == 'invite')
@dp.throttled(anti_flood, rate=1)
async def invite_friend_btn(callback_query: CallbackQuery):
    user_id = callback_query.from_user.id
    return await bot.send_message(user_id, text=msg.ref_text + str(user_id))


@dp.callback_query_handler(lambda x: x.data == 'out')
@dp.throttled(anti_flood, rate=1)
async def out_cash_btn(callback_query: CallbackQuery):
    user_id = callback_query.from_user.id
    return await bot.send_message(user_id, text=msg.out_text)


@dp.callback_query_handler(lambda x: x.data == 'back_to_menu')
@dp.throttled(anti_flood, rate=1)
async def back_to_menu(callback_query: CallbackQuery):
    user_id = callback_query.from_user.id
    return await get_menu_btn(user_id, callback_query.message.message_id)


# ________________________________________ END _______________________________________________________________


@dp.message_handler(content_types=['text'])
@dp.throttled(anti_flood, rate=1)
async def echo(message: Message):
    await bot.send_message(message.from_user.id, text=message.text)
