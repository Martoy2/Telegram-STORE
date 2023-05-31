from aiogram import *
import config as cfg
from keyboards.kb import *
import parse
import sqlite3
from db import BotDB
import random
import logging
from pyqiwip2p import QiwiP2P
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State

QIWI_PRIV_KEY=cfg.QIWI

let="AaBbCcDdEeFfGg"

p2p = QiwiP2P(auth_key=QIWI_PRIV_KEY)

TOKEN_API = cfg.TOKEN

logging.basicConfig(level=logging.ERROR, filename="py_log.log",filemode="w")

storage = MemoryStorage()
bot = Bot(TOKEN_API)
dp = Dispatcher(bot, storage=storage)

class BotStatesGroup(StatesGroup):
    waiting_ad_vpl = State()
    statr_vpl = State()
    start_user_vpl = State()
    otziv = State()
    rassl = State()

BotDB=BotDB('bd.db')

cfg.managers = cfg.managers + ", " + cfg.admins

def check_reg(id):
    if not BotDB.user_exists(id):
        return False
    else:
        return True

def create_pay(id, amount, callback):
    comment = str(id) + "_" + str(amount) + "_" + callback + "_" + str(random.randint(10000, 99999))
    bill_id=str(random.randint(10000, 99999)) + comment + "_" + str(random.randint(10000, 99999))
    bill = p2p.bill(bill_id=bill_id, amount = amount, lifetime=15, comment=comment)
    url = p2p.check(bill_id).pay_url
    BotDB.SavePay(id, bill_id, comment)
    return url

@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    if not BotDB.user_exists(message.from_user.id):
        BotDB.newUser(message.from_user.id)
        for i in (cfg.managers).split(", "):
            await bot.send_message(chat_id=i, text=f"Зарегестрирован новый пользователь! {message.from_user.id}[ник: {message.from_user.username}]")
        #await bot.send_message(chat_id=[i for i in (cfg.managers).split(", ")], text=f"Зарегестрирован новый пользователь! {message.from_user.id}[ник: {message.from_user.username}]")
    await message.reply("Привет! Это Quade Shop. \nВыбери из предложенных вариантов:", reply_markup=create_main_kb(BotDB.check_subscribe(message.from_user.id)))

@dp.message_handler(commands=['admin'])
async def admin(message: types.message):
    if str(message.from_user.id) in cfg.managers.split(", "):
        await bot.send_message(message.chat.id, '☎Admin Панель', reply_markup=kb_admin)
    else:
        await bot.send_message(message.chat.id, 'У вас нет доступа.')

@dp.message_handler(text="🎮Магазин")
async def shop(message: types.Message):
    id = message.from_user.id
    if check_reg(id) == True:
        await message.reply(f"Выберите категорию: ", reply_markup=create_main_inline_kb())
    else:
        await message.reply(f"Вам нужно зарегестрироваться, для этого пропишите /start")

@dp.message_handler(text="Отзывы✨")
async def shop(message: types.Message):
    id = message.from_user.id
    if check_reg(id) == True:
        await message.reply(f"Отзывы @quade_shop_reviews")
    else:
        await message.reply(f"Вам нужно зарегестрироваться, для этого пропишите /start")


