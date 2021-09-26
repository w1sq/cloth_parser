from pyrogram import Client
from pathlib import Path

with open('auth_data.txt','r',encoding='utf-8') as f:
    data = f.read().split('\n')

app = Client("userinviter", api_id=data[0], api_hash=data[1],
             phone_number=data[2])


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