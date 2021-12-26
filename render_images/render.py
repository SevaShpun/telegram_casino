from PIL import Image, ImageDraw, ImageFont
from io import BytesIO


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
    img = Image.open('./render_images/assets/img/payments.jpg')
    img = img.convert('RGB')
    draw = ImageDraw.Draw(img)
    w_start, w_end = (317, 442)

    font = ImageFont.truetype('./render_images/fonts/appetite-italic.ttf', 24)
    w_text, h_text = draw.textsize(str(cash) + 'rub', font=font)

    draw.text((w_start + ((w_end - w_start) - w_text) / 2, 115), str(cash) + 'rub', (245, 245, 100), font=font)
    bio = BytesIO()
    bio.name = (str(user_id) + '.jpg')
    img.save(bio)
    bio.seek(0)
    return bio
