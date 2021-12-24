from main import bot, dp, anti_flood
from aiogram.types import Message, CallbackQuery
import sqlConnect
import messages.msg as msg
import keyboards.inline_kb as kb_il
import games.spin.spin as spin
from asyncio import sleep


bet_status = {}


@dp.callback_query_handler(lambda x: x.data == 'spin')
@dp.throttled(anti_flood, rate=1)
async def spin_btn(callback_query: CallbackQuery):
    user_id = callback_query.from_user.id
    await bot.delete_message(user_id, message_id=callback_query.message.message_id)
    spin_text = msg.spin_game_main.format(spin.user_bet.get(str(user_id), 10), sqlConnect.get_user_balance(user_id))
    return await bot.send_message(user_id, text=spin_text, reply_markup=kb_il.inline_spin_kb)


@dp.callback_query_handler(lambda x: x.data == 'spin_up_bet' or x.data == 'spin_down_bet')
async def update_bet_spin_btn(callback_query: CallbackQuery):
    user_id = callback_query.from_user.id
    spin.update_bet(user_id, callback_query.data)
    callback_text = callback_query.message.text
    str_message = callback_text[:-1 * sum([len(j) for j in callback_text.split()[-4:]]) - 3]

    spin_text = str_message + msg.spin_game_update_bet.format(spin.user_bet.get(str(user_id), 10), callback_text.split()[-1][:-2])

    return await bot.edit_message_text(chat_id=user_id, message_id=callback_query.message.message_id,
                                       text=spin_text, reply_markup=kb_il.inline_spin_kb)


@dp.callback_query_handler(lambda x: x.data in ['spin_red', 'spin_green', 'spin_black'])
@dp.throttled(anti_flood, rate=1)
async def start_(callback_query: CallbackQuery):
    user_id = callback_query.from_user.id
    if bet_status.get(str(user_id), False):
        return
    balance = sqlConnect.get_user_balance(user_id)

    if balance < spin.user_bet.get(str(user_id), 10):
        msg_not_balance = msg.spin_game_not_balance.format(spin.user_bet.get(str(user_id), 10), balance)
        try:
            return await bot.edit_message_text(chat_id=user_id, message_id=callback_query.message.message_id,
                                               text=msg_not_balance, reply_markup=kb_il.inline_spin_kb)
        except Exception as ex:
            print(ex)
            return

    result_game = spin.start_game(user_id, callback_query.data)
    message = msg.spin_game_win if result_game[0] else msg.spin_game_lose

    sqlConnect.update_balance(user_id, result_game[1] if result_game[0] else -1 * result_game[1])
    sqlConnect.update_count_game(user_id)

    balance += result_game[1] if result_game[0] else -1 * result_game[1]

    message = message.format(result_game[-1], result_game[1] * 2 if result_game[0] else result_game[1],
                             spin.user_bet.get(str(user_id), 10), balance)
    with open(f"./games/spin/assets/gif/{result_game[-1].split()[0]}.gif", 'rb') as gif:
        anim_id = await bot.send_animation(chat_id=user_id, animation=gif)
    bet_status[str(user_id)] = True
    await sleep(7)
    bet_status[str(user_id)] = False
    await bot.delete_message(chat_id=user_id, message_id=anim_id.message_id)

    return await bot.edit_message_text(chat_id=user_id, message_id=callback_query.message.message_id,
                                       text=message, reply_markup=kb_il.inline_spin_kb)