@dp.callback_query_handler()
async def shop_kb(callback: types.CallbackQuery, state=FSMContext):
    if check_reg(callback.from_user.id) == True:
        if callback.data == 'discord':
            await callback.answer(text='Discord Nitro')
            await bot.edit_message_text(chat_id=callback.message.chat.id, message_id=callback.message.message_id, text='Выберите тип подписки: ', reply_markup=create_kb()["inline_kb_ds_shop"])
        elif callback.data == "steam":
            await callback.answer(text='Steam Gift')
            await bot.edit_message_text(chat_id=callback.message.chat.id, message_id=callback.message.message_id, text='Выберите нужную сумму: ', reply_markup=create_kb()["inline_kb_steam_shop"])
        elif callback.data == "gplay":
            await callback.answer(text='Warning❗Только на полностью турецком аккаунте. Если вы не уверены что эти коды активируються на вашем аккаунте, мы не несем ответсвеность.')
            await bot.edit_message_text(chat_id=callback.message.chat.id, message_id=callback.message.message_id, text='Warning❗Только на полностью турецком аккаунте. Если вы не уверены что эти коды активируються на вашем аккаунте, мы не несем ответсвеность.\nВыберите нужную сумму: ', reply_markup=create_kb()["inline_kb_gplay_shop"])
        elif callback.data == "xbox":
            await callback.answer(text='Xbox Ultimate + Forza 5 Premium')
            await bot.edit_message_text(chat_id=callback.message.chat.id, message_id=callback.message.message_id, text='Xbox GamePass Ultimate + Forza Horizon 5 Premium \n(на ваш аккаунт): ', reply_markup=create_kb()["inline_kb_xbox_shop"])
        elif callback.data == "discord-basic-moth":
            amount = cfg.get_price()["basic_moth"]
            id = callback.from_user.id
            await bot.edit_message_text(chat_id=callback.message.chat.id, message_id=callback.message.message_id, text='Счет создан, что бы оплатить нажмите "Оплатить", что бы проверить оплату нажмите "Проверить", что бы отменить нажмите "Отменить"', reply_markup=create_pay_kb(create_pay(id=id, amount=amount, callback=callback.data)))
        elif callback.data == "discord-basic-year":
            amount = cfg.get_price()["basic_year"]
            id = callback.from_user.id
            await bot.edit_message_text(chat_id=callback.message.chat.id, message_id=callback.message.message_id, text='Счет создан, что бы оплатить нажмите "Оплатить", что бы проверить оплату нажмите "Проверить", что бы отменить нажмите "Отменить"', reply_markup=create_pay_kb(create_pay(id=id, amount=amount, callback=callback.data)))
        elif callback.data == "discord-full-moth":
            amount = cfg.get_price()["full_moth"]
            id = callback.from_user.id
            await bot.edit_message_text(chat_id=callback.message.chat.id, message_id=callback.message.message_id, text='Счет создан, что бы оплатить нажмите "Оплатить", что бы проверить оплату нажмите "Проверить", что бы отменить нажмите "Отменить"', reply_markup=create_pay_kb(create_pay(id=id, amount=amount, callback=callback.data)))
        elif callback.data == "discord-full-year":
            amount = cfg.get_price()["full_year"]
            id = callback.from_user.id
            await bot.edit_message_text(chat_id=callback.message.chat.id, message_id=callback.message.message_id, text='Счет создан, что бы оплатить нажмите "Оплатить", что бы проверить оплату нажмите "Проверить", что бы отменить нажмите "Отменить"', reply_markup=create_pay_kb(create_pay(id=id, amount=amount, callback=callback.data)))
        elif callback.data == "xbox-lifetime":
            amount = cfg.get_price()["xbox_lifetime"]
            id = callback.from_user.id
            await bot.edit_message_text(chat_id=callback.message.chat.id, message_id=callback.message.message_id, text='Счет создан, что бы оплатить нажмите "Оплатить", что бы проверить оплату нажмите "Проверить", что бы отменить нажмите "Отменить"', reply_markup=create_pay_kb(create_pay(id=id, amount=amount, callback=callback.data)))
        elif callback.data == 'steam-rg':
            amount = cfg.get_price()["steam_rg"]
            id = callback.from_user.id
            await bot.edit_message_text(chat_id=callback.message.chat.id, message_id=callback.message.message_id, text='Если вы уже меняли регион в последние 3 месяца, то просто отмените платеж!(Мы не сможем сменить регион в таком случае)\n🚩После смены региона вам нельзя менять пароль, совершать какие-либо покупки, пополнения или продажи на своем аккаунте 3 дня, пользоваться торговой площадкой 5 дней, а также принимать или отправлять подарки 3 дня. К тому же нельзя менять регион 3 месяца.\nСчет создан, что бы оплатить нажмите "Оплатить", что бы проверить оплату нажмите "Проверить", что бы отменить нажмите "Отменить"', reply_markup=create_pay_kb(create_pay(id=id, amount=amount, callback=callback.data)))
        elif callback.data == "steam-wallet-20":
            amount = cfg.get_price()["steam_20"]
            id = callback.from_user.id
            await bot.edit_message_text(chat_id=callback.message.chat.id, message_id=callback.message.message_id, text='Счет создан, что бы оплатить нажмите "Оплатить", что бы проверить оплату нажмите "Проверить", что бы отменить нажмите "Отменить"', reply_markup=create_pay_kb(create_pay(id=id, amount=amount, callback=callback.data)))
        elif callback.data == "steam-wallet-50":
            amount = cfg.get_price()["steam_50"]
            id = callback.from_user.id
            await bot.edit_message_text(chat_id=callback.message.chat.id, message_id=callback.message.message_id, text='Счет создан, что бы оплатить нажмите "Оплатить", что бы проверить оплату нажмите "Проверить", что бы отменить нажмите "Отменить"', reply_markup=create_pay_kb(create_pay(id=id, amount=amount, callback=callback.data)))
        elif callback.data == "steam-wallet-100":
            amount = cfg.get_price()["steam_100"]
            id = callback.from_user.id
            await bot.edit_message_text(chat_id=callback.message.chat.id, message_id=callback.message.message_id, text='Счет создан, что бы оплатить нажмите "Оплатить", что бы проверить оплату нажмите "Проверить", что бы отменить нажмите "Отменить"', reply_markup=create_pay_kb(create_pay(id=id, amount=amount, callback=callback.data)))
        elif callback.data == "steam-wallet-200":
            amount = cfg.get_price()["steam_200"]
            id = callback.from_user.id
            await bot.edit_message_text(chat_id=callback.message.chat.id, message_id=callback.message.message_id, text='Счет создан, что бы оплатить нажмите "Оплатить", что бы проверить оплату нажмите "Проверить", что бы отменить нажмите "Отменить"', reply_markup=create_pay_kb(create_pay(id=id, amount=amount, callback=callback.data)))
        elif callback.data == "google-play-25":
            amount = cfg.get_price()["gplay_25"]
            id = callback.from_user.id
            await bot.edit_message_text(chat_id=callback.message.chat.id, message_id=callback.message.message_id, text='Счет создан, что бы оплатить нажмите "Оплатить", что бы проверить оплату нажмите "Проверить", что бы отменить нажмите "Отменить"', reply_markup=create_pay_kb(create_pay(id=id, amount=amount, callback=callback.data)))
        elif callback.data == "google-play-50":
            amount = cfg.get_price()["gplay_50"]
            id = callback.from_user.id
            await bot.edit_message_text(chat_id=callback.message.chat.id, message_id=callback.message.message_id, text='Счет создан, что бы оплатить нажмите "Оплатить", что бы проверить оплату нажмите "Проверить", что бы отменить нажмите "Отменить"', reply_markup=create_pay_kb(create_pay(id=id, amount=amount, callback=callback.data)))
        elif callback.data == "google-play-100":
            amount = cfg.get_price()["gplay_100"]
            id = callback.from_user.id
            await bot.edit_message_text(chat_id=callback.message.chat.id, message_id=callback.message.message_id, text='Счет создан, что бы оплатить нажмите "Оплатить", что бы проверить оплату нажмите "Проверить", что бы отменить нажмите "Отменить"', reply_markup=create_pay_kb(create_pay(id=id, amount=amount, callback=callback.data)))
        elif callback.data == "google-play-250":
            amount = cfg.get_price()["gplay_250"]
            id = callback.from_user.id
            await bot.edit_message_text(chat_id=callback.message.chat.id, message_id=callback.message.message_id, text='Счет создан, что бы оплатить нажмите "Оплатить", что бы проверить оплату нажмите "Проверить", что бы отменить нажмите "Отменить"', reply_markup=create_pay_kb(create_pay(id=id, amount=amount, callback=callback.data)))
        elif callback.data == "google-play-500":
            amount = cfg.get_price()["gplay_500"]
            id = callback.from_user.id
            await bot.edit_message_text(chat_id=callback.message.chat.id, message_id=callback.message.message_id, text='Счет создан, что бы оплатить нажмите "Оплатить", что бы проверить оплату нажмите "Проверить", что бы отменить нажмите "Отменить"', reply_markup=create_pay_kb(create_pay(id=id, amount=amount, callback=callback.data)))
        elif callback.data == "google-play-1000":
            amount = cfg.get_price()["gplay_1000"]
            id = callback.from_user.id
            await bot.edit_message_text(chat_id=callback.message.chat.id, message_id=callback.message.message_id, text='Счет создан, что бы оплатить нажмите "Оплатить", что бы проверить оплату нажмите "Проверить", что бы отменить нажмите "Отменить"', reply_markup=create_pay_kb(create_pay(id=id, amount=amount, callback=callback.data)))
        elif callback.data == "check":
            id = callback.from_user.id
            bill_id = BotDB.CheckPay(id)[0]
            if BotDB.CheckPay(id)[1] ==p2p.check(bill_id).comment:
                status = p2p.check(bill_id).status
                await bot.send_message(chat_id=callback.message.chat.id, text=f"Статус платежа: {status}")
                if status == "PAID":
                    await bot.delete_message(chat_id=callback.message.chat.id, message_id=callback.message.message_id)
                    BotDB.addBill(id)
                    purchase = str(((p2p.check(bill_id).comment).split("_")[2]).replace("-", " ") + " " + (p2p.check(bill_id).comment).split("_")[1] + " руб.")
                    BotDB.add_purchases(id, purchase)
                    if "xbox-lifetime" in ((p2p.check(bill_id).comment).split("_")[2]):
                        BotDB.add_subscribe(id, 1)
                        await bot.send_message(chat_id=callback.message.chat.id, text = "Спасибо за покупку!", reply_markup=create_main_kb(BotDB.check_subscribe(callback.message.chat.id)))
                        BotDB.create_task(id, callback.from_user.username, "XBOX LIFE TIME", p2p.check(bill_id).amount, 1)
                    elif "discord" in ((p2p.check(bill_id).comment).split("_")[2]):
                        BotDB.create_task(id, callback.from_user.username, (p2p.check(bill_id).comment).split("_")[2], p2p.check(bill_id).amount, 0)
                        await bot.send_message(chat_id=callback.message.chat.id, text = "Спасибо за покупку! Мы уведомим вас, как начнем выполнять заказ!", reply_markup=create_main_kb(BotDB.check_subscribe(callback.message.chat.id)))
                        product = (p2p.check(bill_id).comment).split("_")[2]
                        for i in (cfg.managers).split(", "):
                            await bot.send_message(i, f"Пользователь: {callback.from_user.id}(ник: {callback.from_user.username}), оплатил заказ: {product}, ценной: {p2p.check(bill_id).amount} руб.")
                    elif "google-play" in ((p2p.check(bill_id).comment).split("_")[2]):
                        if cfg.gplay_auto==False:
                            BotDB.create_task(id, callback.from_user.username, (p2p.check(bill_id).comment).split("_")[2], p2p.check(bill_id).amount, 0)
                            await bot.send_message(chat_id=callback.message.chat.id, text = "Спасибо за покупку! Мы уведомим вас, как начнем выполнять заказ!", reply_markup=create_main_kb(BotDB.check_subscribe(callback.message.chat.id)))
                            product = (p2p.check(bill_id).comment).split("_")[2]
                            for i in (cfg.managers).split(", "):
                                await bot.send_message(i, f"Пользователь: {callback.from_user.id}(ник: {callback.from_user.username}), оплатил заказ: {product}, ценной: {p2p.check(bill_id).amount} руб.")
                        else:
                            BotDB.create_task(id, callback.from_user.username, (p2p.check(bill_id).comment).split("_")[2], p2p.check(bill_id).amount, 1)
                            await bot.send_message(chat_id=callback.from_user.id, text=f"Спасибо за покупку! Ваш ключ {123}")
                    elif "steam-wallet" in ((p2p.check(bill_id).comment).split("_")[2]):
                        if cfg.steam_auto==False:
                            BotDB.create_task(id, callback.from_user.username, (p2p.check(bill_id).comment).split("_")[2], p2p.check(bill_id).amount, 0)
                            await bot.send_message(chat_id=callback.message.chat.id, text = "Спасибо за покупку! Мы уведомим вас, как начнем выполнять заказ!", reply_markup=create_main_kb(BotDB.check_subscribe(callback.message.chat.id)))
                            product = (p2p.check(bill_id).comment).split("_")[2]
                            for i in (cfg.managers).split(", "):
                                await bot.send_message(i, f"Пользователь: {callback.from_user.id}(ник: {callback.from_user.username}), оплатил заказ: {product}, ценной: {p2p.check(bill_id).amount} руб.")
                        else:
                            BotDB.create_task(id, callback.from_user.username, (p2p.check(bill_id).comment).split("_")[2], p2p.check(bill_id).amount, 1)
                            await bot.send_message(chat_id=callback.from_user.id, text=f"Спасибо за покупку! Ваш ключ {123}")
                    elif "steam-rg" in ((p2p.check(bill_id).comment).split("_")[2]):
                        BotDB.create_task(id, callback.from_user.username, (p2p.check(bill_id).comment).split("_")[2], p2p.check(bill_id).amount, 0)
                        await bot.send_message(chat_id=callback.message.chat.id, text = "Спасибо за покупку! Мы уведомим вас, как начнем выполнять заказ!", reply_markup=create_main_kb(BotDB.check_subscribe(callback.message.chat.id)))
                        product = (p2p.check(bill_id).comment).split("_")[2]
                        for i in (cfg.managers).split(", "):
                            await bot.send_message(i, f"Пользователь: {callback.from_user.id}(ник: {callback.from_user.username}), оплатил заказ: {product}, ценной: {p2p.check(bill_id).amount} руб.")
            else:
                await bot.send_message(chat_id=callback.message.chat.id, text=f"Мы не нашли ваш платеж!")
        elif callback.data == "reject":
            id = callback.from_user.id
            bill_id = BotDB.CheckPay(id)[0]
            if BotDB.CheckPay(id)[1] ==p2p.check(bill_id).comment and p2p.check(bill_id).status != "PAID" or "REJECT":
                p2p.reject(bill_id)
                status = p2p.check(bill_id).status
                await bot.send_message(chat_id=callback.message.chat.id, text=f"Ваш платеж закрыт!\nСтатус платежа: {status}")
                await bot.delete_message(chat_id=callback.message.chat.id, message_id=callback.message.message_id)
            else:
                await bot.send_message(chat_id=callback.message.chat.id, text=f"Мы не нашли ваш платеж! Или он уже оплачен/закрыт.")
        elif callback.data == "history":
            id = callback.from_user.id
            purchases = BotDB.get_purchases(id)
            await bot.send_message(chat_id=callback.message.chat.id, text=f"Ваша история покупок:\n{purchases}")
        if callback.data == 'back':
            await bot.edit_message_text(chat_id=callback.message.chat.id, message_id=callback.message.message_id, text='Выберите категорию: ', reply_markup=create_main_inline_kb())
        if callback.data == "otziv":
            await BotStatesGroup.otziv.set()
            await bot.edit_message_text(chat_id=callback.message.chat.id, message_id=callback.message.message_id, text="Напишите сюда сообщение и оно отправить в группу с отзывами(@quade_shop_reviews): ", reply_markup=None)
            @dp.message_handler(state=BotStatesGroup.otziv)
            async def otziv(message: types.Message, state: FSMContext):
                await bot.send_message(chat_id=BotDB.get_admin_id(message.from_user.id), text=f"Пользователь {message.from_user.id}({message.from_user.username}), оставил отзыв: {message.text}")
                await bot.forward_message(chat_id = "-1001564221496", from_chat_id=message.from_user.id, message_id=message.message_id)
                await state.finish()
        if callback.data == 'start_msg':
            if BotDB.check_task_Status(callback.from_user.id) == True:
                await bot.edit_message_text(chat_id=callback.from_user.id, message_id=callback.message.message_id, text="Теперь ваши сообщения дойдут до админа!")
                await BotStatesGroup.start_user_vpl.set()
                @dp.message_handler(state=BotStatesGroup.start_user_vpl)
                async def start_vpl_user(message: types.Message, state: FSMContext):
                    if BotDB.check_task_Status(message.from_user.id) == True:
                        if BotDB.check_pause(message.from_user.id) == False:
                            temp = f"{message.from_user.id}:\n{message.text}"
                            await bot.send_message(chat_id=BotDB.get_admin_id(message.from_user.id), text=temp)
                        else:
                            BotDB.save_message(id=message.from_user.id, message=message.text)
                    else:
                        await state.finish()
                    
                @dp.message_handler(content_types=['photo'], state=BotStatesGroup.start_user_vpl)
                async def start_vpl_user_photo(message: types.Message, state: FSMContext):
                    if BotDB.check_task_Status(message.from_user.id) == True:
                        temp = message.photo[0].file_id
                        temp_text = f"{message.from_user.id}:\n{message.caption}"
                        await bot.send_photo(chat_id=BotDB.get_admin_id(message.from_user.id), photo=temp, caption=temp_text)
                    else:
                        await state.finish()
            else:
                await bot.send_message(chat_id=callback.from_user.id, text="На данный момент, не один ваш заказ не выполняеться. Вы не можете начать чат. Если у вас остались вопросы напишите в поддержку: @quade_help_bot")
        if str(callback.from_user.id) in cfg.managers.split(", "):
            item = callback.data.replace("(", "").replace(")", "").split(",")
            item_old = item
            if BotDB.check_pause(id=item[0]) == True or BotDB.check_task_Status(id=item[0]) == False:
                if callback.data in str(list(BotDB.get_task())):
                    item = callback.data
                    if BotDB.check_pause(id=int(item_old[0])) == True:
                        yes = InlineKeyboardButton('Продолжить выполнять', callback_data=str(item))
                    else:
                        yes = InlineKeyboardButton('Начать выполнять', callback_data=str(item))
                    back = InlineKeyboardButton('Назад', callback_data='back_pr')
                    inline_kb_yes = InlineKeyboardMarkup()
                    inline_kb_yes.add(yes, back)
                    await BotStatesGroup.waiting_ad_vpl.set()
                    await bot.edit_message_text(chat_id=callback.from_user.id, message_id=callback.message.message_id, text=str(item), reply_markup=inline_kb_yes)
            else:
                await bot.send_message(chat_id=callback.from_user.id, text="Один из заказов пользователя уже выполняеться, вы можете выбрать другой!")
                keyboard = types.InlineKeyboardMarkup()
                button_list = []
                for item in list(BotDB.get_task()):
                    button_list.append(types.InlineKeyboardButton(text=str(item), callback_data=str(item)))
                keyboard.add(*button_list)
                await bot.send_message(chat_id=callback.from_user.id, text='Ваши заказы к выполнению: ', reply_markup=keyboard)
    else:
        await bot.send_message(chat_id=callback.from_user.id, text="Вы не зарегестрированы! Для начала использования бота, используйте команду /start")

