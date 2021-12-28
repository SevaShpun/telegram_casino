from main import bot, dp, anti_flood
from aiogram.types.message import ContentType
from aiogram.types import Message, CallbackQuery, PreCheckoutQuery, InputMedia, InputFile
import payments.keyboard.inline as kb
from payments.tools import send_offer, update_price, price_list
import sqlConnect
from render_images.render import payments_render


@dp.callback_query_handler(lambda x: x.data == 'in')
@dp.throttled(anti_flood, rate=1)
async def back_to_menu(callback_query: CallbackQuery):
    user_id = callback_query.from_user.id
    file = InputMedia(media=InputFile(payments_render(user_id, price_list.get(str(user_id), 100))))
    return await bot.edit_message_media(chat_id=user_id, message_id=callback_query.message.message_id,
                                        media=file,
                                        reply_markup=kb.inline_kb)


@dp.callback_query_handler(lambda x: x.data in ['up_price', 'down_price'])
async def change_price(callback_query: CallbackQuery):
    user_id = callback_query.from_user.id
    update_price(user_id, callback_query.data)
    file = InputMedia(media=InputFile(payments_render(user_id, price_list.get(str(user_id), 100))))
    return await bot.edit_message_media(chat_id=user_id, message_id=callback_query.message.message_id,
                                        media=file,
                                        reply_markup=kb.inline_kb)


@dp.callback_query_handler(lambda x: x.data == 'get_offer')
@dp.throttled(anti_flood, rate=1)
async def get_offer(callback_query: CallbackQuery):
    user_id = callback_query.from_user.id
    return await send_offer(user_id, price_list.get(str(user_id), 100))


@dp.pre_checkout_query_handler(lambda query: True)
async def process_pre_checkout_query(pre_checkout_query: PreCheckoutQuery):
    return await bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)


@dp.message_handler(content_types=ContentType.SUCCESSFUL_PAYMENT)
async def process_successful_payment(message: Message):
    invoice_payload = message.successful_payment.to_python()['invoice_payload']
    sqlConnect.add_dep(message.from_user.id, int(invoice_payload))
    return
