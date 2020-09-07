import requests
from bs4 import BeautifulSoup
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
import math
import datetime
import json
import schedule
import calendar

token = '1f357011004d3f409515afbe4844a0cfe4dffaa26268e22758a4b1e32b328dcca0fe96db2eb5af0bd8dd3'
vk_session = vk_api.VkApi(token = token)
vk = vk_session.get_api()
longpoll = VkLongPoll(vk_session)

Monday = []
Tuesday = []
Wednesday = []
Thursday = []
Friday = []

times = ['08:15-09:05','10:00-10:50','11:45-12:35-13:25','14:20-15:10','16:05-16:55','17:50-18:40']

errors = ['error#1: Ошибка. Группа не найдена.','error#2: Ошибка. Команда не найдена. Используйте "главная".','error#3: Ошибка. Вы еще не ввели группу.']

keyboard = {'one_time': True,
            'buttons':
            [
                [
                    {'action':
                        {'type':'text', 
                        'label':'Расписание'},
                    'color':'positive',
                    },
                    {'action':
                        {'type':'text', 
                        'label':'Изменить группу'},
                    'color':'positive',
                    }
                ]
            ]
            }
            
key = {'one_time': True,
            'buttons':
            [
                [
                    {'action':
                        {'type':'text', 
                        'label':'Понедельник'},
                    'color':'positive',
                    },
                    {'action':
                        {'type':'text', 
                        'label':'Вторник'},
                    'color':'positive',
                    },
                    {'action':
                        {'type':'text', 
                        'label':'Среда'},
                    'color':'positive',
                    }
                ],
                [
                     {'action':
                        {'type':'text', 
                        'label':'Четверг'},
                    'color':'positive',
                    },
                     {'action':
                        {'type':'text', 
                        'label':'Пятница'},
                    'color':'positive',
                    },
                    {'action':
                        {'type':'text', 
                        'label':'Главная'},
                    'color':'positive',
                    },
                ]
            ]
            }           
            
def output(param):
    if param.lower() == 'понедельник' or param.lower() == 'пнд' or param.lower() == 'monday':
        print('~~~~~~~~~~~Monday~~~~~~~~~~~')
        for day1 in Monday:
            print(day1)
    elif param.lower() == 'вторник' or param.lower() == 'вт' or param.lower() == 'tuesday':        
        print('~~~~~~~~~~~Tuesday~~~~~~~~~~~')
        for day2 in Tuesday:
            print(day2)
    elif param.lower() == 'среда' or param.lower() == 'ср' or param.lower() == 'wednesday':
        print('~~~~~~~~~~~Wednesday~~~~~~~~~~~')
        for day3 in Wednesday:
            print(day3)
    elif param.lower() == 'четверг' or param.lower() == 'чт' or param.lower() == 'thursday':
        print('~~~~~~~~~~~Thursday~~~~~~~~~~~')
        for day4 in Thursday:
            print(day4)
    elif param.lower() == 'пятница' or param.lower() == 'пт' or param.lower() == 'friday':
        print('~~~~~~~~~~~Friday~~~~~~~~~~~')
        for day5 in Friday:
            print(day5)
    elif param.lower() == 'неделя' or param.lower() == 'weak':
        print('~~~~~~~~~~~Monday~~~~~~~~~~~')
        for day1 in Monday:
            print(day1)
        print('~~~~~~~~~~~Tuesday~~~~~~~~~~~')
        for day2 in Tuesday:
            print(day2)
        print('~~~~~~~~~~~Wednesday~~~~~~~~~~~')
        for day3 in Wednesday:
            print(day3)
        print('~~~~~~~~~~~Thursday~~~~~~~~~~~')
        for day4 in Thursday:
            print(day4)
        print('~~~~~~~~~~~Friday~~~~~~~~~~~')
        for day5 in Friday:
            print(day5)
    else:
        print('error')
    
        
def add(i, full):
    if i == 1 or i == 7 or i == 13 or i == 19 or i == 25 or i == 31:
        Monday.append(full)
    elif i == 2 or i == 8 or i == 14 or i == 20 or i == 26 or i == 32:
        Tuesday.append(full)
    elif i == 3 or i == 9 or i == 15 or i == 21 or i == 27 or i == 33:
        Wednesday.append(full)
    elif i == 4 or i == 10 or i == 16 or i == 22 or i == 28 or i == 34:
        Thursday.append(full)
    elif i == 5 or i == 11 or i == 17 or i == 23 or i == 29 or i == 35:
        Friday.append(full)
    
