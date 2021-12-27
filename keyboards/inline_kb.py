from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


inline_menu_kb = InlineKeyboardMarkup()

inline_menu_btn_spin = InlineKeyboardButton('Играть в рулетку (Beta)', callback_data='spin')
inline_menu_btn_invite = InlineKeyboardButton('Пригласить друга', callback_data='invite')
inline_menu_btn_out = InlineKeyboardButton('Вывести средства', callback_data='out')
inline_menu_btn_in = InlineKeyboardButton('Пополнить баланс', callback_data='in')

inline_menu_kb.add(inline_menu_btn_spin)
inline_menu_kb.add(inline_menu_btn_out, inline_menu_btn_invite)
inline_menu_kb.add(inline_menu_btn_in)


inline_spin_kb = InlineKeyboardMarkup()

inline_spin_up_10 = InlineKeyboardButton('+10', callback_data='up_10')
inline_spin_up_100 = InlineKeyboardButton('+100', callback_data='up_100')
inline_spin_up_1000 = InlineKeyboardButton('+1000', callback_data='up_1000')

inline_spin_down_10 = InlineKeyboardButton('-10', callback_data='down_10')
inline_spin_down_100 = InlineKeyboardButton('-100', callback_data='down_100')
inline_spin_down_1000 = InlineKeyboardButton('-1000', callback_data='down_1000')

inline_spin_start_red = InlineKeyboardButton('Red', callback_data='spin_red')
inline_spin_start_zero = InlineKeyboardButton('Zero', callback_data='spin_green')
inline_spin_start_black = InlineKeyboardButton('Black', callback_data='spin_black')

inline_spin_max = InlineKeyboardButton('Max ставка', callback_data='max_bet')
inline_spin_min = InlineKeyboardButton('Min ставка', callback_data='min_bet')

inline_spin_kb.add(*[inline_spin_start_red, inline_spin_start_zero, inline_spin_start_black])
inline_spin_kb.add(*[inline_spin_max, inline_spin_min])
inline_spin_kb.add(*[inline_spin_up_10, inline_spin_up_100, inline_spin_up_1000])
inline_spin_kb.add(*[inline_spin_down_1000, inline_spin_down_100, inline_spin_down_10])

inline_spin_menu = InlineKeyboardButton('Вернуться в меню', callback_data='back_to_menu')
inline_spin_kb.add(inline_spin_menu)
