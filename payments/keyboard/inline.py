from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

inline_kb = InlineKeyboardMarkup()

down = InlineKeyboardButton('< Уменьшить сумму', callback_data="down_price")
up = InlineKeyboardButton('Увеличить сумму >', callback_data="up_price")

get_offer = InlineKeyboardButton('Пополнить', callback_data="get_offer")

inline_spin_menu = InlineKeyboardButton('Вернуться в меню', callback_data='back_to_menu')

inline_kb.add(down, up)
inline_kb.add(get_offer)
inline_kb.add(inline_spin_menu)