@dp.callback_query_handler(state=BotStatesGroup.waiting_ad_vpl)
async def waiting_adm(callback: types.CallbackQuery, state: FSMContext):
    if str(callback.from_user.id) in cfg.managers.split(", "):
        if callback.data in f"{list(BotDB.get_task())}":
            item = callback.data.replace("(", "").replace(")", "").split(",")
            if BotDB.check_pause(id=item[0]) == False:
                BotDB.create_old_task(item[0], item[2], callback.from_user.id)
                await bot.edit_message_text(chat_id=callback.from_user.id, message_id=callback.message.message_id, text=f"Вы начали выпонлнять заказ: <b>'{str(item)}'</b>", parse_mode="html")
                await bot.send_message(chat_id=callback.from_user.id, text="Пишите сюда что бы написать собеседнику: ", reply_markup=kb_vpl)
                await bot.send_message(chat_id=item[0], text=f"Ваш заказ <b>{item[2]}</b> начал выполняться!", parse_mode="html")
                await bot.send_message(chat_id=item[0], text="Что бы начать чат с админом нажмите 'Начать общение': ", reply_markup=kb_start_msg)
            else:
                await bot.edit_message_text(chat_id=callback.from_user.id, message_id=callback.message.message_id, text=f"Вы продолжили выполнять заказ: <b>'{str(item)}'</b>", parse_mode="html")
                await bot.send_message(chat_id=callback.from_user.id, text="Сообщения пользователя на паузе: ", reply_markup=kb_vpl)
                for i in (str(BotDB.get_message(item[0]))[1:-3]).split("/new/"):
                    await bot.send_message(chat_id=callback.from_user.id, text=i)
            await BotStatesGroup.statr_vpl.set()
            @dp.message_handler(state=BotStatesGroup.statr_vpl)
            async def start_vpl(message: types.Message, state: FSMContext):
                if message.text == "Закончить выполнение!":
                    id=item[0]
                    task=str(item[2]).replace(" ", '').replace("'", '')
                    BotDB.task_stop(int(id), task)
                    BotDB.delete_old_task(int(id))
                    await message.reply(f"Вы закончили выполнять заказ {task}, для пользователя {id}", reply_markup=kb_admin)
                    await bot.send_message(chat_id=int(id), text=f"Ваш заказ <b>{task}</b> успешно выполнен!\nХотите оставить отзыв?", parse_mode="html", reply_markup=otizv_kb)
                    await state.finish()
                elif message.text == "Отправить кнопку 'Начать общение'":
                    id=item[0]
                    await bot.send_message(chat_id=int(id), text=f"Что бы начать чат с админом нажмите 'Начать общение':", reply_markup=kb_start_msg)
                elif message.text == "Поставить заказ на паузу":
                    id=item[0]
                    task=str(item[2]).replace(" ", '').replace("'", '')
                    BotDB.pause_task(id)
                    await bot.send_message(chat_id=message.from_user.id, text=f"Вы поставили выполнение заказа: {id}, {task} на паузу.", reply_markup=kb_admin)
                    await state.finish()
                else:
                    temp = message.text
                    id = item[0]
                    await bot.send_message(chat_id=id, text=temp)
            @dp.message_handler(content_types=['photo'], state=BotStatesGroup.statr_vpl)
            async def start_vpl1(message: types.Message, state: FSMContext):
                temp = message.photo[0].file_id
                temp_text = message.caption
                id = item[0]
                await bot.send_photo(chat_id=id, photo=temp, caption=temp_text)
        if callback.data == "back_pr":
            if str(callback.from_user.id) in cfg.managers.split(", "):
                keyboard = types.InlineKeyboardMarkup()
                button_list = []
                for item in list(BotDB.get_task()):
                    button_list.append(types.InlineKeyboardButton(text=str(item), callback_data=str(item)))
                keyboard.add(*button_list)
                await state.finish()
                await bot.edit_message_text(chat_id=callback.from_user.id, message_id=callback.message.message_id, text='Ваши заказы к выполнению: ', reply_markup=keyboard)

