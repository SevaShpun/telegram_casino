from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


inline_menu_kb = InlineKeyboardMarkup()
inline_menu_btn_slot = InlineKeyboardButton('Играть в слоты', callback_data='slot')
inline_menu_btn_spin = InlineKeyboardButton('Играть в рулетку', callback_data='spin')
inline_menu_btn_invite = InlineKeyboardButton('Приглосить друга', callback_data='invite')
inline_menu_btn_out = InlineKeyboardButton('Вывести средства', callback_data='out')

for i in [inline_menu_btn_slot, inline_menu_btn_spin, inline_menu_btn_invite, inline_menu_btn_out]:
    inline_menu_kb.add(i)

