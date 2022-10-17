import re
import requests
import xmltodict
import time
import config

FILE_POSTED = config.FILE_POSTED

def get_posted_works():
    try:
        with open(FILE_POSTED, 'r') as f:
            return f.read().split('|[%SPLIT%]|')
    except:
        return False
        
        
def work_is_exist(works, link):
    for k, v in enumerate(works):
        if v == link:
            return True
    return False

def add_link_to_file(link):
    works = get_posted_works()
    with open(FILE_POSTED, 'a') as f:
        if works and len(works) > 0:
            # text = ''
            # for k, v in enumerate(works):
            #     text = text + f'|[%SPLIT%]|{link}'
            f.write(f'|[%SPLIT%]|{link}')
        else:
            f.write(f'|[%SPLIT%]|{link}')
            
            
def prepare_text_to_send(text):
    for k, sb in enumerate(config.SUBS):
        text = re.sub(sb['template'], sb['sub'], text)
    return text

def send_to_telegram(text):
    data = {'chat_id':config.USER_ID, 'text': text}
    requests.post('https://api.telegram.org/bot'+config.TOKEN+'/sendMessage', data=data)
            

while True:
    x = requests.get(config.UPWORK_URL)
    try:
        rss = xmltodict.parse(x.text).get('rss')
    except:
        time.sleep(30*60)
        continue
    
    channel = rss.get('channel')
    if not channel:
        time.sleep(30*60)
        continue
    

    items = channel.get('item')
    
    for k, item in enumerate(items):
        link = item.get('link')
        works = get_posted_works()
        if not works:
            add_link_to_file(link)
            continue
        if not work_is_exist(works, link):
            add_link_to_file(link)
            text = f'''{item.get('title')}\n\n{item.get('description')}\n\n{item.get('pubDate')}\n{link}'''
            text = prepare_text_to_send(text)
            send_to_telegram(text)
            print(text)
        else:
            print('is exist')
    time.sleep(15*60)