@dp.message_handler(text="Рассылка")
async def rassl(message: types.Message, state: FSMContext):
    if str(message.from_user.id) in cfg.admins.split(", "):
        await BotStatesGroup.rassl.set()
        await bot.send_message(chat_id=message.from_user.id, text="Напишите сюда что бы разослать сообщение всем пользователям: ", reply_markup=None)
        @dp.message_handler(state=BotStatesGroup.rassl)
        async def rassl(message: types.Message, state: FSMContext):
            temp = message.text
            id_list = (str(BotDB.get_all_id()).replace("(", "").replace(",)", "").replace("[", "").replace("]", "")).split(", ")
            logging.info(f"{id_list, type(id_list)}", exc_info=True)
            await message.answer("Начинаю рассылку!")
            await state.finish()
            for i in id_list:
                try:
                    await bot.send_message(chat_id=int(i), text=temp)
                except:
                    logging.error(f"{i} DA {id_list}", exc_info=True)
            await message.answer("Все сообщения успешно доставлены!")
        @dp.message_handler(state=BotStatesGroup.rassl, content_types=['photo'])
        async def rassl_photo(message: types.Message, state: FSMContext):
            temp = message.photo[0].file_id
            temp_text = message.caption
            id_list = (str(BotDB.get_all_id()).replace("(", "").replace(",)", "").replace("[", "").replace("]", "")).split(", ")
            await message.answer("Начинаю рассылку!")
            await state.finish()
            for i in id_list:
                await bot.send_photo(chat_id=int(i), photo=temp, caption=temp_text)
            await message.answer("Все сообщения успешно доставлены!")
    else:
        await message.reply("У вас нет прав.")

