#!/bin/python3
import telebot
import requests
import json
import os

global nInfo1
global nInfo2
nInfo1 = "absInfoFirstSheet.txt"
nInfo2 = "absInfoSecondSheet.txt"
dUpdate_text = "Обновить файлы - удаление существующих файлов и создание на их замену новых с новым содержимым" \
               "которое будет получено с таблицы\n\n"
dOpen_text = "Открыть файлы - которые возможно открыть и посмотреть их содержимое\n\n"
dCancel_text = "Главное меню - возврат на главное меню"
rGroup_text = "Группы - список групп, учащихся у тебя\n\n"
rSubject_text = "Дисциплины - список дисциплин, что ты ведёшь\n\n"
rLink_text = "Ссылки - список ссылок на доки с более подробной информацией о каждой группе\n\n"
rCancel_text = "Главное меню - возврат на главное меню"
unresolved_message = "На всякую хрень не отвечаю, якобы отсутствие чувств проявляю, оскорблять не стоит🗿🗿🗿"

class isheet:
    """
    rc_mark: a marks that we will sent
    tid: sheets'es id
    sid: sheet's name
    surl: sheet's api url
    google_token: a token that can used in refresh token
    tgbot_token: a bot's token, nothing interesting
    """
    rc_mark = {'П', 'Н', 'Б', 'О'}
    tid = ''
    sid1 = '1сем-Осень'
    sid2 = '2сем-Весна'
    google_token = '1//0ckdqe3fJ4-LRCgYIARAAGAwSNwF-L9IrmPKSdeA2eL0DzmYocxM9J5oENiVZZzcfSix2f9DtcdmC89OJbimZdoWiSuCfu5ikeVc'
    tgbot_token = "1277500164:AAEkU8DbjZX0E6wRa3JDKUKumIjlOuSLsRM"
    url_token = "https://oauth2.googleapis.com/token"
    gclient_id = "173493138930-85ifhekbvi7iak312hvbcok3f8466hn6.apps.googleusercontent.com"
    gclient_secret = "wVPZmRRZquXcrcZ53Ygryj7C"

    def __init__(self, access_token):
        self.acc_token = access_token


class get_new_token:
    payload = f"client_id={isheet.gclient_id}&client_secret={isheet.gclient_secret}&grant_type=refresh_token&refresh_token={isheet.google_token}"
    headers = {
        'charset': 'UTF-8',
        'Content-Type': 'application/x-www-form-urlencoded'
    }


tg = telebot.TeleBot(isheet.tgbot_token)
keyboard_main_menu = telebot.types.ReplyKeyboardMarkup()
keyboard_main_remove = telebot.types.ReplyKeyboardRemove()
keyboard_main_menu.row('Выгрузить таблицу')
keyboard_main_menu.add('Настройки файлов', 'Закрыть')
keyboard_update_menu = telebot.types.ReplyKeyboardMarkup()
keyboard_update_remove = telebot.types.ReplyKeyboardRemove()
keyboard_update_menu.row("Обновить файлы", "Открыть файлы")
keyboard_update_menu.add("Главное меню", "")
keyboard_read_menu = telebot.types.ReplyKeyboardMarkup()
keyboard_read_remove = telebot.types.ReplyKeyboardRemove()
keyboard_read_menu.row("Группы", "Дисциплины")
keyboard_read_menu.add("Ссылки", "Главное меню")


def addFile(allInfoCols1, allInfoRows1, urls1, allInforCols2, allInfoRows2, urls2, bollForChoice, mid):
    print('а это внутри функции...')
    _allInfoCols1 = json.loads(allInfoCols1.text)
    _allInfoRows1 = json.loads(allInfoRows1.text)
    _urls1 = json.loads(urls1.text)
    _allInforCols2 = json.loads(allInforCols2.text)
    _allInfoRows2 = json.loads(allInfoRows2.text)
    _urls2 = json.loads(urls2.text)
    # with open(nInfo1, "w+") as file:
    #     for i in _allInfoCols1:
    #         tg.send_message(mid, _allInfoCols1[2][0][i])
    ff = _allInfoRows1['values']
    print(ff)
    with open(f"iFiles/{nInfo1}", "w+") as file:
        for line in ff:
            f = " ".join(line[1:])
            file.write(f + '\n')


@tg.message_handler(commands=['get_token'])
def gtoken(message):
    rtest = requests.request("POST", isheet.url_token, headers=get_new_token.headers, data=get_new_token.payload)
    prtest = json.loads(rtest.text)
    access_token = prtest['access_token']
    print(access_token)
    return access_token


@tg.message_handler(commands=['start'])
def sendFirstMessage(message):
    global access_token
    fStartText = "Привет, давай начнём работу\n"
    mid = message.chat.id
    dirList = list(os.listdir("iFiles"))
    if nInfo1 in dirList:
        gmsg = tg.send_message(mid, f"{fStartText}\nФайлы в порядке, можно работать", reply_markup=keyboard_main_menu)
        tg.register_next_step_handler(gmsg, main_choice_menu)
    else:
        bmsg = tg.send_message(mid, f"{fStartText}\nОтсутствуют файлы для работы, отправь мне"
                                    f"ссылку на Таблицу, введя ссылку в"
                                    f"поле ввода, она находится ниже, рекомендуется"
                                    f"перед отправкой убедиться, что доступ к Таблице у "
                                    f"бота имеется, ссылка корректна и имеет актуальный "
                                    f"айди Таблицы", reply_markup=keyboard_main_remove)
        access_token = gtoken(message)
        tg.register_next_step_handler(bmsg, getUrl)


