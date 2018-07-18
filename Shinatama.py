import telepot
from pprint import pprint
from time import sleep
import requests
from telepot.namedtuple import ReplyKeyboardMarkup
import urllib3

docURL_NoAPI = 'https://docs.google.com/spreadsheets/d/1gwXTFcBnWk4ZZVlvd3pphlb78nkwUxnVY-WQQVpyicE/'

myproxy_url = 'https://51.38.131.129:3128/'
#myproxy_url = 'https://80.211.169.186:8080/'
#прокси взяты отсюда
#https://hidemy.name/ru/proxy-list/?type=s#list
zavs = ['183 МЗ','КЖБИ','ОЗЖБК', 'АЗЖБК', 'НЗЖБК', 'ТЖСК']
factories ={}
for i in zavs:
    factories.update({i:''})
factories.update({'Последнее обновление':''})
telepot.api._pools = {
    'default': urllib3.ProxyManager(proxy_url=myproxy_url, num_pools=3, maxsize=10, retries=False, timeout=30), }

telepot.api._onetime_pool_spec = (
    urllib3.ProxyManager, dict(proxy_url=myproxy_url, num_pools=1, maxsize=1, retries=False, timeout=30))

token = '503612450:AAGv5Qt0FOl6oluaA2-YHpuOUnV2kqKZif8'
bot = telepot.Bot(token)
#response = bot.getUpdates()
#ID=response[0]['message']['from']['id']

start_keyboard = ReplyKeyboardMarkup(resize_keyboard=True, keyboard=[['Призвать Солнышко']])

bttns = [str(i) for i in zavs]
#pprint(bttns)
bttns_menu = [
    [bttns[0],bttns[1]],
    [bttns[2],bttns[3]],
    [bttns[4],bttns[5]],
    ['Cпасибо, Солнышко, свет очей моих!']
]
keyboard = ReplyKeyboardMarkup(keyboard=bttns_menu, resize_keyboard=True)

'''
bot.sendMessage(chat_id=ID, text='Choose Your Destiny', reply_markup=keyboard)

response = bot.getUpdates()
ID=response[0]['message']['from']['id']
pprint(response[len(response)-1][0])
'''
#response = bot.getUpdates()
#ID=response[0]['message']['from']['id']
#last_update_id = response[len(response)-1]['update_id']
#print(last_update_id)
#print(response[len(response)-1]['message']['text'])
#print(response[len(response)-1]['update_id'])
t=0
last_update_id=0
while True:
    response = bot.getUpdates()
    ID = response[len(response) - 1]['message']['from']['id']
    #last_update_id = response[len(response) - 1]['update_id']
    response_text = response[len(response) - 1]['message']['text']
    #print(response_text)
    if response[len(response)-1]['update_id']!=last_update_id:
        if response_text=='Призвать Солнышко':
            #print('0000')
            bot.sendMessage(chat_id=ID, text="Выберите завод", reply_markup=keyboard)
        elif response_text in factories.keys():
            resp = requests.session().get(docURL_NoAPI)
            for i in factories.keys():
                for s in resp.text.split('\n'):
                    if s.find(i) > 0:
                        a = [str(x) for x in s.split(',')]
                        factories.update({i: a[1][1:]})
            answer = response_text +' '+ factories[response_text].lower()+', мой господин!'
            bot.sendMessage(chat_id=ID, text=answer, reply_markup=keyboard)
        elif response_text =='Cпасибо, Солнышко, свет очей моих!':
            bot.sendMessage(chat_id=ID, text="Рада служить вам, мой господин, призовите меня в удобное время", reply_markup=start_keyboard)
        else:
            bot.sendMessage(chat_id=ID, text='Призовите Солнышко', reply_markup=start_keyboard)
    last_update_id=response[len(response)-1]['update_id']
    sleep(1)