@dp.message_handler(text="🌈Профиль")
async def shop(message: types.Message):
    id = message.from_user.id
    if check_reg(id) == True:
        if str(message.from_user.id) in cfg.admins.split(", "):
            status = "Админ"
        elif str(message.from_user.id) in cfg.managers.split(", "):
            status = "Менеджер"
        else:
            status = "Пользователь"
        if BotDB.check_subscribe(id) == True:
            subscribe = "Game Pass + Forza"
        else:
            subscribe = "Отсутствует"
        count = BotDB.get_stat(id)
        await message.reply(f"<b>Ваш профиль:</b> {message.from_user.username} ✅\n<b>Статус:</b> {status}\n<b>Подписка:</b> {subscribe}\n<b>Количество сделок:</b> {count}", parse_mode="html", reply_markup=inline_kb_history)
    else:
        await message.reply(f"Вам нужно зарегестрироваться, для этого пропишите /start")

@dp.message_handler(text="Статистика")
async def admin_stat(message: types.Message):   
    if str(message.from_user.id) in cfg.admins.split(", "):
        await message.reply(f"*Количество пользователей:* {BotDB.countUser()}\n*Новых пользователей:* {1}\n*Общее количество сделок:* {BotDB.get_count_purchase()}\n*Сделок за сегодня:* {1}\n*Сумма сделок за сегодня:* {1}\n*Общая сумма сделок:* {BotDB.get_sum_purchase_all()}\n*Чистая прибль за сегодня:* {1}\n*Чистая прибль за все время:* {1}", parse_mode="Markdown")


