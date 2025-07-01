
import re

import telepot

# from setup.models import BaseSettings

try:
    token = "7741920090:AAGnnRpe_b77Eq9gUpPcZHxXxrzWBmTueAI"
    my_id = "1144946799"
except:
    token = ''
    my_id = ''


telegramBot = telepot.Bot(token)

def send_message(text):
    telegramBot.sendMessage(my_id, text, parse_mode="Markdown")


def order_telegram(order):
    pr = []

    for item in order.items.all():
        pr_name = item.first_name
        pr_quantity = item.quantity
        pr_price = str(item.price)

        pr_summ = pr_quantity * item.price


        pr.append({

            'Название':pr_name,
            'Количество':pr_quantity,
            'Цена':pr_price,
            'Итого': str(pr_summ),
        })

    res = re.sub(r"[#%!@*{}]", "\n", str(pr))
    res = re.sub(r"[',]", "", res)

    message = "Заявка с сайта: " + "\n" + "*Номер заказа*: " +str(order.id) + "\n" + "*Телефон*: " + str(order.phone) + "\n" + "*Оплата*: " +str(order.pay_method)+ "\n" + "*Доставка*: " + "\n" + "*Товары*: " + "\n" + str(res) + "\n"

    try:
        send_message(message)
    except Exception as e:
        print(e)
