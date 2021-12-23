from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


inline_menu_kb = InlineKeyboardMarkup()

inline_menu_btn_slot = InlineKeyboardButton('Играть в слоты (В разработке)', callback_data='slot')
inline_menu_btn_spin = InlineKeyboardButton('Играть в рулетку (Beta)', callback_data='spin')
inline_menu_btn_invite = InlineKeyboardButton('Приглосить друга', callback_data='invite')
inline_menu_btn_out = InlineKeyboardButton('Вывести средства', callback_data='out')

for i in [inline_menu_btn_slot, inline_menu_btn_spin, inline_menu_btn_invite, inline_menu_btn_out]:
    inline_menu_kb.add(i)


inline_spin_kb = InlineKeyboardMarkup()

inline_spin_up_bet = InlineKeyboardButton('Увеличить ставку >', callback_data='spin_up_bet')
inline_spin_down_bet = InlineKeyboardButton('< Уменьшить ставку', callback_data='spin_down_bet')

inline_spin_start_red = InlineKeyboardButton('Red', callback_data='spin_red')
inline_spin_start_zero = InlineKeyboardButton('Zero', callback_data='spin_green')
inline_spin_start_black = InlineKeyboardButton('Black', callback_data='spin_black')

inline_spin_kb.add(*[inline_spin_down_bet, inline_spin_up_bet])
inline_spin_kb.add(*[inline_spin_start_red, inline_spin_start_zero, inline_spin_start_black])

inline_spin_menu = InlineKeyboardButton('Вернуться в меню', callback_data='back_to_menu')
inline_spin_kb.add(inline_spin_menu)