@dp.message_handler(text="Данные✉")
async def xbox_data(message: types.Message):
    if BotDB.check_subscribe(message.from_user.id)==True:
        keyboard = InlineKeyboardButton("Туториал", callback_data='tutorial', url="https://telegra.ph/Forza-Horizon-Aktivaciya-04-27")
        inl_tutor = InlineKeyboardMarkup()
        inl_tutor.add(keyboard)
        await message.reply(f"Логин: {parse.get_data()[0]} Пароль: {parse.get_data()[1]}")
        await message.answer(f"Если пароль поменялся, новый всегда будет здесь, не нужно никуда писать!!!", reply_markup=inl_tutor)
    else:
        await message.reply(f"У вас нет доступа")

@dp.message_handler(text="🌟Поддержка")
async def shop(message: types.Message):
    await message.reply(f"@quade_help_bot - Обратиться за помощью🚀 (на данный момент не работает, со всеми вопросами пишите @ne_martoy)")

@dp.message_handler(text="Назад")
async def back(message: types.Message):
    id = message.from_user.id
    if check_reg(id) == True:
        await message.reply("Привет! Это Quade Shop. \nВыбери из предложенных вариантов:", reply_markup=create_main_kb(BotDB.check_subscribe(message.from_user.id)))
    else:
        await message.reply(f"Вам нужно зарегестрироваться, для этого пропишите /start")

@dp.message_handler(text="Заказы к выполнению")
async def execution(message: types.Message):
    if str(message.from_user.id) in cfg.managers.split(", "):
        keyboard = types.InlineKeyboardMarkup()
        button_list = []
        for item in list(BotDB.get_task()):
            button_list.append(types.InlineKeyboardButton(text=str(item), callback_data=str(item)))
        keyboard.add(*button_list)
        await message.answer('Ваши заказы к выполнению: ', reply_markup=keyboard)


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
