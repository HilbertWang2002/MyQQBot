# -*- coding:gbk -*-
from nonebot import on_command, CommandSession
import requests,json
@on_command('talk', aliases=(''))
async def talk(session: CommandSession):
    sentence = session.get('sentence', prompt='�������˵ʲô��')
    payload = {'showapi_appid':'107968','info':sentence,'userid':'userid','showapi_sign':'f8f1ea25878742e69dfc5a5ef6eff9b7'}
    r = requests.get("http://route.showapi.com/60-27", params=payload)
    text = json.loads(r.text)
    await session.send(text['showapi_res_body']['text'])
    
@talk.args_parser
async def _(session: CommandSession):
    # ȥ����Ϣ��β�Ŀհ׷�
    stripped_arg = session.current_arg_text.strip()

    if session.is_first_run:
        # �������һ�����У���һ�ν�������Ự��
        if stripped_arg:
            session.state['sentence'] = stripped_arg
        return

    if not stripped_arg:
        session.pause('Ҫ˵�Ļ�����Ϊ���أ�����������')
    session.state[session.current_key] = stripped_arg