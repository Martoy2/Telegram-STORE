from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove, InlineKeyboardButton, InlineKeyboardMarkup
import config as cfg

#admin kb

b_history = KeyboardButton("История покупок")
b_stat = KeyboardButton("Статистика")
b_zakaz = KeyboardButton("Заказы к выполнению")
b_rassl = KeyboardButton("Рассылка")
b_back = KeyboardButton("Назад")

kb_admin = ReplyKeyboardMarkup(resize_keyboard=True)
kb_admin.add(b_history, b_stat).add(b_zakaz, b_rassl).add(b_back)

#default kb

def create_main_kb(check):
    b1= KeyboardButton("🎮Магазин")
    b2= KeyboardButton("🌟Поддержка")
    b3= KeyboardButton("🌈Профиль")
    data = KeyboardButton("Данные✉")
    otizv_2 = KeyboardButton("Отзывы✨")
    kb_m = ReplyKeyboardMarkup(resize_keyboard=True)
    if check == True:
        kb_m.add(b1).add(b2, b3).add(data, otizv_2)
    else:
        kb_m.add(b1).add(b2, b3).add(otizv_2)
    return kb_m

#проверка платежа

def create_pay_kb(url):
    b1 = InlineKeyboardButton("Оплатить", url=url)
    b2 = InlineKeyboardButton("Проверить", callback_data="check")
    b3 = InlineKeyboardButton("Отменить", callback_data="reject")

    kb_check_pay = InlineKeyboardMarkup(resize_keyboard=True)

    kb_check_pay.add(b1, b2).add(b3)
    return kb_check_pay

#shop
def create_main_inline_kb():
    discord = InlineKeyboardButton('Discord Nitro', callback_data='discord')
    steam = InlineKeyboardButton('Steam Gift Code (Turkey)', callback_data='steam')
    play_market = InlineKeyboardButton('PlayMarket Gift Code (Turkey)', callback_data='gplay')
    xbox = InlineKeyboardButton('Xbox + Forza', callback_data='xbox')
    rg_steam = InlineKeyboardButton(f'Смена региона Steam (Турция) - {cfg.get_price()["steam_rg"]} руб.', callback_data='steam-rg')

    inline_kb_shop = InlineKeyboardMarkup()

    inline_kb_shop.add(discord, steam).add(play_market, xbox).add(rg_steam)

    return inline_kb_shop

#ds_shop
def create_kb():
    #ds_shop
    basic_moth = InlineKeyboardButton(f'Basic (1 Месяц) - {cfg.get_price()["basic_moth"]} руб.', callback_data='discord-basic-moth')
    basic_year = InlineKeyboardButton(f'Basic (1 Год) - {cfg.get_price()["basic_year"]} руб.', callback_data='discord-basic-year')
    full_moth = InlineKeyboardButton(f'Full (1 Месяц) - {cfg.get_price()["full_moth"]} руб.', callback_data='discord-full-moth')
    full_year = InlineKeyboardButton(f'Full (1 Год) - {cfg.get_price()["full_year"]} руб.', callback_data='discord-full-year')
    back = InlineKeyboardButton('Назад', callback_data='back')

    inline_kb_ds_shop = InlineKeyboardMarkup()

    inline_kb_ds_shop.add(basic_moth, basic_year).add(full_moth, full_year).add(back)


    #steam
    steam_20 = InlineKeyboardButton(f'20 TL - {cfg.get_price()["steam_20"]} руб.', callback_data='steam-wallet-20')
    steam_50 = InlineKeyboardButton(f'50 TL - {cfg.get_price()["steam_50"]} руб.', callback_data='steam-wallet-50')
    steam_100 = InlineKeyboardButton(f'100 TL - {cfg.get_price()["steam_100"]} руб.', callback_data='steam-wallet-100')
    steam_200 = InlineKeyboardButton(f'200 TL - {cfg.get_price()["steam_200"]} руб.', callback_data='steam-wallet-200')
    back = InlineKeyboardButton('Назад', callback_data='back')

    inline_kb_steam_shop = InlineKeyboardMarkup()

    inline_kb_steam_shop.add(steam_20, steam_50).add(steam_100, steam_200).add(back)

    #gplay
    gplay_25 = InlineKeyboardButton(f'25 TL - {cfg.get_price()["gplay_25"]} руб.', callback_data='google-play-25')
    gplay_50 = InlineKeyboardButton(f'50 TL - {cfg.get_price()["gplay_50"]} руб.', callback_data='google-play-50')
    gplay_100 = InlineKeyboardButton(f'100 TL - {cfg.get_price()["gplay_100"]} руб.', callback_data='google-play-100')
    gplay_250 = InlineKeyboardButton(f'250 TL - {cfg.get_price()["gplay_250"]} руб.', callback_data='google-play-250')
    gplay_500 = InlineKeyboardButton(f'500 TL - {cfg.get_price()["gplay_500"]} руб.', callback_data='google-play-500')
    gplay_1000 = InlineKeyboardButton(f'1000 TL - {cfg.get_price()["gplay_1000"]} руб.', callback_data='google-play-1000')
    back = InlineKeyboardButton('Назад', callback_data='back')

    inline_kb_gplay_shop = InlineKeyboardMarkup()

    inline_kb_gplay_shop.add(gplay_25, gplay_50).add(gplay_100, gplay_250).add(gplay_500, gplay_1000).add(back)

    #subscribe
    xbox_lifetime = InlineKeyboardButton(f'Навсегда - {cfg.get_price()["xbox_lifetime"]} руб.', callback_data='xbox-lifetime')

    inline_kb_xbox_shop = InlineKeyboardMarkup()

    inline_kb_xbox_shop.add(xbox_lifetime).add(back)




    d=dict()
    d['inline_kb_ds_shop'] = inline_kb_ds_shop
    d['inline_kb_steam_shop'] = inline_kb_steam_shop
    d['inline_kb_gplay_shop'] = inline_kb_gplay_shop
    d["inline_kb_xbox_shop"] = inline_kb_xbox_shop
    return d

#profile
history_kb = InlineKeyboardButton('Мои покупки', callback_data='history')

inline_kb_history = InlineKeyboardMarkup()

inline_kb_history.add(history_kb)

#кб для выполнения заказа
back = KeyboardButton("Закончить выполнение!")
send_chat = KeyboardButton("Отправить кнопку 'Начать общение'")
pause = KeyboardButton("Поставить заказ на паузу")

kb_vpl = ReplyKeyboardMarkup(resize_keyboard=True)
kb_vpl.add(back, pause).add(send_chat)

#начать общение
start_kb = InlineKeyboardButton('Начать общение', callback_data='start_msg')

kb_start_msg = InlineKeyboardMarkup(resize_keyboard=True)
kb_start_msg.add(start_kb)

#отзывы кб

otizv_kb = InlineKeyboardButton("Оставить отзыв", callback_data='otziv')

kb_otziv = InlineKeyboardMarkup(resize_keyboard=True)
kb_otziv.add(otizv_kb, back)