def test(i,item,znam):
    p = ''
    y = ''
    d = ''
    s = 0
    full = ''
    if item.text != ' ':
        if item.find('table', class_ = 'inner'):
            check = item.findAll('td', class_ = 'schedule_half')
            for che in check:
                if s%2 != znam:
                    if che.find('div', class_ = 'place_half'):
                        y = che.find('div', class_ = 'place_half').get_text()
                    if che.find('div', class_ = 'subject_half'):
                        p = che.find('div', class_ = 'subject_half').get('title')
                    if che.find('div', class_ = 'sp_half'):
                        d = che.find('div', class_ = 'sp_half').get_text()
                    if p != '' and y != '' and d != '':
                        full = times[math.floor((i)/6)]+' '+p+' '+d+' '+y+'\n'
                        add(i,full) 
                    s = s+1
                else:
                    s=s+1
        else:
            if item.find('div', class_ = 'place_std'):
                y = item.find('div', class_ = 'place_std').get_text()
            if item.find('div', class_ = 'subject_std'):
                p = item.find('div', class_ = 'subject_std').get('title')
            if item.find('div', class_ = 'sp_std'):
                d = item.find('div', class_ = 'sp_std').get_text()
            if p != '' and y != '' and d != '':
                full = times[math.floor((i)/6)]+' '+p+' '+d+' '+y+'\n'
                add(i,full)
  


  
def send_msg(id, text):
    vk.messages.send(user_id = id, message = text, random_id = 0)

def send_stick(id, number):
    vk.messages.send(user_id = id, sticker_id = number, random_id = 0)

def send_photo(id, url):
    vk.messages.send(user_id = id, attachment = url, random_id = 0)
    
def parce(param):
    Monday.clear()
    Tuesday.clear()
    Wednesday.clear()
    Thursday.clear()
    Friday.clear()
    HEADERS = {
        'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36 OPR/69.0.3686.77'
    }
    
    bstu = 'http://www.bstu.ru/about/useful/schedule/'
    url = ''
    i = 0
    weak = datetime.date(2010, 6, 16).strftime("%V")
    
    response = requests.get(bstu, headers = HEADERS)
    soup = BeautifulSoup(response.content, 'html.parser')
    
      
    for it in soup.findAll('a'):
        if 'http://www.bstu.ru/static/themes/bstu/schedule/index' in str(it.get('href')) and it.text.lower() == param:
            url = str(it.get('href'))
            break 
    if url != '':       
        response = requests.get(url, headers = HEADERS)
        soup = BeautifulSoup(response.content, 'html.parser')
        items = soup.findAll('td', class_ = 'schedule_std')
        if int(weak)%2 == 0:
            znam = False
        else:
            znam = True
            
        for item in items:
            i = i+1
            test(i,item,znam)
    else:
        return errors[0]
          

group = False
for event in longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW:
        if event.to_me:
            msg = event.text.lower()
            id = event.user_id
            word_list = msg.split()
            if msg == 'понедельник' and group:
                for o in Monday:
                    vk.messages.send(user_id = id, keyboard=json.dumps(key, ensure_ascii=False), message = o, random_id = 0)
            elif msg == 'вторник' and group:
                for o in Tuesday:
                    vk.messages.send(user_id = id, keyboard=json.dumps(key, ensure_ascii=False), message = o, random_id = 0)
            elif msg == 'среда' and group:
                for o in Wednesday:
                    vk.messages.send(user_id = id, keyboard=json.dumps(key, ensure_ascii=False), message = o, random_id = 0)
            elif msg == 'четверг' and group:
                for o in Thursday:
                    vk.messages.send(user_id = id, keyboard=json.dumps(key, ensure_ascii=False), message = o, random_id = 0)       
            elif msg == 'пятница' and group:
                for o in Friday:
                    vk.messages.send(user_id = id, keyboard=json.dumps(key, ensure_ascii=False), message = o, random_id = 0)
            elif msg == 'главная':
                vk.messages.send(user_id = id, keyboard=json.dumps(keyboard, ensure_ascii=False), message = 'Вы на главной странице', random_id = 0)
            elif msg == 'расписание':
                send_msg(id, 'Введите группу')
            elif (any(char in "-" for char in msg)):  
                if parce(msg) == errors[0]:
                    send_msg(id, errors[0])
                else:
                    group = True
                    vk.messages.send(user_id = id, keyboard=json.dumps(key, ensure_ascii=False), message = 'Выберите день недели', random_id = 0)
            elif msg == 'изменить группу':
                if group:
                    send_msg(id, 'Введите группу')
                else:
                    vk.messages.send(user_id = id, keyboard=json.dumps(keyboard, ensure_ascii=False), message = errors[2], random_id = 0)
            else:
                send_msg(id, errors[1])
                    