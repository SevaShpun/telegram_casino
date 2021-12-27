from main import bot, dp, anti_flood
from aiogram.types import Message, CallbackQuery, InputMedia, InputFile
import sqlConnect
import keyboards.inline_kb as kb_il
import games.spin.spin as spin
from asyncio import sleep
from render_images.render import spin_render


bet_status = {}


@dp.callback_query_handler(lambda x: x.data == 'spin')
@dp.throttled(anti_flood, rate=1)
async def spin_btn(callback_query: CallbackQuery):
    user_id = callback_query.from_user.id
    await bot.delete_message(user_id, message_id=callback_query.message.message_id)
    img = spin_render(user_id, sqlConnect.get_user_balance(user_id), spin.user_bet.get(str(user_id), 10), 0)
    return await bot.send_photo(user_id, photo=img, reply_markup=kb_il.inline_spin_kb)


@dp.callback_query_handler(lambda x: x.data in ['spin_up_bet', 'spin_down_bet'])
async def update_bet_spin_btn(callback_query: CallbackQuery):
    user_id = callback_query.from_user.id
    spin.update_bet(user_id, callback_query.data)

    img = spin_render(user_id, sqlConnect.get_user_balance(user_id), spin.user_bet.get(str(user_id), 10), 0)
    file = InputMedia(media=InputFile(img))

    return await bot.edit_message_media(chat_id=user_id, message_id=callback_query.message.message_id,
                                        media=file, reply_markup=kb_il.inline_spin_kb)


@dp.callback_query_handler(lambda x: x.data in ['spin_red', 'spin_green', 'spin_black'])
@dp.throttled(anti_flood, rate=1)
async def start_(callback_query: CallbackQuery):
    user_id = callback_query.from_user.id

    if bet_status.get(str(user_id), False):
        return

    balance = sqlConnect.get_user_balance(user_id)
    user_bet = spin.user_bet.get(str(user_id), 10)

    if balance < user_bet:
        img = spin_render(user_id, sqlConnect.get_user_balance(user_id), spin.user_bet.get(str(user_id), 10), -1)
        file = InputMedia(media=InputFile(img))
        return await bot.edit_message_media(chat_id=user_id, message_id=callback_query.message.message_id,
                                            media=file, reply_markup=kb_il.inline_spin_kb)

    result_game = spin.start_game(user_id, callback_query.data)

    sqlConnect.update_balance(user_id, result_game[1] if result_game[0] else -1 * result_game[1])
    sqlConnect.update_count_game(user_id)

    balance += result_game[1] if result_game[0] else -1 * result_game[1]
    result_msg = result_game[1] * 2 if result_game[0] else result_game[1]

    if result_game[-1].split()[0] == '0':
        result_msg = result_game[1] + user_bet

    with open(f"./games/spin/assets/video/{result_game[-1].split()[0]}.mp4", 'rb') as gif:
        try:
            anim_id = await bot.send_video(chat_id=user_id, video=gif)
            bet_status[str(user_id)] = True
            await sleep(7.5)
            bet_status[str(user_id)] = False
            await bot.delete_message(chat_id=user_id, message_id=anim_id.message_id)
        except Exception as ex:
            print(ex)

    is_win = 1 if result_game[0] else 2

    img = spin_render(user_id, balance, spin.user_bet.get(str(user_id), 10), is_win, result_game[-1], result_msg)
    file = InputMedia(media=InputFile(img))

    return await bot.edit_message_media(chat_id=user_id, message_id=callback_query.message.message_id,
                                        media=file, reply_markup=kb_il.inline_spin_kb)