def main_setting_menu(smessage):
    sid = smessage.chat.id
    if smessage.text == "Обновить файлы":
        checkpoint = False
        tg.register_next_step_handler(checkpoint, main_setting_menu)
    elif smessage.text == "Открыть файлы":
        checkpoint = tg.send_message(sid, "Работает Открыть файлы")
        tg.register_next_step_handler(checkpoint, main_setting_menu)
    elif smessage.text == "Главное меню":
        sendFirstMessage(smessage)

    else:
        checkpoint = tg.send_message(sid, unresolved_message)
        tg.register_next_step_handler(checkpoint, main_setting_menu)


def update_file(message):
    uid = message.chat.id


def main_choice_menu(call):
    cid = call.chat.id
    if call.text == "Настройки файлов":
        checkpoint = tg.send_message(cid, dUpdate_text + dOpen_text + dCancel_text, reply_markup=keyboard_update_menu)
        tg.register_next_step_handler(checkpoint, main_setting_menu)
    elif call.text == "Выгрузить таблицу":
        checkpoint = tg.send_message(cid, rGroup_text + rSubject_text + rLink_text + rCancel_text,
                                     reply_markup=keyboard_read_menu)
    elif call.text == "Закрыть":
        tg.send_message(cid, "Чтобы снова получить доступ к боту, пропиши или нажми на /start",
                        reply_markup=keyboard_main_remove)
    else:
        checkpoint = tg.send_message(cid, unresolved_message)
        tg.register_next_step_handler(checkpoint, main_choice_menu)


def getUrl(gmessage):
    global irul
    mid = gmessage.chat.id
    tid = '/'.join(gmessage.text.split('/')[5:][:-1])
    print(tid)
    surl1 = f"https://sheets.googleapis.com/v4/spreadsheets/{tid}/values/{isheet.sid1}"
    surl2 = f"https://sheets.googleapis.com/v4/spreadsheets/{tid}/values/{isheet.sid2}"
    try:
        tg.send_message(mid, "Попытка загрузки...")
        gtest_col1 = requests.get(f"{surl1}!A:O?access_token={access_token}&majorDimension=COLUMNS")
        print(gtest_col1)
        if gtest_col1.status_code != 200:
            tg.send_message(mid, f"{isheet.sid1} в виде столбцов - ❌")
        else:
            tg.send_message(mid, f"{isheet.sid1} в виде столбцов - ✔️")
        gtest_rows1 = requests.get(f"{surl1}!A:O?access_token={access_token}&majorDimension=ROWS")
        tg.send_message(mid, "33%")
        if gtest_rows1.status_code != 200:
            tg.send_message(mid, f"{isheet.sid1} в виде строк - ❌")
        else:
            tg.send_message(mid, f"{isheet.sid1} в виде строк - ✔️")
        gtest_urls1 = requests.get(f"{surl1}!C:C?access_token={access_token}&majorDimension=COLUMNS")
        tg.send_message(mid, "40%")
        if gtest_urls1.status_code != 200:
            tg.send_message(mid, f"{isheet.sid1} ссылки - ❌")
        else:
            tg.send_message(mid, f"{isheet.sid1} ссылки - ✔️")
        gtest_col2 = requests.get(f"{surl1}!A:O?access_token={access_token}&majorDimension=COLUMNS")
        tg.send_message(mid, "56%")
        if gtest_col2.status_code != 200:
            tg.send_message(mid, f"{isheet.sid2} в виде столбцов - ❌")
        else:
            tg.send_message(mid, f"{isheet.sid2} в виде столбцов - ✔️")
        gtest_rows2 = requests.get(f"{surl2}!A:O?access_token={access_token}&majorDimension=ROWS")
        tg.send_message(mid, "82%")
        if gtest_rows2.status_code != 200:
            tg.send_message(mid, f"{isheet.sid2} в виде строк - ❌")
        else:
            tg.send_message(mid, f"{isheet.sid2} в виде строк - ✔️")
        gtest_urls2 = requests.get(f"{surl2}!C:C?access_token={access_token}&majorDimension=COLUMNS")
        if gtest_urls2.status_code != 200:
            tg.send_message(mid, f"{isheet.sid2} ссылки - ❌")
        else:
            tg.send_message(mid, f"{isheet.sid2} ссылки - ✔️")
        tg.send_message(mid, "100%")
        if gtest_col1.status_code == 200:
            tg.send_message(mid, "Загрузил:)")
            '''Функция которая будет создавать файл и в него все все все загружать'''
            print('ну тип тут функция вроде бы...')
            addFile(gtest_col1, gtest_rows1, gtest_urls1, gtest_col2, gtest_rows2, gtest_urls2, True, mid)
            return sendFirstMessage(gmessage)
        else:
            tg.send_message((mid, f"Ошибка {gtest_col1.status_code}"))
    except:
        if gtest_col1.status_code == 403:
            tg.send_message(mid, f"Ошибка {gtest_col1.status_code}, введённые значения не верны, "
                                 f"попробуй ещё раз")
        if gtest_col1.status_code == 404:
            tg.send_message(mid, f"Такой Таблицы не существует ({gtest_col1.status_code})")
        if gtest_col1.status_code == 400:
            tg.send_message(mid,
                            f"Я ничего не загрузил, у меня {gtest_col1.status_code}, пересмотри введённые"
                            f"данные!")


tg.polling()
