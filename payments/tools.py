from main import bot
from aiogram import types
from config import payments_token, payments_config

price_list = {}


async def send_offer(user_id, price: int):
    await bot.send_invoice(user_id,
                           title='{} рублей'.format(price),
                           description='Пополнение баланса на {} рублей'.format(price),
                           provider_token=payments_token,
                           currency='RUB',
                           is_flexible=False,  # True если конечная цена зависит от способа доставки
                           prices=[types.LabeledPrice(label='{} рублей'.format(price), amount=price * 100)],
                           start_parameter='time-machine-example',
                           payload=price
                           )


def update_price(user_id, change):
    if change == 'up_price':
        if str(user_id) in price_list:
            if price_list[str(user_id)] != payments_config[-1]:
                price_list[str(user_id)] = payments_config[payments_config.index(price_list[str(user_id)]) + 1]
            else:
                price_list[str(user_id)] = payments_config[0]
        else:
            price_list[str(user_id)] = payments_config[1]
    if change == 'down_price':
        if str(user_id) in price_list:
            if price_list[str(user_id)] != payments_config[0]:
                price_list[str(user_id)] = payments_config[payments_config.index(price_list[str(user_id)]) - 1]
            else:
                price_list[str(user_id)] = payments_config[-1]
        else:
            price_list[str(user_id)] = payments_config[-1]
    return True
