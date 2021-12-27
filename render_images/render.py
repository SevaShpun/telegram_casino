from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
from messages.msg import spin_rules


def main_render(user_id, balance: int, count_refs: int, count_games: int):
    img = Image.open('render_images/assets/img/main.jpg')
    img = img.convert('RGB')
    draw = ImageDraw.Draw(img)
    w_start, w_end = (270, 388)
    font = ImageFont.truetype('render_images/fonts/appetite-italic.ttf', 24)
    list_text = [str(balance) + 'rub', str(count_games), str(count_refs)]
    for pos, i in enumerate(list_text):
        w_text, h_text = draw.textsize(i, font=font)
        draw.text((w_start + ((w_end - w_start) - w_text) / 2, 60 * pos + 115), i, (245, 245, 100), font=font)
    bio = BytesIO()
    bio.name = (str(user_id) + '.jpg')
    img.save(bio)
    bio.seek(0)
    return bio


def payments_render(user_id, cash: int):
    img = Image.open('render_images/assets/img/payments.jpg')
    img = img.convert('RGB')
    draw = ImageDraw.Draw(img)
    w_start, w_end = (317, 442)

    font = ImageFont.truetype('render_images/fonts/appetite-italic.ttf', 24)
    w_text, h_text = draw.textsize(str(cash) + 'rub', font=font)

    draw.text((w_start + ((w_end - w_start) - w_text) / 2, 115), str(cash) + 'rub', (245, 245, 100), font=font)
    bio = BytesIO()
    bio.name = (str(user_id) + '.jpg')
    img.save(bio)
    bio.seek(0)
    return bio


def spin_render(user_id, balance: int, bet: int, result: int, win_number='null', win_money=0):
    img = Image.open('render_images/assets/img/spin.jpg')
    img = img.convert('RGB')
    draw = ImageDraw.Draw(img)
    w_start_balance, w_end_balance = (118, 218)
    w_start_bet, w_end_bet = (345, 445)
    w_start_text, w_end_text = (58, 395)

    font = ImageFont.truetype('render_images/fonts/appetite-italic.ttf', 24)

    w_balance, h_balance = draw.textsize(str(balance), font=font)
    draw.text((w_start_balance + ((w_end_balance - w_start_balance) - w_balance) / 2, 249),
              str(balance), (245, 245, 100), font=font)

    w_bet, h_bet = draw.textsize(str(bet), font=font)
    draw.text((w_start_bet + ((w_end_bet - w_start_bet) - w_bet) / 2, 249),
              str(bet), (245, 245, 100), font=font)

    if result == -1:
        text = 'Ставка не может быть\nбольше баланса'
        for pas, i in enumerate(text.split('\n')):
            w_text, h_text = draw.textsize(i, font=font)
            draw.text((w_start_text + ((w_end_text - w_start_text) - w_text) / 2, 120 + pas * 25),
                      i, (179, 21, 7), font=font)
        bio = BytesIO()
        bio.name = (str(user_id) + '.jpg')
        img.save(bio)
        bio.seek(0)
        return bio

    text_result_list = [('Правила игры:', (31, 31, 29)),
                        ('Вы выиграли!', (9, 138, 4)),
                        ('Вы проиграли!', (179, 21, 7))]
    w_text, h_text = draw.textsize(text_result_list[result][0], font=font)
    draw.text((w_start_text + ((w_end_text - w_start_text) - w_text) / 2, 93),
              text_result_list[result][0], text_result_list[result][1], font=font)

    if not result:
        for pas, i in enumerate(spin_rules.split('\n')):
            w_text, h_text = draw.textsize(i, font=font)
            draw.text((w_start_text + ((w_end_text - w_start_text) - w_text) / 2, 130 + pas * 25),
                      i, (8, 5, 77), font=font)
        bio = BytesIO()
        bio.name = (str(user_id) + '.jpg')
        img.save(bio)
        bio.seek(0)
        return bio

    colors_dict = {'Зеленое': (9, 138, 4), 'Черное': (31, 31, 29), "Красное": (179, 21, 7)}
    w_text, h_text = draw.textsize('Выпало: ' + win_number, font=font)
    draw.text((w_start_text + ((w_end_text - w_start_text) - w_text) / 2, 125),
              'Выпало: ' + win_number, colors_dict.get(win_number.split()[-1], (31, 31, 29)), font=font)

    font_win = ImageFont.truetype('render_images/fonts/appetite-italic.ttf', 40)
    res_win_money = ['+', (23, 115, 2)] if result == 1 else ['-', (179, 21, 7)]
    w_text, h_text = draw.textsize(res_win_money[0] + str(win_money), font=font_win)
    draw.text((w_start_text + ((w_end_text - w_start_text) - w_text) / 2, 160),
              res_win_money[0] + str(win_money), res_win_money[1], font=font_win)

    bio = BytesIO()
    bio.name = (str(user_id) + '.jpg')
    img.save(bio)
    bio.seek(0)
    return bio
