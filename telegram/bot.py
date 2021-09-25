from pyrogram import Client
from pathlib import Path


API_ID = 7156723
API_HASH = 'bee99f46cea8eb54676e5258eb906ce1'
PHONE_NUMBER = '+79152409140'

app = Client("sender", api_id=API_ID, api_hash=API_HASH,
             phone_number=PHONE_NUMBER)

if __name__ == '__main__':
    with open(f'message.txt','r',encoding='utf-8') as message:
        message = message.read()
    app.start()
    dialogs = app.get_dialogs()
    with open('groups.txt','r',encoding='utf-8') as f:
        names = f.read().split('\n')
    for name in names:
        chat_id = 0
        for dialog in dialogs:
            if dialog['chat']['title'] == name:
                chat_id = int(dialog['chat']['id'])
        if chat_id == 0:
            print('Группа не нашлась')
        else:
            my_file = Path(f"{name}")
            if my_file.is_file():
                with open(f'{name}.txt','r',encoding='utf-8') as sent:
                    sent_members = sent.read().split('\n')
            else:
                sent_members = []
            members = app.get_chat_members(chat_id=chat_id)
            with open(f'{name}.txt','w',encoding='utf-8') as sent:
                for member in members:
                    member_id = member['user']['id']
                    if member_id not in sent_members:
                        app.send_message(member_id,message)
                        sent.write('\n'+ str(member_id))
    app.stop()