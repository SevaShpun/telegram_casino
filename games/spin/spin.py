from config import spin_config
import random

user_bet = {}


def update_bet(user_id, change):
    if change == 'spin_up_bet':
        if str(user_id) in user_bet:
            if user_bet[str(user_id)] != spin_config[-1]:
                user_bet[str(user_id)] = spin_config[spin_config.index(user_bet[str(user_id)]) + 1]
            else:
                user_bet[str(user_id)] = spin_config[0]
        else:
            user_bet[str(user_id)] = spin_config[1]
    if change == 'spin_down_bet':
        if str(user_id) in user_bet:
            if user_bet[str(user_id)] != spin_config[0]:
                user_bet[str(user_id)] = spin_config[spin_config.index(user_bet[str(user_id)]) - 1]
            else:
                user_bet[str(user_id)] = spin_config[-1]
        else:
            user_bet[str(user_id)] = spin_config[-1]
    return True


def start_game(user_id, color):
    bet = user_bet.get(str(user_id), spin_config[0])
    colors_list = ['Зеленое', 'Черное', "Красное"]
    win_numb = random.randint(0, 14)

    if color == 'spin_green' and win_numb == 0:
        return [True, bet*14 - bet, str(win_numb) + ' ' + colors_list[0]]

    if color == 'spin_red' and 0 < win_numb < 8:
        return [True, bet, str(win_numb) + ' ' + colors_list[2]]

    if color == 'spin_black' and win_numb > 7:
        return [True, bet, str(win_numb) + ' ' + colors_list[1]]

    win_color = 0
    if 0 < win_numb < 8:
        win_color = 2
    if win_numb > 7:
        win_color = 1
    return [False, bet, str(win_numb) + ' ' + colors_list[win_color]]


